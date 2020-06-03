
import logging

from tornado.log import enable_pretty_logging

from discovery.utils.controllers import SchemaController

logging.getLogger('elasticsearch').setLevel('WARNING')

KNOWN_SCHEMAS = {
    'ctsa': 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json',
    'bts': 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld'
}


def main():
    '''
        Interactive Prompt
    '''
    # Will REPLACE/UPDATE original in es.
    namespace = input("Enter the schema namespace:")
    if namespace in KNOWN_SCHEMAS:
        url = KNOWN_SCHEMAS[namespace]
    else:
        url = input("Enter the url where the schema json is hosted:")
    user = input("Enter your email:") or 'cwu@scripps.edu'

    print(SchemaController.add(namespace, url, user))


if __name__ == "__main__":
    enable_pretty_logging()
    main()
