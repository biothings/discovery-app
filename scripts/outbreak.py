"""
    Add dataset metadata to outbreak.api

    Assume elasticsearch related setups exist on the target server.

    python -m scripts.outbreak --help

"""

import logging
from datetime import datetime
import requests
from elasticsearch import Elasticsearch, RequestError
from tornado.options import options, parse_command_line

from discovery.model.dataset import Dataset

options.define('target_host', default='es7.outbreak.info')

MAPPING_URL = 'https://raw.githubusercontent.com/SuLab/outbreak.info-resources/master/outbreak_resources_es_mapping_v3.json'
INDEX_PREFIX = 'outbreak-dataset-'
INDEX_ALIAS = 'outbreak-resources-dataset'


def main():

    parse_command_line()
    client = Elasticsearch(options.target_host)

    # create index
    datestring = ''.join(str(item) for item in datetime.now().timetuple()[:-1])
    index_name = INDEX_PREFIX + datestring
    _ = client.indices.create(index_name, {
        "settings": {
            "query": {
                "default_field": "all"
            },
            "default_pipeline": "resources-common",
            "analysis": {
                "normalizer": {
                    "keyword_lowercase_normalizer": {
                        "filter": [
                            "lowercase"
                        ],
                        "type": "custom",
                        "char_filter": []
                    }
                },
                "analyzer": {
                    "string_lowercase": {
                        "filter": "lowercase",
                        "tokenizer": "keyword"
                    },
                    "whitespace_lowercase": {
                        "filter": "lowercase",
                        "tokenizer": "whitespace"
                    }
                }
            }
        },
        "mappings": {
            "properties": requests.get(MAPPING_URL).json(),
            "dynamic": False
        }
    })
    logging.debug(_)

    for doc in Dataset.search().scan():
        dic = doc.to_json()
        if dic.get('@type') == 'outbreak:Dataset':
            dic['@type'] = 'Dataset'
            try:
                client.index(index_name, dic, id=doc.meta.id)
            except RequestError as err:
                logging.error(err.info)

    # switch index alias
    _ = client.indices.update_aliases({
        "actions": [
            {
                "remove": {
                    "index": INDEX_PREFIX + '*',
                    "alias": INDEX_ALIAS
                }
            },
            {
                "add": {
                    "index": index_name,
                    "alias": INDEX_ALIAS,
                }
            }
        ]
    })
    logging.debug(_)

    # delete old index
    indices = list(client.indices.get(INDEX_PREFIX + '*').keys())
    indices.remove(index_name)
    indices = ','.join(indices)
    _ = client.indices.delete(indices)
    logging.info(_)


if __name__ == "__main__":
    main()
