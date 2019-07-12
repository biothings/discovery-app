'''
    ES Tests
    Require Elasticsearch setup at localhost:9200
'''

from discovery.scripts.index_schema import index_schema
from discovery.tests import run
from discovery.api.es.doc import SchemaClass, Schema


def setup():
    ''' Module Level Setup '''

    url = ('https://raw.githubusercontent.com/data2health'
           '/schemas/master/cvisb/cvisb_dataset.json')

    index_schema('cvisb', url, 'namespacestd0')


def test_01():
    '''
    [ES Schema Class] Retrival by "_id"
    '''
    Schema.get(id='cvisb')


def test_02():
    '''
    [ES Schema Class] Saving RAW format
    '''
    schema = Schema.get(id='cvisb')
    text = schema.decode_raw()
    assert "Dataset in the Center for Viral Systems Biology" in text


def test_03():
    '''
    [ES Class Class] Retrival by "_id"
    '''
    SchemaClass.get(id="cvisb:CvisbDataset")


if __name__ == '__main__':

    run('ES Local Test')
