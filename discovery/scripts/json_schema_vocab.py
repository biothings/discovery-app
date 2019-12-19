from jsonschema import Draft7Validator, validators
from jsonschema.exceptions import SchemaError, ValidationError

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
                "ontology": "edam",   # must be a ontology_id from supported ontology in EBI OLS
                "children_of": "http://edamontology.org/topic_3361"   # IRI of an ontology term. The entire ontology is used if not specified
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
                "ontology": ["edam", "ncit"],    # mutliple ontology ids are supported
                "children_of": [
                    "http://edamontology.org/topic_3361",
                    "http://purl.obolibrary.org/obo/NCIT_C20368"    # multiple ontology terms are supported
                ]
            }
        }
    }
}

schema_not_strict = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "measurementTechnique": {
            "type": "string",
            "vocabulary": {
                "ontology": "edam",
                "children_of": "http://edamontology.org/topic_3361",
                "strict": False    # optional, if False, valiator only print out a warning msg, instead of an ValidationError
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

    # EBI OLS API Doc here: https://www.ebi.ac.uk/ols/docs/api
    ols_url = "http://www.ebi.ac.uk/ols/api/search"
    res = requests.get(ols_url, params=ols_params)
    ols_data = res.json()
    return ols_data['response']["numFound"] > 0


def is_controlled_vocabulary(validator, value, instance, schema):
    if not isinstance(instance, str):
        yield ValidationError("%r is not a string" % instance)

    ontology = value.get('ontology', None)
    if not ontology:
        yield SchemaError('must provide "ontology" for "vocabulary" in schema')
    children_of = value.get('children_of', None)
    is_strict = value.get('strict', True)
    if not term_found_in_ontology(instance, ontology, children_of):
        err_msg = f'value "{instance}" not found in "{ontology}" ontology'
        if children_of:
            err_msg += f' (children nodes of "{children_of}")'
        if is_strict:
            # raise a valiation error, this is the default
            yield ValidationError(err_msg)
        else:
            # just print out a warning msg
            print("Warning:", err_msg)


def get_validator(schema, default=False):
    """return a validator supporting "vocabulary" rule,
       return a default validator if default is True.
    """
    if default:
        return Draft7Validator(schema)

    all_validators = dict(Draft7Validator.VALIDATORS)
    all_validators['vocabulary'] = is_controlled_vocabulary

    VocabularyValidator = validators.create(
        meta_schema=Draft7Validator.META_SCHEMA, validators=all_validators
    )

    vocab_validator = VocabularyValidator(schema)
    return vocab_validator


def test_data():
    print("Testing single ontology term...")
    vocab_validator = get_validator(schema)
    vocab_validator.validate(data)

    print("Testing multiple ontology term...")
    vocab_validator = get_validator(schema_multiple)
    vocab_validator.validate(data)
    vocab_validator.validate(data_2)


def test_error():
    data = {
        "measurementTechnique": "invalid string"
    }
    vocab_validator = get_validator(schema_multiple)
    vocab_validator.validate(data)


def test_not_strict():
    data = {
        "measurementTechnique": "invalid string"
    }
    vocab_validator = get_validator(schema_not_strict)
    vocab_validator.validate(data)


def test_all():
    test_data()
    test_not_strict()
    test_error()
