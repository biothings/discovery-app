import unittest
from pyadf.panel import Panel

class PanelTests(unittest.TestCase):

    def test_empty_panel(self):
        panel = Panel('info').to_doc()

        self.assertEqual(panel, {
            'type': 'panel',
            'attrs': {
                'panelType': 'info'
            },
            'content': []
        })

    def test_panel_with_text(self):
        panel = Panel('info')  \
            .paragraph() \
                .text('Hi there') \
            .end() \
            .to_doc()

        self.assertEqual(panel, {
            'type': 'panel',
            'attrs': {
                'panelType': 'info'
            },
            'content': [{
                'type': 'paragraph',
                'content': [{
                    'type': 'text',
                    'text': 'Hi there'
                }]
            }]
        })

    def test_panel_with_emoji(self):
        panel = Panel('info')  \
            .paragraph() \
                .emoji('smile', emoji_id='123', fallback='fallback') \
            .end() \
            .to_doc()

        self.assertEqual(panel, {
            'type': 'panel',
            'attrs': {
                'panelType': 'info'
            },
            'content': [{
                'type': 'paragraph',
                'content': [{
                    'type': 'emoji',
                    'attrs': {
                        'shortName': ':smile:',
                        'fallback': 'fallback',
                        'id': '123'
                    }
                }]
            }]
        })



if __name__ == '__main__':
    unittest.main()
