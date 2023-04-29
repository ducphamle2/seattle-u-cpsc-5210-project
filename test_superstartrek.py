from superstartrek import World, Ship
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


if __name__ == '__main__':
    unittest.main()
