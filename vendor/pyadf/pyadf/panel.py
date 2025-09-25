from pyadf.group_node import GroupNode
from pyadf.group_node_children_mixin import GroupNodeChildrenMixin

class Panel(GroupNode, GroupNodeChildrenMixin):
    type = 'panel'
    def __init__(self, panel_type='info', parent=None):
        self.panel_type = panel_type
        super(Panel, self).__init__(parent=parent)

    def attrs(self):
        if self.panel_type:
            return {
                'panelType': self.panel_type
            }
        return None
