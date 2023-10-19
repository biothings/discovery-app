import os
import os.path
import tornado
import tornado.gen
import tornado.web
import tornado.websocket
import tornado.httpclient

ap = os.path.abspath
join = os.path.join


# https://github.com/timkpaine/tornado-proxy-handlers/blob/main/tornado_proxy_handlers/handlers.py#L13
# Used to proxy another local port serving the frontend code as a default on port 3000
# Any other route not defined in python code will be handled by the frontend
class ProxyHandler(tornado.web.RequestHandler):
    def initialize(self, proxy_url, **kwargs):
        super(ProxyHandler, self).initialize(**kwargs)
        self.proxy_url = proxy_url
        if not self.proxy_url.endswith('/'):
            self.proxy_url + '/'

    @tornado.gen.coroutine
    def get(self, url=None):
        """Get the login page"""
        if url is None:
            if self.request.uri.startswith("/"):
                url = self.request.uri[1:]
            else:
                url = self.request.uri
        url = self.proxy_url + url
        req = tornado.httpclient.HTTPRequest(url)
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch(req, raise_error=False)
        # websocket upgrade
        if response.code == 599:
            self.set_status(200)  # switching protocols
            return

        self.set_status(response.code)
        if response.code != 200:
            self.finish()
        else:
            if response.body:
                for header in response.headers:
                    if header.lower() == "content-length":
                        self.set_header(
                            header,
                            str(
                                max(
                                    len(response.body),
                                    int(response.headers.get(header)),
                                )
                            ),
                        )
                    else:
                        if header.lower() != "transfer-encoding":
                            self.set_header(header, response.headers.get(header))

            self.write(response.body)
            self.finish()
