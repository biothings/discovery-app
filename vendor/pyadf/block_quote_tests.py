import unittest
from pyadf.block_quote import BlockQuote

class BlockQuoteTests(unittest.TestCase):
    
    def test_empty_block_quote(self):
        quote = BlockQuote().to_doc()

        self.assertEqual(quote, {
            'type': 'blockquote',
            'content': []
        })

    def test_block_quote_with_text(self):
        quote = BlockQuote()  \
            .paragraph() \
                .text('Hi there') \
            .end() \
            .to_doc()
        
        self.assertEqual(quote, {
            'type': 'blockquote',
            'content': [{
                'type': 'paragraph',
                'content': [{
                    'type': 'text',
                    'text': 'Hi there'
                }]
            }]
        })

    def test_block_quote_with_emoji(self):
        quote = BlockQuote()  \
            .paragraph() \
                .emoji('smile', emoji_id='123', fallback='fallback') \
            .end() \
            .to_doc()
        
        self.assertEqual(quote, {
            'type': 'blockquote',
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