import unittest
from pyadf.code_block import CodeBlock

class CodeBlockTests(unittest.TestCase):

    def test_codeblock_with_language(self):
        codeblock = CodeBlock('python').text('import antigravity')
        doc = codeblock.to_doc()

        self.assertEqual(doc, {
            'type': 'codeBlock',
            'attrs': {
                'language': 'python'
            },
            'content': [{
                'type': 'text',
                'text': 'import antigravity'
            }]
        })

    def test_codeblock_without_language(self):
        codeblock = CodeBlock().text('import antigravity')
        doc = codeblock.to_doc()

        self.assertEqual(doc, {
            'type': 'codeBlock',
            'content': [{
                'type': 'text',
                'text': 'import antigravity'
            }]
        })

if __name__ == '__main__':
    unittest.main()
