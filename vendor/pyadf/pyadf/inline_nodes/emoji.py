from .inline_node import InlineNode

class Emoji(InlineNode):
    type = 'emoji'
    def __init__(self, shortname, emoji_id=None, fallback=None):
        super(Emoji, self).__init__()
        self.shortname = shortname
        self.id = emoji_id
        self.fallback = fallback

    def attrs(self):
        result = {
            'shortName': ":{}:".format(self.shortname)
        }
        if (self.id != None):
            result['id'] = self.id
        if (self.fallback != None):
            result['fallback'] = self.fallback

        return result