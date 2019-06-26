
import tornado

from .base import APIBaseHandler


class ProxyHandler(APIBaseHandler):
    '''
    Retrive a document from a remote server to bypass same origin policy
    '''

    async def get(self):

        try:
            url = self.get_argument("url")
            http_client = tornado.httpclient.AsyncHTTPClient()
            response = await http_client.fetch(url)
        except tornado.web.MissingArgumentError as err:
            self.set_status(err.status_code)
            self.write(str(err))
        except tornado.httpclient.HTTPClientError as err:
            self.set_status(err.code)
            self.write(str(err))
        else:
            self.write(response.body)
