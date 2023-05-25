"""
Calculate metadata coverage of documents registered on DDE
and save coverage on Schema index
"""

import logging

from discovery.model.dataset import Dataset
from discovery.model.schema import Schema
from discovery.registry import schemas


class DocumentCoverageChecker:
    classes_found = {}
    coverage = {}

    def percentage(self, part, whole):
        return round(100 * float(part) / float(whole), 2)

    def check_field(self, meta_type, prop, value):
        if isinstance(value, dict):
            self.check_dictionary(value)
        else:
            if prop not in ["_score", "_meta", "_ts", "_id", "@context", "@type"]:
                # ignore internal fields not relevant
                if prop not in self.classes_found[meta_type]:
                    # property comes from schema not metadata
                    # property exists but not found yet
                    if value == "SCHEMA PROPERTY":
                        self.classes_found[meta_type][prop] = 0
                    else:
                        self.classes_found[meta_type][prop] = 1
                else:
                    self.classes_found[meta_type][prop] += 1
            else:
                logging.info("skipping internal field: %s", prop)


    def check_dictionary(self, doc):
        meta_type = doc.get("@type", None)
        if meta_type:
            if ":" not in meta_type:
                # default schema.org prefix
                meta_type = "schema:" + meta_type
            if meta_type not in self.classes_found:
                # will be the 100% #
                self.classes_found[meta_type] = {"_count": 1}
                # get schema for this meta type class
                try:
                    schema_class = schemas.get_class(meta_type.split(":")[0], meta_type)
                    schema_properties = schema_class["properties"]
                    for prop in schema_properties:
                        self.check_field(meta_type, prop["label"], "SCHEMA PROPERTY")
                except:
                    logging.info("schema for this class does not exist: %s", meta_type)
            else:
                self.classes_found[meta_type]["_count"] += 1
            for prop, value in doc.items():
                self.check_field(meta_type, prop, value)
        else:
            logging.info(f"Doc has no @type: {doc}")

    def restructure_results(self):
        for k, v in self.classes_found.items():
            # sort in ascending order
            v = dict(sorted(v.items(), key=lambda item: item[1]))
            count = v["_count"]
            # delete temp count so it's not included
            v.pop("_count", None)
            for key, val in v.items():
                if k not in self.coverage:
                    self.coverage[k] = {"coverage": {}, "count": count}
                self.coverage[k]["coverage"][key] = self.percentage(val, count)


def daily_coverage_update():
    """
    Look through metadata and calculate field coverage per class instance
    """
    datasets = Dataset.search().extra(size=1000)
    docs = datasets.source(True).scan()
    checker = DocumentCoverageChecker()
    for doc in docs:
        doc = doc.to_dict()
        checker.check_dictionary(doc)
    checker.restructure_results()
    new_meta = {"_meta": {"metadata_coverage": checker.coverage}}
    s = Schema()
    s.update_index_meta(new_meta)
    print("Coverage update complete")
