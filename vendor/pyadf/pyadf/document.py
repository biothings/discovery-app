#! /usr/bin/python3
# -*- coding: utf-8 -*-

from pyadf.group_node import GroupNode
from pyadf.group_node_children_mixin import GroupNodeChildrenMixin

class Document(GroupNode, GroupNodeChildrenMixin):
    type = 'doc'

    def to_doc(self):
        result = super(Document,self).to_doc()
        result['version'] = 1
        result['content'] = [ x.to_doc() for x in self.content ]
        return {'body': result}