import unittest
from unittest import TestCase
from superstartrek import Game
import superstartrek as sst
from basic_structure import Point, QuadrantData
from unittest.mock import patch, MagicMock
from io import StringIO

#python -m unittest test_computer.py

class ComputerTest(TestCase):
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_computer_disabled(self, mock_print, mock_input):
        game = Game()
        game.world.ship.damage_stats[7] = -1
        game.computer()
        mock_print.assert_called_with("COMPUTER DISABLED")