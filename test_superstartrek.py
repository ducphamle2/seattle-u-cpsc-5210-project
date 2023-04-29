from superstartrek import World, Ship
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
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


if __name__ == '__main__':
    unittest.main()
