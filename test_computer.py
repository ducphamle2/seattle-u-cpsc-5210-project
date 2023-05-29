import unittest
from unittest import TestCase
from world import World
from superstartrek import Game
import superstartrek as sst
from basic_structure import Point, QuadrantData
from unittest.mock import patch, MagicMock
from io import StringIO

#python -m unittest test_computer.py

class ComputerTest(TestCase):
    
    def setUp(self):
        self.world = World()  # Assuming you have a World class defined
        self.world.ship.damage_stats[7] = 0  # Enable the computer
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_computer_disabled(self, mock_print, mock_input):
        game = Game()
        game.world.ship.damage_stats[7] = -1
        game.computer()
        mock_print.assert_called_with("COMPUTER DISABLED")
        
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['', '-1']
        game = Game()
        game.computer()
        expected_output = (
            "\nFUNCTIONS AVAILABLE FROM LIBRARY-COMPUTER:\n"
            "   0 = CUMULATIVE GALACTIC RECORD\n"
            "   1 = STATUS REPORT\n"
            "   2 = PHOTON TORPEDO DATA\n"
            "   3 = STARBASE NAV DATA\n"
            "   4 = DIRECTION/DISTANCE CALCULATOR\n"
            "   5 = GALAXY 'REGION NAME' MAP\n\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
        
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_2_nb_klingons_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['2', '-1']
        game = Game()
        game.world.quadrant.nb_klingons = 0
        game.computer()
        expected_output = (
            
                        "\nSCIENCE OFFICER SPOCK REPORTS  'SENSORS SHOW NO ENEMY "
                        "SHIPS\n"
                        "                                IN THIS QUADRANT'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
