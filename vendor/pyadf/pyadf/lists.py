from pyadf.group_node import GroupNode
from pyadf.group_node_children_mixin import GroupNodeChildrenMixin


class _ListNode(GroupNode):

    def add_item(self, item):
        "Simplified implementation to add a single list item"
        list_item = ListItem(self)
        list_item.content.append(item)
        self.content.append(list_item)


class BulletList(_ListNode):
    type = 'bulletList'


class OrderedList(_ListNode):
    type = 'orderedList'


class ListItem(GroupNode, GroupNodeChildrenMixin):
    type = 'listItem'


class TaskList(GroupNode):
    type = 'taskList'

    def __init__(self, local_id, parent=None):
        super(TaskList, self).__init__(parent=parent)
        self.local_id = local_id

    def attrs(self):
        return {
            'localId': self.local_id
        }

    def add_item(self, content, local_id, state='TODO'):
        task_item = TaskItem(self, local_id=local_id, state=state)
        task_item.content.append(content)
        self.content.append(task_item)
        return task_item


class TaskItem(GroupNode, GroupNodeChildrenMixin):
    type = 'taskItem'

    def __init__(self, parent, local_id, state):
        super(TaskItem, self).__init__(parent=parent)
        self.local_id = local_id
        self.state = state

    def attrs(self):
        return {
            'localId': self.local_id,
            'state': self.state
        }
