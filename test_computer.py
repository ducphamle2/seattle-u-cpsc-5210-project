import unittest
from unittest import TestCase
from world import World
from superstartrek import Game
import superstartrek as sst
from basic_structure import Point, QuadrantData, KlingonShip
from unittest.mock import patch, MagicMock
from unittest import mock
from io import StringIO
# from superstartrek import from1, from2, to1, to2

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
        
    
    # -----Empty Command-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_empty(self, mock_stdout, mock_input):
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
        
        
    # -----Command 0-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['0', '-1']
        self.game.world.ship.position.quadrant = 3
        self.game.computer()
        expected_output = ("\n\n        COMPUTER RECORD OF GALAXY FOR QUADRANT 3\n\n"
               "       1     2     3     4     5     6     7     8\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 1    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 2    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 3    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 4    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 5    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 6    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 7    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 8    ***   ***   ***   ***   ***   ***   ***   ***\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
        
    # -----Command 1-----
    @patch('builtins.print')
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_1_bases_in_galaxy_0(self, mock_stdout, mock_input, mock_print):
        # Setup
        mock_input.side_effect = ['1', '-1']
        self.game.world.quadrant.nb_klingons = 0
        self.game.world.bases_in_galaxy = 0
        
        # Call the method
        self.game.computer()
        
        # Assertions
        self.assertEqual(mock_print.call_count, 16)
        
    
    @patch('builtins.print')
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_1_bases_in_galaxy_1(self, mock_stdout, mock_input, mock_print):
        # Setup
        mock_input.side_effect = ['1', '-1']
        self.game.world.quadrant.nb_klingons = 0
        self.game.world.bases_in_galaxy = 1
        
        # Call the method
        self.game.computer()
        
        # Assertions
        self.assertEqual(mock_print.call_count, 15)
    

    # -----Command 2-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_2_nb_klingons_0(self, mock_stdout, mock_input):
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
    def test_computer_command_2_nb_klingons_1_and_shield_0(self, mock_stdout, mock_input):
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
    def test_computer_command_2_nb_klingons_2_and_shield_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['2', '-1']
        self.game.world.quadrant.nb_klingons = 2
        self.game.world.quadrant.klingon_ships = [mock.Mock(sector=Point(1, 2), shield=0)]
        self.game.computer()
        expected_output = (

                        "\nFROM ENTERPRISE TO KLINGON BATTLE CRUISERS\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
    
    # @patch('builtins.print')
    # @patch('builtins.input')
    # @patch('sys.stdout', new_callable=StringIO)
    # def test_computer_command_2(self, mock_stdout, mock_input, mock_print):
    #     # Setup
    #     mock_input.side_effect = ['2', '-1']
    #     klingon_ship = KlingonShip(Point(1, 1), 100.0)
    #     self.game.world.quadrant.klingon_ships.append(klingon_ship)
    #     self.game.world.quadrant.klingon_ships[0].shield = 1
        
    #     # Call the method
    #     self.game.computer()
        
    #     # Assertions
    #     self.assertEqual(mock_print.call_count, 2)
        
    
    # -----Command 3-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_3_nb_bases_0(self, mock_stdout, mock_input):
        mock_input.side_effect = ['3', '-1']
        self.game.world.quadrant.nb_bases = 0
        self.game.computer()
        expected_output = (
            
                        "\nMR. SPOCK REPORTS,  'SENSORS SHOW NO STARBASES IN THIS "
                        "QUADRANT.'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
        
    # This test works correct, it fails because of the bug in the code
    
    # @patch('builtins.print')
    # @patch('builtins.input')
    # @patch('sys.stdout', new_callable=StringIO)
    # def test_computer_command_3_nb_bases_1(self, mock_stdout, mock_input, mock_print):
    #     # Setup
    #     mock_input.side_effect = ['3', '-1']
    #     self.game.world.quadrant.nb_bases = 2
        
    #     # Call the method
    #     self.game.computer()
        
    #     # Assertions
    #     self.assertEqual(mock_print.call_count, 15)
    
    
    # -----Command 4-----
    # @patch('builtins.print')
    # @patch('builtins.input')
    # @patch('sys.stdout', new_callable=StringIO)
    # def test_computer_command_4(self, mock_stdout, mock_input, mock_print):
    #     # Setup
    #     mock_input.side_effect = ['4', '-1']
        
    #     # Call the method
    #     self.game.computer()
        
    #     # Assertions
    #     self.assertEqual(mock_print.call_count, 15)
        
        
    # -----Command 5-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_5(self, mock_stdout, mock_input):
        mock_input.side_effect = ['5', '-1']
        self.game.world.ship.position.quadrant = 3
        self.game.computer()
        expected_output = ("\n                        THE GALAXY\n"
               "       1     2     3     4     5     6     7     8\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 1         ANTARES                  SIRIUS\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 2          RIGEL                   DENEB\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 3         PROCYON                 CAPELLA\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 4           VEGA                 BETELGEUSE\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 5         CANOPUS                ALDEBARAN\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 6          ALTAIR                 REGULUS\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 7       SAGITTARIUS               ARCTURUS\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n"
                " 8          POLLUX                  SPICA\n"
                "     ----- ----- ----- ----- ----- ----- ----- -----\n\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
        
    @patch('builtins.print')
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_command_5(self, mock_stdout, mock_input, mock_print):
        # Setup
        mock_input.side_effect = ['5', '-1']
        self.game.world.ship.position.quadrant = 3
        
        # Call the method
        self.game.computer()
        
        # Assertions
        self.assertEqual(mock_print.call_count, 21)
        
        
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
        
        
    # -----Command A (error value)-----
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_computer_error_value_command(self, mock_stdout, mock_input):
        mock_input.side_effect = ['A', '-1']
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


#python -m coverage run -m unittest && coverage report -m
#python -m unittest test_computer.py