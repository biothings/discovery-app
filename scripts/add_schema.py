
from tornado.log import enable_pretty_logging

from discovery.utils.indexing import add_schema_by_url

KNOWN_SCHEMAS = {
    'ctsa': 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json',
    'bts': 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld'
}


def main():
    '''
        Interactive Prompt
    '''
    # Will REPLACE/UPDATE original in es.
    prefix = input("Enter the schema namespace:")
    if prefix in KNOWN_SCHEMAS:
        url = KNOWN_SCHEMAS[prefix]
    else:
        url = input("Enter the url where the schema json is hosted:")
    user = input("Enter your email:")
    print(add_schema_by_url(prefix, url, user))


if __name__ == "__main__":
    enable_pretty_logging()
    main()
