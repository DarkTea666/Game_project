import json
import unittest
from unittest import TestCase, main
from unittest.mock import MagicMock, sentinel, patch
from cocos.director import director

from util import util_starting_stats
from database_ideas import *
from map_generation import *
from create_monster import *

class TestDatabase(TestCase):
    def SetUp(self):
        director.init()
    def TearDown(self):
        self.window.close()

    #tiles
    def test_encode_tile_1(self):
        with self.assertRaises(TypeError):
            json.dumps(complex(9,3), default = encode_tile)

    @patch('map_generation.Sprite.__init__', return_value = sentinel.sprite_init)
    def test_encode_tile2(self, m_sprite_init):
        tile = Tile(sentinel.image, 1, True)
        self.assertNotEqual(json.dumps(tile, default = encode_tile),
                {'exit':False, 'entrance':False, 'passable':True, 'water':False,
                'void':False, 'vegetation':False, 'cracked':False,
                'extend_dict':False})

    @patch('map_generation.Sprite._get_image', return_value = sentinel.get_image)
    @patch('map_generation.Sprite.__init__', return_value = sentinel.sprite_init)
    def test_tile_database(self, m_sprite_init, m_get_image):#TODO: make a tile arrtibute with image path
        with sqlite3.connect(':memory:') as db:
            db.execute(create_tile_table)
            tile = Tile(sentinel.image, 1, True)
            import pdb; pdb.set_trace()
            tile_inf = json.dumps(tile, default = encode_tile)
            db.execute(insert_tile, [4, 4, 1, tile_inf])
            for that_tile in db.execute(select_level_tiles, [1]):
                a_tile = json.loads(that_tile[3])#that_tile is a tuple
                self.assertEqual(a_tile, tile)
    #mobs
    def test_encode_mob1(self):
        with self.assertRaises(TypeError):
            json.dumps(complex(1,2), default = encode_mob)

    @patch('create_monster.Sprite.scale.__set__', return_value = sentinel.scale_set)#smth wrong here
    @patch('create_monster.Sprite.__init__', return_value = sentinel.sprite_init)
    def test_encode_mob2(self, m_sprite_init, m_scale_set):
        mob = Monster(sentinel.image, util_starting_stats.Gnoll_hunter, 1)
        self.assertEqual(json.dumps(tile, default = encode_mob), {})

    @patch('create_monster.Sprite.scale.__set__', return_value=sentinel.scale_set)  # smth wrong here
    @patch('create_monster.Sprite.__init__', return_value=sentinel.sprite_init)
    def test_mob_database(self, m_scale_set, m_sprite_init):
        with sqlite3.connect(':memory:') as db:
            db.execute(create_mob_table)
            mob = Monster(sentinel.image, util_starting_stats.Gnoll_hunter, 1)
            mob_inf = json.dumps(tile, default = encode_mob)
            db.execute(insert_mob, [4, 4, 1, mob_inf])
            for that_mob in db.execute(select_level_mobs, [1]):
                print('########################################################################################')
                print(that_mob)
                that_mob = json.loads(that_mob)
                self.assertEqual(that_mob, mob)


if __name__ == '__main__':
    unittest.main()

