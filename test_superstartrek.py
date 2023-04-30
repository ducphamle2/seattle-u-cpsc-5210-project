import unittest
import sys
from superstartrek import Point, Position, Ship
from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized
from superstartrek import Ship
from io import StringIO

class TestingShip(TestCase):

    def test_ship_refill(self):
        ship = Ship()
        ship.refill()
        self.assertEqual(ship.energy_capacity, 3000)
        self.assertEqual(ship.torpedo_capacity, 10)

    @parameterized.expand([
        ("energy_greater_than_0_nominal", 1500, 1490),
        ("energy_equal_0_on_boundary", 2990, 0), 
        ("energy_smaller_0_off_boundary_lower", 2991, 0),
    ])
    def test_manuver_energy_energy_value(self, __name__, n, expected_energy):
        # fixture
        ship = Ship()
        # mock max value to always return the shields so we dont need to care about comparing with zero
        ship.maneuver_energy(n)
        self.assertEqual(ship.energy, expected_energy)

    @parameterized.expand([
        ("energy_smaller_0_shield_greater_than_0_should_not_return_0", 2990, 1, 1),
        ("energy_smaller_0_shield_equal_to_0_should_return_0", 2990, 0, 0),
        ("energy_smaller_0_shield_smaller_than_0_should_return_0", 2991, 0, 0),
    ])
    def test_manuver_energy_shield(self, __name__, n, shield_value, expected_shield):
        # fixture
        ship = Ship()
        ship.shields = shield_value
        # mock max value to always return the shields so we dont need to care about comparing with zero
        ship.maneuver_energy(n)
        self.assertEqual(ship.shields, expected_shield)
        
        
    @patch('star_trek_game.fnr', return_value=4)
    def ship_initializer(self):
        
        expected_devices = ("WARP ENGINES",
            "SHORT RANGE SENSORS",
            "LONG RANGE SENSORS",
            "PHASER CONTROL",
            "PHOTON TUBES",
            "DAMAGE CONTROL",
            "SHIELD CONTROL",
            "LIBRARY-COMPUTER",)
        
        ship = Ship()
        self.assertEqual(ship.position, Position(Point(4, 4), Point(4, 4)))
        self.assertEqual(ship.energy, 3000)
        self.assertEqual(ship.torpedoes, 10)
        self.assertEqual(ship.docked, False)
        self.assertEqual(ship.devices, expected_devices)
        self.assertEqual(ship.damage_stats, [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(ship.shields, 0)

    @parameterized.expand([
        ('shields_input_greater_than_0_valid', '1', 1),
        ('shields_input_smaller_than_energy_plus_shields_valid','100', 100),   
        ('shields_valid_value','50', 50),         
    ])
    def test_shield_control_shields_valid_input(self, __name__, input_value, expected_shields):
        ship = Ship()
        initial_energy = 101  #energy start value, considered as an upper boundary for shields 
        ship.energy = initial_energy
        initial_shileds = ship.shields
        
        with patch('builtins.input', return_value=input_value):
            with StringIO() as buffer:
                sys.stdout = buffer
                ship.shield_control()
                output = buffer.getvalue()

                assert ship.energy == initial_energy + initial_shileds - int(input_value)
                assert expected_shields == ship.shields

                assert "DEFLECTOR CONTROL ROOM REPORT:" in output
                assert f"  'SHIELDS NOW AT {ship.shields} UNITS PER YOUR COMMAND.'" in output

                sys.stdout = sys.__stdout__


    @parameterized.expand([
        ('abc',),
        ('1.2',), 
    ])
    def test_shield_control_raises_value_error_with_invalid_shields_input(self, input_value):
        ship = Ship()
        with patch('builtins.input', return_value=input_value):
            with self.assertRaises(ValueError) as context:
                ship.shield_control()
            
            self.assertEqual(str(context.exception), f"invalid literal for int() with base 10: '{input_value}'")


    def test_shield_control_shields_valid_input_very_large(self):
        ship = Ship()
        initial_energy = 99999999999999999999999999999999999999999999999999999999999999999999999999999999
        initial_shileds = ship.shields
        ship.energy = initial_energy
        # choose x smaller than initial_energy so it would be valid
        x = '99999999999999999999999999999999999999999999999999999999999999999999999999999998'
        x_int = int(x)
        with patch('builtins.input', return_value=x):
                ship.shield_control()

                assert ship.shields == x_int
                assert ship.energy == initial_energy + initial_shileds - x_int


if __name__ == '__main__':
    unittest.main()

