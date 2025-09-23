from pyadf.group_node import GroupNode
from pyadf.inline_nodes.text import Text

class CodeBlock(GroupNode):
    type = 'codeBlock'
    def __init__(self, language='', parent=None):
        self.language = language
        super(CodeBlock, self).__init__(parent=parent)

    def attrs(self):
        if self.language:
            return {
                'language': self.language
            }
        return None

    # codeBlock only supports text so let's just hand-roll it here
    def text(self, text):
        node = Text(text)
        self.content.append(node)
        return self
