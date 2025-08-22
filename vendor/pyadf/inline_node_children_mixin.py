from pyadf.inline_nodes.text import Text
from pyadf.inline_nodes.emoji import Emoji
from pyadf.inline_nodes.mention import Mention

class InlineNodeChildrenMixin(object):

    def text(self, text):
        node = Text(text)
        self.content.append(node)
        return self

    def emoji(self, shortname, emoji_id=None, fallback=None):
        node = Emoji(shortname, emoji_id=emoji_id, fallback=fallback)
        self.content.append(node)
        return self

    def mention(self, mention_id, mention_text, access_level=None):
        node = Mention(mention_id, mention_text, access_level=access_level)
        self.content.append(node)
        return self