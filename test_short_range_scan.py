from unittest import TestCase
from unittest.mock import patch
from world import World
from superstartrek import Game
from basic_structure import Entity, Position, Point
from ship import Ship
import quadrant
from io import StringIO
from unittest import mock

class TestShortRangeScan(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()
        self.ship = Ship()
        
    @patch('builtins.print')
    def test_short_range_scan_docked(self, mock_print):
        # Setup
        self.game.world.ship.docked = True
        self.game.world.quadrant.get_value = lambda x, y: Entity.starbase

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertTrue(self.game.world.ship.docked)
        self.assertEqual(self.game.world.ship.shields, 0)
        self.assertEqual(mock_print.call_count, 11)
        
    @patch('builtins.print')
    def test_short_range_scan_red(self, mock_print):
        # Setup
        self.game.world.quadrant.nb_klingons = -1
        self.game.world.quadrant.get_value = lambda x, y: Entity.void

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertEqual(mock_print.call_count, 10)
        
    @patch('builtins.print')
    def test_short_range_scan_yellow(self, mock_print):
        # Setup
        self.game.world.ship.energy = 100
        self.game.world.quadrant.nb_klingons = 0
        self.game.world.quadrant.get_value = lambda x, y: Entity.void

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertEqual(mock_print.call_count, 10)
        
    @patch('builtins.print')
    def test_short_range_scan_green(self, mock_print):
        # Setup
        self.game.world.ship.energy = 100
        self.game.world.quadrant.nb_klingons = 0
        self.game.world.quadrant.get_value = lambda x, y: Entity.void

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertEqual(mock_print.call_count, 10)

    @patch('builtins.print')
    def test_short_range_scan_sensors_out(self, mock_print):
        # Setup
        self.game.world.ship.damage_stats[1] = -1
        self.game.world.quadrant.get_value = lambda x, y: Entity.void

        # Call the method
        self.game.short_range_scan()

        # Assertions
        mock_print.assert_called_with('\n*** SHORT RANGE SENSORS ARE OUT ***\n')
