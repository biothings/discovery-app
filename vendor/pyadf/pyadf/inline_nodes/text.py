from pyadf.inline_nodes.inline_node import InlineNode

class Text(InlineNode):
    type = 'text'
    def __init__(self, text):
        self.text = text
        super(Text, self).__init__()

    def to_doc(self):
        result = super().to_doc()

        result['text'] = self.text

        return result