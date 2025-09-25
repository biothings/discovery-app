from pyadf.inline_nodes.marks.mark import Mark

class TextColor(Mark):
    type = 'textColor'
    def __init__(self, color):
        self.color = color
        super(TextColor, self).__init__()


    def attrs(self):
        result = {
            'color': self.color
        }
        return result
