'''
    Empty Index Creator
'''

from discovery.api.es.doc import SchemaClass, Schema, DatasetMetadata
from elasticsearch_dsl import Index


def main():
    '''
        Quick Setup Script

        - Create two empty indexes
        - Meet minimum running requirement

    '''

    index_primary = Index('discover_schema')
    index_secondary = Index('discover_class')

    # remove existing indexes

    if index_primary.exists():
        index_primary.delete()

    if index_secondary.exists():
        index_secondary.delete()

    Schema.init()
    SchemaClass.init()
    DatasetMetadata.init()


if __name__ == "__main__":
    main()
