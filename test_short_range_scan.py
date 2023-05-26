from unittest import TestCase
from unittest.mock import patch
from world import World
from superstartrek import Game
from basic_structure import Entity

class TestShortRangeScan(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()
        
    @patch('builtins.print')
    def test_short_range_scan_docked(self, mock_print):
        # Setup
        self.world.ship.docked = True
        self.world.quadrant.get_value = lambda x, y: Entity.starbase if x == 2 and y == 2 else None

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertTrue(self.world.ship.docked)
        self.assertEqual(self.world.ship.shields, 0)
        self.assertEqual(mock_print.call_count, 10)
        
    @patch('builtins.print')
    def test_short_range_scan_red(self, mock_print):
        # Setup
        self.world.quadrant.nb_klingons = 3

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertEqual(mock_print.call_count, 10)
        
    @patch('builtins.print')
    def test_short_range_scan_yellow(self, mock_print):
        # Setup
        self.world.ship.energy = 100
        self.world.quadrant.nb_klingons = 0

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertEqual(mock_print.call_count, 10)
        
    @patch('builtins.print')
    def test_short_range_scan_green(self, mock_print):
        # Setup
        self.world.ship.energy = 100
        self.world.quadrant.nb_klingons = 0

        # Call the method
        self.game.short_range_scan()

        # Assertions
        self.assertEqual(mock_print.call_count, 10)

    @patch('builtins.print')
    def test_short_range_scan_sensors_out(self, mock_print):
        # Setup
        self.world.ship.damage_stats[1] = -1

        # Call the method
        self.game.short_range_scan()

        # Assertions
        mock_print.assert_called_with('---------------------------------')
