# pylint: disable=invalid-name,global-statement

''' Schema.org Datasource Indexer '''

import functools
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from discovery.web.api.es.doc import Class, Schema

print()
print("-"*100)
print(" "*35, "Schema.org Auto Indexer")
print("-"*100)
print()

SCHEMA_ORG_URL = "https://schema.org/version/3.5/schema.jsonld"

res = requests.get(SCHEMA_ORG_URL).json()
print('Downloaded', len(res['@graph']), 'objects.\n')

superclses = {}
properties = {}

for obj in res['@graph']:
    if '@type' in obj:
        if obj['@type'] == 'rdfs:Class':
            if 'rdfs:subClassOf' in obj:
                # single parent
                if isinstance(obj['rdfs:subClassOf'], dict):
                    superclses[obj['@id']] = [obj['rdfs:subClassOf']['@id']]
                # multiple parents
                elif isinstance(obj['rdfs:subClassOf'], list):
                    superclses[obj['@id']] = [item['@id'] for item in obj['rdfs:subClassOf']]
                else:
                    raise TypeError
            else:
                print('[INFO] Found base class', obj['@id'])
        elif obj['@type'] == 'rdf:Property':
            DOMAIN = "http://schema.org/domainIncludes"
            if DOMAIN in obj:
                clses = []
                # belong to a single cls
                if isinstance(obj[DOMAIN], dict):
                    clses = [obj[DOMAIN]['@id']]
                # belong to multiple clses
                elif isinstance(obj[DOMAIN], list):
                    clses = [item['@id'] for item in obj[DOMAIN]]
                else:
                    raise TypeError
                for cls_ in clses:
                    if cls_ in properties:
                        properties[cls_].append(obj['@id'])
                    else:
                        properties[cls_] = [obj['@id']]
            else:
                print('[WARNING] Skipping domainless property', obj['@id'])
        else:
            pass
    else:
        print('[WARNING] Skipping typeless object', obj['@id'])

print()
print('Loaded', len(superclses), 'class nodes.')
print('Loaded', len(properties), 'property nodes.')
print()
print('Indexing Legend')
print('100 documents per line')
print(' . : Created')
print(' ^ : Updated')
print()

schemas = []
for obj in res['@graph']:
    if '@type' in obj and obj['@type'] == 'rdfs:Class':
        clses = superclses[obj['@id']] if obj['@id'] in superclses else []
        props = properties[obj['@id']] if obj['@id'] in properties else []
        # convert url to name
        clses = [url[18:] for url in clses if url.startswith('http://schema.org/') or url]
        props = [url[18:] for url in props if url.startswith('http://schema.org/') or url]
        ###### DEBUG #####
        # print()
        # print(obj['@id'])
        # print(clses)
        # print(props)
        # print()
        ##################
        cls_ = Class(name=obj['rdfs:label'], clses=clses, props=props, schema='schema')
        cls_.url = obj['@id'] + '.jsonld'
        cls_.comment = obj['rdfs:comment']
        schemas.append(cls_)


# Index schema
Schema('schema', SCHEMA_ORG_URL, 'schema_org_auto_indexer').save()

# Index classes

sample_size = 50  # for performance benchmark

count = -sample_size  # number of dots printed this line
lock = threading.Lock()


def es_save(sch):
    ''' save a schema to es index '''
    new_created = sch.save(refresh=False)
    global count, lock
    with lock:
        if new_created:
            print('.', end='')
        else:
            print('^', end='')
        count += 1
        if count > 99:  # 100 per line
            print()
            count = 0
        sys.stdout.flush()
    return new_created


start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as executor:
    res_sample = executor.map(es_save, schemas[:sample_size])
end = time.perf_counter()
print()

print()
print('Estimated time left:',
      round((len(schemas) - sample_size) / sample_size * (end - start)), 'seconds.')
print()

with ThreadPoolExecutor(max_workers=4) as executor:
    res_main = executor.map(es_save, schemas[sample_size:])
    res = list(res_sample) + list(res_main)
end = time.perf_counter()
print()

print()
print('Total time spent:', round((end - start)), 'seconds.')
print('Created', functools.reduce(lambda a, b: a+b, res), 'document(s).')
print('Updated', len(res) - functools.reduce(lambda a, b: a+b, res), 'document(s).')
print()
