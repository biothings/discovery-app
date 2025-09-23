import unittest
from pyadf.inline_nodes.marks.link import Link
from pyadf.inline_nodes.text import Text
from pyadf.document import Document

class LinkTests(unittest.TestCase):

    def test_link_with_no_title(self):
        link = Link('http://google.com', None)
        doc = link.to_doc()
        
        self.assertEqual(doc, {
            'type': 'link',
            'attrs': {
                'href': 'http://google.com'
            }
        })


    def test_link_with_title(self):
        link = Link('http://google.com', 'my title')
        doc = link.to_doc()
        
        self.assertEqual(doc, {
            'type': 'link',
            'attrs': {
                'href': 'http://google.com',
                'title': 'my title'
            }
        })

    def test_node_with_link_mark(self):
        text = Text('hello')
        text.add_mark(Link('http://google.com', None))
        doc = text.to_doc()

        self.assertEqual(doc, {
            'type': 'text',
            'text': 'hello',
            'marks': [
                {
                    'type': 'link',
                    'attrs': {
                        'href': 'http://google.com'
                    }
                }
            ]
        })

    def test_node_with_link_and_another_node_following(self):
        self.maxDiff = None
        doc = Document()                            \
            .paragraph()                            \
                .text('hello')                      \
                    .link('http://google.com')      \
                .text('there')                      \
            .end()                                  \
            .to_doc()

        self.assertEqual(doc, {
            'body': {
                'version': 1,
                'type': 'doc',
                'content': [{
                    'type': 'paragraph',
                    'content': [{
                        'type': 'text',
                        'text': 'hello',
                        'marks': [
                            {
                                'type': 'link',
                                'attrs': {
                                    'href': 'http://google.com'
                                }
                            }
                        ]
                    }, {
                        'type': 'text',
                        'text': 'there'
                    }]
                }]
            }
        })

    def test_add_link_with_no_content_throws_exception(self):
        with self.assertRaises(ValueError):
            Document().paragraph().link('http://google.com')