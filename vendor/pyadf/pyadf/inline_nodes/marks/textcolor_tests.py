import unittest
from pyadf.inline_nodes.marks.textcolor import TextColor
from pyadf.inline_nodes.text import Text
from pyadf.document import Document

class LinkTests(unittest.TestCase):

    def test_color(self):
        color = TextColor('blue')
        doc = color.to_doc()
        
        self.assertEqual(doc, {
            'type': 'textColor',
            'attrs': {
                'color': 'blue'
            }
        })

    def test_node_with_textcolor_mark(self):
        text = Text('hello')
        text.add_mark(TextColor('blue'))
        doc = text.to_doc()

        self.assertEqual(doc, {
            'type': 'text',
            'text': 'hello',
            'marks': [
                {
                    'type': 'textColor',
                    'attrs': {
                        'color': 'blue'
                    }
                }
            ]
        })

    def test_node_with_textcolor_and_another_node_following(self):
        self.maxDiff = None
        doc = Document()                            \
            .paragraph()                            \
                .text('hello')                      \
                    .textcolor('blue')              \
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
                                'type': 'textColor',
                                'attrs': {
                                    'color': 'blue'
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