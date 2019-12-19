from jsonschema import Draft7Validator, validators
from jsonschema.exceptions import ValidationError

import requests

data = {
    "measurementTechnique": "Whole genome sequencing"
}

data_2 = {
    "measurementTechnique": "Gene Knockout"
}


schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "measurementTechnique": {
            "type": "string",
            "vocabulary": {
                "ontology": "edam",
                "children_of": "http://edamontology.org/topic_3361"
            }
        }
    }
}

schema_multiple = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "measurementTechnique": {
            "type": "string",
            "vocabulary": {
                "ontology": ["edam", "ncit"],
                "children_of": [
                    "http://edamontology.org/topic_3361",
                    "http://purl.obolibrary.org/obo/NCIT_C20368"
                ]
            }
        }
    }
}


def term_found_in_ontology(term, ontology, children_of=None):
    ols_params = {
        "q": term,
        "ontology": ontology,
        "fieldList": "id,iri,label",
        "type": "class",
        "queryFields": "label",
        "exact": True
    }
    if children_of:
        ols_params['childrenOf'] = children_of

    for param in ols_params:
        # join list input as comma-sep string
        if param in ['ontology', 'childrenOf'] and isinstance(ols_params[param], list):
            ols_params[param] = ','.join(ols_params[param])

    ols_url = "http://www.ebi.ac.uk/ols/api/search"
    res = requests.get(ols_url, params=ols_params)
    ols_data = res.json()
    return ols_data['response']["numFound"] > 0


def is_controlled_vocabulary(validator, value, instance, schema):
    if not isinstance(instance, str):
        yield ValidationError("%r is not a string" % instance)

    ontology = value.get('ontology', None)
    if not ontology:
        yield ValidationError('must provide "ontology" for "vocabulary" in schema')
    children_of = value.get('children_of', None)
    if not term_found_in_ontology(instance, ontology, children_of):
        err_msg = f'value "{instance}" not found in "{ontology}" ontology'
        if children_of:
            err_msg += f' (children nodes of "{children_of}")'
        yield ValidationError(err_msg)


def test_data():
    all_validators = dict(Draft7Validator.VALIDATORS)
    all_validators['vocabulary'] = is_controlled_vocabulary

    VocabularyValidator = validators.create(
        meta_schema=Draft7Validator.META_SCHEMA, validators=all_validators
    )

    vocab_validator = VocabularyValidator(schema)

    # uncomment this line to test against the default validator
    # vocab_validator = Draft7Validator(schema)

    vocab_validator.validate(data)

    vocab_validator = VocabularyValidator(schema_multiple)
    vocab_validator.validate(data)
    vocab_validator.validate(data_2)
