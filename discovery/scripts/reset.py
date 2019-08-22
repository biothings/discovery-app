'''
    Reset es indexes

    - Remove existing indexes
    - No data will be populated
'''

from elasticsearch_dsl import Index

from discovery.api.es.doc import DatasetMetadata, Schema, SchemaClass


def main():

    index_primary = Index('discover_schema')
    index_secondary = Index('discover_class')
    index_tertiary = Index('discover_metadata')

    # remove existing indexes

    if index_primary.exists():
        index_primary.delete()

    if index_secondary.exists():
        index_secondary.delete()

    if index_tertiary.exists():
        index_tertiary.delete()

    Schema.init()
    SchemaClass.init()
    DatasetMetadata.init()


if __name__ == "__main__":
    main()
