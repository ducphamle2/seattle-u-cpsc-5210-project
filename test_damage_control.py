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

    @parameterized.expand([
        (-1000, 1),
        (0, 10),
        (-0.01, 1),
        (1000, 10),
    ])
    @patch('builtins.print')
    def test_damage_control_process_display_damage_control_report(self, damage_stats: float, expected_call_count: int, mock_print):
        # setup
        damage_stats_list = [0,-0.01,-1000,1000,1,damage_stats,3,4]
        # call the method
        self.game.damage_control_process_display_damage_control_report(damage_stats_list,("foo","foo","foo","foo","foo","foo","foo","foo"))
        # assert
        self.assertEqual(mock_print.call_count, expected_call_count)

    @parameterized.expand([
        (0, 0, 0, False),
        (-0.01, 0,0.1,True),
        (-0.01, 0.99,0.9,True),
        (-0.01, 0.98,0.9,True),
        (-0.01, 1000,0.9,True),
    ])
    def test_damage_control_calculate_damage_sum(self, damage_stats: float, delay_in_repairs_at_base: float, expected_damage_sum: float, expected_is_valid: bool):
        # setup
        damage_stats_list = [damage_stats,0,0,0,0,0,0,0]
        # call the method
        damage_sum, is_valid = self.game.damage_control_calculate_damage_sum(damage_stats_list, delay_in_repairs_at_base)
        # assert
        self.assertEqual(damage_sum, expected_damage_sum)
        self.assertEqual(is_valid, expected_is_valid)



        
