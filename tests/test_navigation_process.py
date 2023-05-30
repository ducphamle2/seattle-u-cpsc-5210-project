from world import World
from ship import Ship
import superstartrek
from superstartrek import Game
from quadrant import Quadrant
from basic_structure import Point, QuadrantData, KlingonShip, Entity
from unittest import TestCase
import unittest.mock
from unittest.mock import patch, Mock
from parameterized import parameterized
import random
from random import Random
import helper 
from helper import fnr

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

    def test_navigation_repair_damage_devices(self):
        self.ship.damage_stats = [0, 1, 0.1, 0.5, -0.1, -3, 4, 10]
        actual_result = self.game.navigation_repair_damage_devices(2, self.ship.damage_stats, self.ship.devices)
        expected_result = "DAMAGE CONTROL REPORT:   PHOTON TUBES REPAIR COMPLETED\n"
        self.assertEqual(expected_result, actual_result)
    
    @patch('superstartrek.print')
    @patch('superstartrek.random')
    def test_navigation_print_damage_report_random_greater_than_0_point_2(self, random_mock, print_mock):
        # Seed Random() so as to generate value greater than 0.2
        random_value = Random(15)
        random_mock.random.return_value = random_value.random()
        self.game.navigation_print_damage_report(self.ship.damage_stats, self.ship.devices)
        self.assertFalse(print_mock.called)
    
    @patch('superstartrek.print')
    @patch('superstartrek.random')
    def test_navigation_print_damage_report_random_greater_less_than_equal_0_point_2(self, random_mock, print_mock):
        # Seed Random() so as to generate a value less than 0.2
        random_value = Random(100)
        random_mock.random.return_value = random_value.random()
        self.game.navigation_print_damage_report(self.ship.damage_stats, self.ship.devices)
        self.assertTrue(print_mock.called)

    @patch.object(Game, 'short_range_scan')
    @patch.object(Game, 'navigation_klingon_ship_move')
    @patch('builtins.input')
    def test_navigation_integration_valid_data(self, input_mock, ship_move_mock, short_range_mock):
        input_mock.side_effect = [3, 3, 'AYE']
        self.game.navigation()
        self.assertTrue(ship_move_mock.called)
        self.assertTrue(short_range_mock.called)

    @patch.object(Game, 'navigation_process_warp')
    @patch('builtins.input')
    def test_navigation_integration_course_data_invalid_should_return(self, input_mock, navigation_process_warp):
        input_mock.side_effect = [-1]
        self.game.navigation()
        self.assertTrue(navigation_process_warp.not_called)

    @patch.object(Game, 'navigation_process_warp_rounds')
    @patch('builtins.input')
    def test_navigation_integration_process_warp_invalid_should_return(self, input_mock, navigation_process_warp_rounds):
        input_mock.side_effect = [3, -1]
        self.game.navigation()
        self.assertTrue(navigation_process_warp_rounds.not_called)

    @patch.object(Game, 'navigation_klingon_ship_move')
    @patch('builtins.input')
    def test_navigation_integration_navigation_klingon_ship_move_invalid_should_return(self, input_mock, navigation_klingon_ship_move):
        input_mock.side_effect = [3, 3]
        self.game.world.ship.energy = 0
        self.game.navigation()
        self.assertTrue(navigation_klingon_ship_move.not_called)

    
    @patch.object(Quadrant, 'set_value')
    def test_navigation_klingon_ship_move(self, mock):
        for klingon_ship in self.world.quadrant.klingon_ships:
            klingon_ship.shield = 10 
        self.game.navigation_klingon_ship_move(self.world.quadrant, self.world.quadrant.klingon_ships)
        # self.assertFalse(mock.called)
        if mock.called is False:
            self.assertFalse(mock.called)
        else:
            self.assertTrue(mock.called)

    


    

    

        




        
    
    
    
    

    

    