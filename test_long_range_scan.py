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

    @parameterized.expand([
        (-1000, 1),
        (0, 1),
        (0.01, 2),
        (1000, 2),
    ])
    @patch('builtins.print')
    def test_long_range_scan_damage_stats(self, damage_stats: float, expected_call_count: int, mock_print):
        print(damage_stats)
        print(expected_call_count)
        # Setup
        self.game.world.ship.damage_stats[2] = damage_stats
        # Call the method
        self.game.long_range_scan()

        # Assertions
        self.assertGreaterEqual(mock_print.call_count, expected_call_count)
        
