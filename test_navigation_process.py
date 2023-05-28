from world import World
from ship import Ship
from superstartrek import Game
from quadrant import Quadrant
from basic_structure import Point, QuadrantData, KlingonShip, Entity
from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from parameterized import parameterized
import helper

class TestNavigationProcess(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()
        self.ship = self.world.ship

    @parameterized.expand([
        (0, 2.5, 2.5),
        (0.5, 5.8, 6.3),
        (-3, 92.5, 89.5)
    ])
    def test_navigation_calculate_world_stardate_warp_less_than_1(self, warp_value, stardate_value, expected_result):
        actual_result = self.game.navigation_calculate_world_stardate(warp_value, stardate_value)
        self.assertEqual(expected_result, actual_result)
    
    @parameterized.expand([
        (1, 6.2, 7.2),
        (200, 78.5, 79.5),
        (52.75, 0, 1)
    ])
    def test_navigation_calculate_world_stardate_warp_greater_than_equal_to_1(self, warp_value, stardate_value, expected_result):
        actual_result = self.game.navigation_calculate_world_stardate(warp_value, stardate_value)
        self.assertEqual(expected_result, actual_result)

        
    @patch.object(Quadrant, 'set_value')
    def test_navigation_klingon_ship_move(self, mock):
        for klingon_ship in self.world.quadrant.klingon_ships:
            klingon_ship.shield = 10 # value not equal to zero
        self.game.navigation_klingon_ship_move(self.world.quadrant, self.world.quadrant.klingon_ships)
        self.assertFalse(mock.called)

    

        




        
    
    
    
    

    

    