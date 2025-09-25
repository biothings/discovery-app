from .node import Node
from pyadf.inline_nodes.marks.link import Link
from pyadf.inline_nodes.marks.textcolor import TextColor

class GroupNode(Node):
    def __init__(self, parent=None):
        super(GroupNode, self).__init__()
        self.content = []
        self.parent = parent

    def to_doc(self):
        result = super().to_doc()

        result['content'] = [f.to_doc() for f in self.content]

        return result

    def end(self):
        return self.parent

    # these marks apply to the last-used inline node
    def link(self, href, title=None):
        if (self.content == None or len(self.content) == 0):
            raise ValueError('Can\'t apply marks when there is no content to mark.')
        node = Link(href, title)
        self.content[-1].add_mark(node)
        return self

    def textcolor(self, color):
        if (self.content == None or len(self.content) == 0):
            raise ValueError('Can\'t apply marks when there is no content to mark.')
        node = TextColor(color)
        self.content[-1].add_mark(node)
        return self