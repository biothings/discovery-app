
from .base import APIBaseHandler
from elasticsearch_dsl import Index, Search


class UserQueryHandler(APIBaseHandler):
    '''
    Access schema entries with username
    '''

    def get(self, username):
        '''
        Return a list of schemas that belong to the specified user
        '''

        search = Search(index='discover_schema').query("match", ** {"_meta.username": username})
        response = search.execute()

        self.write({
            "total": response.hits.total,
            "hits": [{
                "name": schema.meta.id,
                "url": schema['_meta'].url
            } for schema in response]
        })
