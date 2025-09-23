from pyadf.group_node import GroupNode
from pyadf.inline_nodes.text import Text

class Heading(GroupNode):
    type = 'heading'
    def __init__(self, level, parent=None):
        self.level = level
        super(Heading, self).__init__(parent=parent)

    def attrs(self):
        return {
            'level': self.level
        }

    # heading only supports text so let's just hand-roll it here
    def text(self, text):
        node = Text(text)
        self.content.append(node)
        return self