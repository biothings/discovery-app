from pyadf.group_node import GroupNode
from pyadf.group_node_children_mixin import GroupNodeChildrenMixin

class BlockQuote(GroupNode, GroupNodeChildrenMixin):
    type = 'blockquote'
    def __init__(self, parent=None):
        super(BlockQuote, self).__init__(parent=parent)        


