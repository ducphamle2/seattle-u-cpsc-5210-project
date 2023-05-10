import unittest
import sys
from superstartrek import Point, Position, Ship
from unittest import TestCase
from unittest.mock import MagicMock
import sys 
from unittest.mock import patch
from parameterized import parameterized
from superstartrek import Ship, Game, World
from io import StringIO

class PhaserControlTest(TestCase):

    @parameterized.expand([
        ("ship_damage_less_than_0_returns_false", -1, False),
        ("ship_damage_equal_0_returns_true", 0, True),
        ("ship_damage_greater_than_0_returns_true", 10, True),
    ])
    def test_check_phasers_operational(self, __name__, ship_damage, expected_result):
        game = Game()
        ship = Ship()
        ship.damage_stats[3] = ship_damage
        assert game.check_phasers_operational(ship) == expected_result


    @parameterized.expand([
        ("no_klingons_returns_true_when_klingons_negative", -1, True),
        ("no_klingons_returns_true_when_klingons_zero", 0, True),
        ("no_klingons_returns_false_when_klingons_exist", 10, False),
    ])
    def test_check_no_klingons(self, __name__, nb_klingons, expected_result):
        game = Game()
        world = World()
        world.quadrant.nb_klingons = nb_klingons
        assert game.check_no_klingons(world) == expected_result

