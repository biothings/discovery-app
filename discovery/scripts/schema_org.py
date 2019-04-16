# pylint: disable=invalid-name

''' Schema.org Datasource Indexer '''

import sys
import time

import requests

from discovery.web.api.es.doc import Metadata, Schema

res = requests.get("https://schema.org/version/3.4/schema.jsonld").json()
print('Downloaded', len(res['@graph']), 'objects.\n')

subclasses = {}
properties = {}

for obj in res['@graph']:
    if '@type' in obj:
        if obj['@type'] == 'rdfs:Class':
            if 'rdfs:subClassOf' in obj:
                # single parent
                if isinstance(obj['rdfs:subClassOf'], dict):
                    subclasses[obj['@id']] = [obj['rdfs:subClassOf']['@id']]
                # multiple parents
                elif isinstance(obj['rdfs:subClassOf'], list):
                    subclasses[obj['@id']] = [item['@id'] for item in obj['rdfs:subClassOf']]
                else:
                    raise TypeError
            else:
                print('Class', obj['@id'], 'is a base class.')
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
                print('Property', obj['@id'], 'is not attached to any class.')
        else:
            pass
    else:
        print('Skipping typeless object', obj['@id'])

print()
print('Loaded', len(subclasses), 'class nodes.')
print('Loaded', len(properties), 'property nodes.\n')

schemas = []
for obj in res['@graph']:
    if '@type' in obj and obj['@type'] == 'rdfs:Class':
        clses = {obj['@id']}
        props = set()
        queue = [obj['@id']]
        while queue:
            cls_ = queue.pop(0)
            if cls_ in properties:
                props.update(properties[cls_])
            if cls_ in subclasses:
                clses.update(subclasses[cls_])
                for subcls in subclasses[cls_]:
                    if subcls not in queue:
                        queue.append(subcls)
        clses = [url[18:] for url in clses if url.startswith('http://schema.org/') or url]
        props = [url[18:] for url in props if url.startswith('http://schema.org/') or url]
        # print()
        # print(obj['@id'])
        # print(clses)
        # print(props)
        # print()
        meta = Metadata(username='schema_org_auto_indexer',
                        url=obj['@id'] + '.jsonld', slug=obj['rdfs:label'])
        print(obj['@id'] + '.jsonld')
        schema = Schema(clses=clses, props=props, _meta=meta)
        schemas.append(schema)

perf_sample_size = 10

start = time.perf_counter()
for schema in schemas[: perf_sample_size]:
    schema.save(refresh=False)
    print('.', end='')
    sys.stdout.flush()
end = time.perf_counter()
print()

print()
print('Estimated', int(len(schemas)/perf_sample_size*(end - start)/60), 'minute(s) left.')
print()

for schema in schemas[10:]:
    schema.save(refresh=False)
    print('.', end='')
    sys.stdout.flush()
