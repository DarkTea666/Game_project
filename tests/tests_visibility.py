import pyglet
from unittest import TestCase, main

from visibility import tile_line, distance, one_octant

class VisibilityTests(TestCase):

    def test_distance2(self):
        self.assertAlmostEqual(distance(5, 8, 2, 4), 5)

    def test_distance1(self):
        self.assertAlmostEqual(distance(0, 0, 1, 1), 2 ** 0.5)

    def test_one_octant(self):
        self.assertEqual(one_octant(0.5, 0.5, 4.5, 1.5), [(0, 0), (1, 0), (2, 1), (3, 1), (4, 1)])

    def test_tile_line0(self):
        self.assertEqual(tile_line(0.5, 2.5, 2.5, 1.5), [(0, 2), (1, 1), (2, 1)])

    def test_tile_line1(self):
        self.assertEqual(tile_line(0.5, 2.5, 1.5, 0.5), [(0, 2), (1, 1), (1, 0)])

    def test_tile_line2(self):
        self.assertEqual(tile_line(2.5, 2.5, 1.5, 0.5), [(2, 2), (1, 1), (1, 0)])

    def test_tile_line3(self):
        self.assertEqual(tile_line(2.5, 2.5, 0.5, 1.5), [(2, 2), (1, 1), (0, 1)])

    def test_tile_line4(self):
        self.assertEqual(tile_line(2.5, 0.5, 0.5, 1.5), [(2, 0), (1, 1), (0, 1)])

    def test_tile_line5(self):
        self.assertEqual(tile_line(2.5, 0.5, 1.5, 2.5), [(2, 0), (1, 1), (1, 2)])

    def test_tile_line6(self):
        self.assertEqual(tile_line(0.5, 0.5, 1.5, 2.5), [(0, 0), (1, 1), (1, 2)])

    def test_tile_line7(self):
       self.assertEqual(tile_line(0.5, 0.5, 2.5, 1.5), [(0, 0), (1, 1), (2, 1)])

    def test_tile_line239(self):
        self.assertEqual(tile_line(8.5, 4.5, 10.5, 5.5), [(8, 4), (9, 5), (10, 5)])

    #def test_


import os
print(os.getcwd())
print(pyglet.resource.path)
if __name__ == '__main__':
    main()
    print(os.getcwd())
    print(pyglet.resource.path)

