from unittest import TestCase, main
from unittest.mock import MagicMock

from cocos.scene import Scene
from cocos import layer, scene
from cocos.scenes import *
from cocos.director import director

import random

from main_scene import *
from algorithms.algorithms_visibility import tile_line_vis, calculate_visibility
from algorithms.algorithms_pathfinding import tile_score, in_list, find_min_score,\
    tile_do, pathfind_to_target, trace_back_path

class TestAlgorithm(TestCase):
    def setUp(self):
        self.window = director.init(width=1250, height=800, autoscale=True, resizable=True, visible=False)

        self.player = Player(starting_stats.Human, starting_stats.Warlock)

        random.seed(666)
        self.map_layer = LevelMap(1)
        self.map_layer.generate_map()

        self.play_layer = PlayingLayer(self.player, self.map_layer, subj1=self.player)

        main_scene = FirstScene()

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

    def test_tile_line_vis_1(self):
        self.assertEqual(tile_line_vis(11, 7, 5, 3, self.map_layer), [(7, 11), (6, 10), (6, 9), (5, 8), (4, 7)])

    def test_tile_line_vis_2(self):
        self.assertEqual(tile_line_vis(13, 9, 12, 1, self.map_layer),  [(9, 13),(8, 13),(7, 13),(6, 13),(5, 12),(4, 12),(3, 12),(2, 12),(1, 12)])

    def test_calculate_visibility(self):
        self.assertEqual(calculate_visibility(7, 11, self.map_layer), [['#', '#', '#', '#', '#', '#', 1, 1, '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', 1, 0, 0, '#', '#', '#', '#', 1, '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', 0, 0, '#', '#', '#', 0, 1, 1, '#', '#', '#', '#', 1, 1, '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', 1, 0, 0, '#', '#', 0, 0, 1, '#', 1, 0, 0, 0, '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', 1, 0, 0, 1, 1, 0, 0, '#', 0, 0, 0, 0, 1, '#', 0, 1, '#'], ['#', '#', '#', '#', '#', '#', '#', 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', 'f', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', 1, 0, 0, 0, 0, 0, 0, 0, 1, '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', 1, 0, 0, 0, '#', 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1], ['#', '#', '#', '#', '#', '#', '#', 1, 0, 0, '#', '#', '#', 0, 0, 1, '#', '#', '#', '#', '#', 0, 0, 1], ['#', '#', '#', '#', '#', '#', '#', 1, 1, 1, '#', '#', '#', 0, 0, 0, 1, '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 0, 0, 1, '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 1, 1, 1, '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']])

    def test_tile_score_1(self):
        self.assertEqual(tile_score(self.map_layer, 7,11,4,4), {'i': 7, 'j': 11, 'value': 0, 'g': 0, 'h': 7})

    def test_tile_score_2(self):
        self.assertEqual(tile_score(self.map_layer, 8,1,12,18), {'i': 8, 'j': 1, 'value': 1, 'g': 0, 'h': 17})

    def test_pathfnd_to_target(self):
        self.map_layer.mark()
        self.assertEqual(pathfind_to_target(self.map_layer, 8, 11, 12, 19, []), [(8,12), (8,13), (8,14), (8,15),
                                                            (8,16), (9,17), (10,18), (11,19), (12,19)])
    def test_pathfnd_to_target(self):
        self.assertEqual(pathfind_to_target(self.map_layer, 8, 11, 12, 19, [(9,12), (9,11), (9,10), (8,10), (7,10),
                                                                            (7,11), (7,12), (8,12)]),[])

if __name__ == '__main__':
    unittest.main()