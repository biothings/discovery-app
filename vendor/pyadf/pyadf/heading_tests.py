import unittest
from pyadf.heading import Heading

class HeadingTests(unittest.TestCase):

    def test_heading_with_text(self):
        heading = Heading(2).text('heading text')
        doc = heading.to_doc()

        self.assertEqual(doc, {
            'type': 'heading',
            'attrs': {
                'level': 2
            },
            'content': [{
                'type': 'text',
                'text': 'heading text'
            }]
        })

if __name__ == '__main__':
    unittest.main()