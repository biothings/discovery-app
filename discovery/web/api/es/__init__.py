''' Setup ES '''

from elasticsearch_dsl.connections import connections

# Default elasticsearch connection
connections.create_connection(hosts=['localhost'], timeout=20)
