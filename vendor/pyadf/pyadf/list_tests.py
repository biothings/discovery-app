import unittest
from .lists import BulletList, OrderedList, ListItem, TaskList
from pyadf.paragraph import Paragraph
from pyadf.document import Document

class ListTests(unittest.TestCase):

    def test_bullet_list_with_no_items(self):
        bullet_list = BulletList()
        doc = bullet_list.to_doc()
        
        self.assertEqual(doc, {
            'type': 'bulletList',
            'content': []
        })

    def test_ordered_list_with_no_items(self):
        ordered_list = OrderedList()
        doc = ordered_list.to_doc()
        
        self.assertEqual(doc, {
            'type': 'orderedList',
            'content': []
        })

    def test_list_item_with_text(self):
        list_item = ListItem()
        list_item.paragraph().text('hello there')
        doc = list_item.to_doc()

        self.assertEqual(doc, {
            'type': 'listItem',
            'content': [{
                'type': 'paragraph',
                'content': [
                    {
                        'type': 'text',
                        'text': 'hello there'
                    }
                ]
            }]
        })

    def test_bullet_list_with_two_items(self):
        bullet_list = BulletList()
        bullet_list.add_item(Paragraph().text('hello'))
        bullet_list.add_item(Paragraph().text('there'))
        
        doc = bullet_list.to_doc()

        self.assertEqual(doc, {
            'type': 'bulletList',
            'content': [
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'hello'
                            }
                        ]
                    }]
                },
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'there'
                            }
                        ]
                    }]
                }
            ]
        })

    def test_ordered_list_with_two_items(self):
        ordered_list = OrderedList()
        ordered_list.add_item(Paragraph().text('hello'))
        ordered_list.add_item(Paragraph().text('there'))
        
        doc = ordered_list.to_doc()

        self.assertEqual(doc, {
            'type': 'orderedList',
            'content': [
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'hello'
                            }
                        ]
                    }]
                },
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'there'
                            }
                        ]
                    }]
                }
            ]
        })

    def test_task_list_with_no_items(self):
        task_list = TaskList(local_id='no_items_local_id')
        doc = task_list.to_doc()

        self.assertEqual(doc, {
            'type': 'taskList',
            'attrs': {'localId': 'no_items_local_id'},
            'content': []
        })

    def test_task_list_with_two_items(self):
        task_list = TaskList(local_id='two_items_local_id')
        task_list.add_item(content=Paragraph().text('hello'), local_id='todo_1_local_id')
        task_list.add_item(content=Paragraph().text('there'), local_id='done_2_local_id', state='DONE')

        doc = task_list.to_doc()

        self.assertEqual(doc, {
            "attrs": {
                "localId": "two_items_local_id"
            },
            "type": "taskList",
            "content": [
                {
                    "attrs": {
                        "localId": "todo_1_local_id",
                        "state": "TODO"
                    },
                    "type": "taskItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": "hello",
                                    "type": "text"
                                }
                            ]
                        }
                    ]
                },
                {
                    "attrs": {
                        "localId": "done_2_local_id",
                        "state": "DONE"
                    },
                    "type": "taskItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": "there",
                                    "type": "text"
                                }
                            ]
                        }
                    ]
                }
            ]
        })
