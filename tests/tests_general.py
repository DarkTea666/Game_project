'''I need to see the imports!!!'''
import time
import unittest
from unittest import TestCase, main
from unittest.mock import MagicMock

from cocos.scene import Scene
from cocos import layer, scene
from cocos.scenes import *
from cocos.director import director
from cocos.actions import Delay, CallFunc

import random

from main_scene import *
from algorithms.algorithms_visibility import tile_line_vis, calculate_visibility
from algorithms.algorithms_pathfinding import tile_score, in_list, find_min_score,\
    tile_do, pathfind_to_target, trace_back_path
from util import util_starting_stats
from create_monster import Monster
from create_character import Player
from map_generation import LevelMap
from interact_layer import InteractableLayer
from effect_layer import EffectLayer
from visibility_layer import VisibilityLayer
from inventories import InventoryLayer
from equiped_layer import EquipedLayer
from util.util_selecting_layer import SelectLayer
from play_layer import PlayingLayer
from items import items_sceptres


class TestGeneral(TestCase):
    def setUp(self):
        self.window = director.init(width=1250, height=800, autoscale=True, resizable=True, visible=False)
        self.player = Player(starting_stats.Human, starting_stats.Warlock)

        random.seed(666)
        self.map_layer = LevelMap(1, subject1=self.player)
        self.map_layer.generate_map()
        self.play_layer = PlayingLayer(self.player, self.map_layer, subj1=self.player)
        self.interactive_layer = InteractableLayer(self.map_layer, subj1=self.player, subj2=self.play_layer)
        self.effect_layer = EffectLayer(self.map_layer)
        self.visibility_layer = VisibilityLayer(self.map_layer, subj1=self.play_layer, subj2=self.player)
        self.equip_layer = EquipedLayer()
        self.inventory_layer = InventoryLayer(self.play_layer, self.interactive_layer, self.equip_layer)

        self.player.equip_layer = self.equip_layer
        self.play_layer.effect_layer = self.effect_layer
        self.play_layer.player.inventory = self.inventory_layer
        self.play_layer.interactive_layer = self.interactive_layer
        self.equip_layer.inv_layer = self.inventory_layer
        self.play_layer.spawn_initial_mobs()
        self.play_layer.spawn_items()
        self.equip_layer.visualise_equiped_items()

        t = util_starting_stats.Gnoll_hunter
        self.mob1 = Monster(t.monster_sprite, t, 1)
        self.mob1.position = (10 + 1) * 50, (len(self.map_layer.map) - 7) * 50

        main_scene = FirstScene()

    def tearDown(self):
            self.window.close()


    def test_tile(self):#
        self.assertEqual(self.player.tile(), {'i':-8, 'j':11})

    def test_check_passability_1(self):
        self.play_layer.add(self.mob1)
        self.play_layer.mobs.append(self.mob1)
        self.assertFalse(self.play_layer.check_passability(-1,0))

    def test_check_passability_2(self):
        self.assertTrue(self.play_layer.check_passability(-1,0))


    def test_check_for_death(self):
        self.assertFalse(self.player.check_for_death())

    def test_check_moves(self):
        self.player.check_moves()
        self.assertEqual(self.player.moves, 0)

    def test_mob_close_combat_check(self):
        self.assertTrue(Monster.close_combat_check(self.mob1,self.player,self.map_layer))

    def test_mob_check_for_death(self):#this mob is a MagicMock
        t = util_starting_stats.Gnoll_hunter
        mob1 = MagicMock(Monster(t.monster_sprite, t, 1))
        mob1.position = (10 + 1) * 50, (len(self.map_layer.map) - 7) * 50
        Monster.__init__(mob1, t.monster_sprite, t, 1)
        self.assertFalse(Monster.check_for_death(mob1, self.player))

    def test_move_if_close_range_1(self):
        self.mob1.position = (10 + 1) * 50, (len(self.map_layer.map) - 7) * 50
        self.play_layer.add(self.mob1)
        self.play_layer.mobs.append(self.mob1)
        self.mob1.move_if_close_range()
        self.assertNotEqual(self.player.health, self.player.max_health)


    @unittest.skip('01.03.2018')
    def test_move_if_close_range_2(self):#no
        self.mob1.position = (9 + 1) * 50, (len(self.map_layer.map) - 7) * 50
        self.play_layer.add(self.mob1)
        self.play_layer.mobs.append(self.mob1)
        self.mob1.move_if_close_range()
        time.sleep(2)
        self.assertEqual(self.mob1.position, ((10+1)*50, (len(self.map_layer.map)-8)*50))


    @unittest.skip('01.03.2018')
    def test_player_move_if_possible_1(self):#no
        self.mob1.position = (9 + 1) * 50, (len(self.map_layer.map) - 7) * 50
        self.play_layer.add(self.mob1)
        self.play_layer.mobs.append(self.mob1)
        self.player.direction = (-1,0)
        self.player.move_if_possible()
        time.sleep(2)
        self.assertEqual(self.player.race_sprite.position, ((11+1)*50, (len(self.map_layer.map)-8)*50))


    @unittest.skip('01.03.2018')
    def test_player_move_if_possible_2(self):#no
        self.mob1.position = (9+1)*50, (len(self.map_layer.map)-7)*50
        self.play_layer.add(self.mob1)
        self.play_layer.mobs.append(self.mob1)
        self.player.direction = (1, 1)
        print(self.player.race_sprite.position)
        self.player.move_if_possible()
        time.sleep(2)
        print(self.player.race_sprite.position)
        self.assertEqual(self.player.race_sprite.position, ((11+1)*50, (len(self.map_layer.map)-9)*50))


    def test_pick_up(self):
        item = items_sceptres.Sceptre(util_starting_stats.Bluefire_sceptre, (7,11))
        inv_layer = self.player.inventory
        inv_layer.add_to_inventory(item)
        self.assertEqual(inv_layer.all_inv[0][0][0], item)

    def test_equip(self):
        item = items_sceptres.Sceptre(util_starting_stats.Bluefire_sceptre, (7, 11))
        self.player.inventory.add_to_inventory(item)
        item.Equip()
        self.assertEqual(self.equip_layer.equipment_dict['long_range_1'][0][0], item)

    def test_unequip(self):
        item = items_sceptres.Sceptre(util_starting_stats.Bluefire_sceptre, (7, 11))
        self.player.inventory.add_to_inventory(item)
        item.Equip()
        item.Unequip()
        self.assertEqual(self.equip_layer.equipment_dict['long_range_1'][0], False)


    '''
    def test_do_after_turn(self):
        pass
        #self.play_layer.add(self.mob1)
        #self.play_layer.mobs.append(self.mob1)
        #self
    '''


if __name__=='__main__':
    main()
