import tornado.web
import tornado.template
from discovery.registry import datasets


class DatasetHandler(tornado.web.RequestHandler):

    def get(self):
        ids = datasets.get_ids()
        tpl = tornado.template.Template("""
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://discovery.biothings.io/dataset</loc>
            </url>
            {% for _id in ids %}
                {% block _id %}
                <url>
                    <loc>{{ "https://discovery.biothings.io/dataset/" + escape(_id) }}</loc>
                </url>
                {% end %}
            {% end %}
        </urlset>""")
        self.set_header('Content-Type', 'text/xml')
        self.write(tpl.generate(ids=ids))
