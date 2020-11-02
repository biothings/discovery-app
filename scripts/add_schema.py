
import logging

from tornado.log import enable_pretty_logging

from discovery.registry import schemas

logging.getLogger('elasticsearch').setLevel('WARNING')

KNOWN_SCHEMAS = {
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

    print("added " + str(schemas.add(namespace, url, user)) + " schema classes")


if __name__ == "__main__":
    enable_pretty_logging()
    main()
