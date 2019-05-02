''' Create two empty indexes necessary to run discovery app '''

from discovery.web.api.es.doc import Schema, Class

Schema.init()
Class.init()
