import unittest
from unittest.mock import sentinel
from unittest.mock import patch
from unittest.mock import MagicMock

from cocos.director import director

from item_menu_layer import ItemMenuLayer

class TestInventory(unittest.TestCase):
    def setUp(self):
        director.init()
    def TearDown(self):
        self.window.close()

    @patch('item_menu_layer.ItemMenuLayer.make_description_labels')
    @patch('item_menu_layer.BatchNode', return_value=sentinel.batch)
    def test_init(self, m_batch_node, m_make_labels):
        item = MagicMock()
        obj = ItemMenuLayer((item, sentinel.func))
        self.assertEqual(sentinel.batch, obj.batch)
        self.assertEqual(sentinel.func, obj.item_funcs)
        self.assertEqual(item, obj.item)
        self.assertEqual(item.menu, obj.description)
        m_make_labels.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
