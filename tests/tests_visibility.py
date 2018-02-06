from unittest import TestCase, main


class VisibilityTests(TestCase):
    def test_distance(self):
        self.assertAlmostEqual(distance(0,0,1,1), 2**0.5)