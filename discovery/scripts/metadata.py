import sys

import requests
from biothings_schema import Schema as SchemaParser
from elasticsearch_dsl import connections

from discovery.api.es.doc import DatasetMetadata

connections.create_connection(hosts=['localhost'], timeout=20)


def post_metadata_document(url, user, privacy):

    doc = requests.get(url).json()
    parser = SchemaParser("https://raw.githubusercontent.com/data2health/"
                          "schemas/master/Dataset/CTSADataset.json")
    ctsa = parser.get_class('bts:CTSADataset')
    ctsa.validate_against_schema(doc)
    print(DatasetMetadata.from_json(doc, user, privacy).save())


if __name__ == "__main__":
    assert len(sys.argv) == 4, "Need url, user and privacy flag."
    post_metadata_document(sys.argv[1], sys.argv[2], sys.argv[3] in ('true', '1'))
