from superstartrek import Point, Position, World, Ship
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch
from parameterized import parameterized


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


if __name__ == '__main__':
    unittest.main()
