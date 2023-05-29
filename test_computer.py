import unittest
from unittest import TestCase
from world import World
from superstartrek import Game
import superstartrek as sst
from basic_structure import Point, QuadrantData
from unittest.mock import patch, MagicMock
from unittest import mock
from io import StringIO

class ComputerTest(TestCase):
    
    def setUp(self):
        self.game = Game()
        self.world = World()
        self.world.ship.damage_stats[7] = 0
    
    # -----Computer Disabled-----
    @patch('builtins.input')
    @patch('builtins.print')
    def test_computer_disabled(self, mock_print, mock_input):
        self.game.world.ship.damage_stats[7] = -1
        self.game.computer()
        mock_print.assert_called_with("COMPUTER DISABLED")
        
    
    # -----Command 0-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['', '-1']
        self.game.computer()
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
        
        
    # -----Command 1-----
    

    # -----Command 2-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_2_nb_klingons_equalTo_zero(self, mock_stdout, mock_input):
        mock_input.side_effect = ['2', '-1']
        self.game.world.quadrant.nb_klingons = 0
        self.game.computer()
        expected_output = (
            
                        "\nSCIENCE OFFICER SPOCK REPORTS  'SENSORS SHOW NO ENEMY "
                        "SHIPS\n"
                        "                                IN THIS QUADRANT'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_2_nb_klingons_equalTo_one_and_shield_equalTo_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['2', '-1']
        self.game.world.quadrant.nb_klingons = 1
        self.game.world.quadrant.klingon_ships = [mock.Mock(sector=Point(1, 2), shield=0)]
        self.game.computer()
        expected_output = (
            
                        "\nFROM ENTERPRISE TO KLINGON BATTLE CRUISER\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
        
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_2_nb_klingons_equalTo_two_and_shield_equalTo_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['2', '-1']
        self.game.world.quadrant.nb_klingons = 2
        self.game.world.quadrant.klingon_ships = [mock.Mock(sector=Point(1, 2), shield=0)]
        self.game.computer()
        expected_output = (

                        "\nFROM ENTERPRISE TO KLINGON BATTLE CRUISERS\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
    
    # -----Command 3-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_3_nb_bases_equalTo_zero(self, mock_stdout, mock_input):
        mock_input.side_effect = ['3', '-1']
        self.game.world.quadrant.nb_bases = 0
        self.game.computer()
        expected_output = (
            
                        "\nMR. SPOCK REPORTS,  'SENSORS SHOW NO STARBASES IN THIS "
                        "QUADRANT.'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
        
    # -----Command 10 (else condition)-----
    @mock.patch('builtins.input')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_10_else_condition(self, mock_stdout, mock_input):
        mock_input.side_effect = ['10', '-1']
        self.game.computer()
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
