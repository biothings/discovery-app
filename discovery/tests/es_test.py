'''
    ES Tests
    Require Elasticsearch setup at localhost:9200
'''

import gzip

from biothings.tests.helper import equal
from discovery.tests import SCHEMAS, run
from discovery.web.api.es.doc import Schema


def test_01():
    ''' ES Schema Retrival '''
    sch = Schema.get(id=SCHEMAS[0].meta.id)
    equal("Retrived", sch.to_dict(), "Original", SCHEMAS[0].to_dict())


def test_02():
    ''' ES Schema Saving '''
    sch = Schema.get(id=SCHEMAS[1].meta.id)
    remote = sch.decode_raw()
    sch.encode_raw()
    equal("Remote", remote, "Local", gzip.decompress(sch['~raw']).decode())


if __name__ == '__main__':
    run('ES Local Test')
