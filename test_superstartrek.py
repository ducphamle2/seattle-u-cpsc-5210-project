from superstartrek import World, Ship
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
import sys 
import io
from parameterized import parameterized
from unittest.mock import patch


class TestingShip(TestCase):

    def test_ship_refill(self):
        ship = Ship()
        ship.refill()
        self.assertEqual(ship.energy_capacity, 3000)
        self.assertEqual(ship.torpedo_capacity, 10)

    @parameterized.expand([
        ("energy_greater_than_0_nominal", 1500, 0, 1490, 0),
        ("energy_equal_0_on_boundary", 2990, 0, 0, 0), 
        ("energy_smaller_0_off_boundary_lower", 3000, 0, 0, 0),
        # ("energy_smaller_0_off_boundary_lower_shield_test", 3000, 0, 0, 0),
    ])
    def test_manuver_energy(self, __name__, n, shield_value, expected_energy, expected_shield):
        ship = Ship()
        ship.shields = shield_value
        ship.maneuver_energy(n)
        self.assertEqual(ship.energy, expected_energy)
        self.assertEqual(ship.shields, expected_shield)

    
    @parameterized.expand([
        ("damage_stats[6]_equals_minus_1_on_boundary", -1),
        ("damage_stats[6]_equals_minus_10_off_boundary_lower", -10)
    ])
    def test_shield_control_damage_stats_6_less_than_0(self, __name__, damage_stats):
        ship = Ship()
        ship.damage_stats[6] = damage_stats
        captured_output = io.StringIO()                  # Create StringIO object
        sys.stdout = captured_output                     #  and redirect stdout.
        ship.shield_control()                                  # Call function.
        sys.stdout = sys.__stdout__                     # Reset redirect.
        self.assertEqual(captured_output.getvalue(), 'SHIELD CONTROL INOPERABLE\n')
    
    @parameterized.expand([
        ("input_energy_value_minus_50_off_boundary_lower", '-50'),
        ("input_energy_value_minus_1_on_boundary", '-1')
    ])
    def test_shield_control_x_less_than_zero(self, __name__, input_value):
        ship = Ship()
        ship.damage_stats[6] = 6 # damage_stats[6] must have a positive value for this test.
        captured_output = io.StringIO()                  # Create StringIO object
        sys.stdout = captured_output        
        with patch('builtins.input', return_value=input_value):
            ship.shield_control()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), '<SHIELDS UNCHANGED>\n')
    
    def test_shield_control_shields_equals_x(self):
        ship = Ship()
        ship.damage_stats[6] = 6 #damage stats must be positive for this test
        ship.shields = 265
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='265'):
            ship.shield_control()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), '<SHIELDS UNCHANGED>\n')

    def test_shield_control_x_greater_than_energy_plus_shields(self):
        ship = Ship()
        ship.damage_stats[6] = 6 # damage stats must be positive for this test
        ship.shields = 300
        ship.energy = 500
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='1000'):
            ship.shield_control()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "SHIELD CONTROL REPORTS  'THIS IS NOT THE FEDERATION "
                "TREASURY.'\n"
                "<SHIELDS UNCHANGED>\n")   

if __name__ == '__main__':
    unittest.main()
