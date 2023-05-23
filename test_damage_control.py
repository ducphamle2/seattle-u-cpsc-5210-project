from superstartrek import World, Game
from unittest import TestCase
import sys 
from unittest.mock import patch
from superstartrek import Game, World
from parameterized import parameterized

class TestShortRangeScan(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()


    def test_damage_control_reset_damage_stats(self):
        # Setup
        damage_stats_list = [0,-0.01,-1000,1000,1,2,3,4]
        # Call the method
        self.game.damage_control_reset_damage_stats(damage_stats_list)

        # Assertions
        self.assertEqual(damage_stats_list, [0, 0, 0, 1000,1,2,3,4])
        
