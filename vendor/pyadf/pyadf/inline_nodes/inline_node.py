from pyadf.node import Node

class InlineNode(Node):

    def __init__(self):
        super(InlineNode,self).__init__()
        self.marks = []

    def add_mark(self, mark):
        self.marks.append(mark)

    def to_doc(self):
        result = super().to_doc()

        if (self.marks != None):                
            mark_count = len(self.marks)
            if (mark_count > 0):
                result['marks'] = [mark.to_doc() for mark in self.marks]

        return result