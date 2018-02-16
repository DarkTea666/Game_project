"""
assert(pathfind_to_target(map_layer, 7, 11, 9, 13,
                          play_layer.mobs)==[(8, 12), (9, 13)])
assert(pathfind_to_target(map_layer, 7, 11, 6, 10,
                          play_layer.mobs)==[(6, 10)])
assert(map_layer.neighbors(7,11)==[0,0,0,0,0,0,0,0])
"""
import pyglet
from unittest import TestCase, main
from Main_program import *
from main_scene import *

class TestPassability(TestCase):
    def setUp(self):
        self.window = director.init(width=1250, height=800, autoscale=True, resizable=True, visible=False)
        player1 = Player(starting_stats.Human,starting_stats.Warlock)

        self.map_layer = LevelMap(1)
        self.map_layer.generate_map()

        self.play_layer = PlayingLayer(player1, self.map_layer)
        self.play_layer.spawn_initial_mobs()
        
        main_scene = MainScene()

    def tearDown(self):
        self.window.close()

    def test_check_passability_1_1(self):
        self.assertTrue(self.play_layer.check_passability(0,0))

    def test_check_passability_2_1(self):
        self.assertTrue(self.play_layer.check_passability(-1,1))

    def test_check_for_death(self):
        self.assertFalse(self.play_layer.player.check_for_death())

    def test_check_tile_for_mob(self):
        self.assertTrue(self.play_layer.check_tile_for_mob(1,1))

    def test_in_bounds(self):
        self.assertFalse(self.map_layer.in_bounds(-1,80))



if __name__=='__main__':
    main()
