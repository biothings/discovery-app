'''
    ES Tests
    Require Elasticsearch setup at localhost:9200
'''

from discovery.web.api.es.doc import Class, Schema

from discovery.tests import run


def setup():
    ''' Module Level Setup '''

    url = ('https://raw.githubusercontent.com/data2health/'
           'schemas/biothings/biothings/biothings_curie_kevin.jsonld')

    schema = Schema('bts', url, 'tester')
    schema.save()

    Class.import_from(schema)


def test_01():
    ''' [ES Schema Class] Retrival by "_id" '''

    Schema.get(id='bts')


def test_02():
    ''' [ES Schema Class] Saving RAW format '''

    schema = Schema.get(id='bts')
    remote_file = schema.retrieve_raw()
    assert "http://schema.biothings.io/" in remote_file


def test_03():
    ''' [ES Class Class] Retrival by "_id" '''

    Class.get(id="bts:BiologicalEntity")


if __name__ == '__main__':

    run('ES Local Test')
