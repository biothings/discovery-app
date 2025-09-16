from pyadf.heading import Heading
from pyadf.paragraph import Paragraph
from pyadf.code_block import CodeBlock

class GroupNodeChildrenMixin(object):

    def paragraph(self):
        p = Paragraph(self)
        self.content.append(p)
        return p

    def blockquote(self):
        # this sucks, but it avoids an error with a circular dependency
        # between BlockQuote and GroupNodeChildrenMixin
        from pyadf.block_quote import BlockQuote
        b = BlockQuote(self)
        self.content.append(b)
        return b

    def heading(self, level):
        h = Heading(level, parent=self)
        self.content.append(h)
        return h

    def codeblock(self, language=''):
        c = CodeBlock(language, parent=self)
        self.content.append(c)
        return c

    def panel(self, panel_type):
        # another circular dependency
        from pyadf.panel import Panel
        p = Panel(panel_type, parent=self)
        self.content.append(p)
        return p

    def bullet_list(self):
        from pyadf.lists import BulletList
        bl = BulletList(parent=self)
        self.content.append(bl)
        return bl

    def task_list(self, local_id):
        from pyadf.lists import TaskList
        tl = TaskList(local_id=local_id, parent=self)
        self.content.append(tl)
        return tl
