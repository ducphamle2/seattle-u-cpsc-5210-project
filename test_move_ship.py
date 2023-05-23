from superstartrek import World, Game, Point
from unittest import TestCase
import sys 
from unittest.mock import patch
from superstartrek import Game, World
from parameterized import parameterized

class TestShortRangeScan(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()

    @parameterized.expand([
        (Point(0, 0), Point(0,0), Point(0,0), Point(0,0), False),
        (Point(-1, 0), Point(5,0), Point(0,0), Point(0,0), True),
        (Point(-1000, 0), Point(2,0), Point(0,0), Point(0,0), True),
        (Point(7, 0), Point(7,0), Point(7,0), Point(7,0), False),
        (Point(8, 0), Point(2,0), Point(7,0), Point(7,0), True),
        (Point(0, -1), Point(0,-1), Point(0,0), Point(0,0), True),
        (Point(0, -1000), Point(0,2), Point(0,0), Point(0,0), True),
        (Point(0, 7), Point(0,7), Point(0,7), Point(0,7), False),
        (Point(0, 8), Point(0,2), Point(0,7), Point(0,7), True),
    ])
    def test_move_ship_verify_hit_edge_calculating_final_position(self, quadrant: Point, sector: Point, expected_quadrant: Point, expected_sector: Point, expected_hit_edge: bool):
        # Call the method
        hit_edge = self.game.move_ship_verify_hit_edge_calculating_final_position(quadrant, sector)

        # Assertions
        self.assertEqual(hit_edge, expected_hit_edge)
        self.assertEqual(quadrant, expected_quadrant)
        self.assertEqual(sector, expected_sector)

        
