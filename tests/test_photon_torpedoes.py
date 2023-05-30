import unittest
from unittest.mock import patch
from superstartrek import Game, Entity, QuadrantData
from basic_structure import Point, Position, KlingonShip
from ship import Ship
from world import World
from quadrant import Quadrant
from parameterized import parameterized

class TestPhotonTorpedoes(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.world = World()
        self.game.ship = Ship()
        self.game.world.quadrant = Quadrant(Point(0, 0), QuadrantData(0, 0, 0), Position(Point(0, 0), Point(0, 0)))

    @parameterized.expand([
        (2, 2, Entity.void, [], "TORPEDO MISSED", 0, "1"),
        (2, 2, Entity.klingon, [KlingonShip(Point(2, 2), 100.0)], "*** KLINGON DESTROYED ***", -1, "1"),
        (2, 2, Entity.star, [KlingonShip(Point(2, 2), 100.0)], "STAR AT 3 , 4 ABSORBED TORPEDO ENERGY.", 0, "1"),
        (2, 2, Entity.starbase, [KlingonShip(Point(2, 2), 100.0)], "COURT MARTIAL!", 0, "1"),
        (0, 0, Entity.void, [KlingonShip(Point(2, 2), 100.0)], "ENSIGN CHEKOV REPORTS, 'INCORRECT COURSE DATA, SIR!'", 0, "10"),
    ])
    def test_photon_torpedoes(self, torpedo_x, torpedo_y, value, klingon_ships, expected_output, expected_nb_klingons, cd_input):

        self.game.world.ship.position.sector.x = torpedo_x
        self.game.world.ship.position.sector.y = torpedo_y
        self.game.world.quadrant.set_value(torpedo_x, torpedo_y+1, value)
        self.game.world.quadrant.klingon_ships = klingon_ships
        with patch('builtins.print') as mock_print, patch('builtins.input', return_value=cd_input):
            self.game.photon_torpedoes()
            mock_print.assert_called_with(expected_output)
        self.assertEqual(self.game.world.quadrant.nb_klingons, expected_nb_klingons)

    @patch.object(Game, "end_game", return_value=None)  # Mocking end_game method here
    def test_photon_torpedoes_win_game(self, end_game_mock):

        self.game.world.ship.position.sector.x = 2
        self.game.world.ship.position.sector.y = 2
        self.game.world.quadrant.set_value(2, 3, Entity.klingon)
        self.game.world.quadrant.klingon_ships = 100
        self.game.world.remaining_klingons = 0
        with patch('builtins.print') as mock_print, patch('builtins.input', return_value=1):
            self.game.photon_torpedoes()
            mock_print.assert_called_with("*** KLINGON DESTROYED ***")

        end_game_mock.assert_called_with(won=True, quit=False)
        self.assertEqual(self.game.world.quadrant.nb_klingons, -1)

    @patch.object(Game, "end_game", return_value=None)  # Mocking end_game method here
    def test_photon_torpedoes_lose_game(self, end_game_mock):

        self.game.world.ship.position.sector.x = 2
        self.game.world.ship.position.sector.y = 2
        self.game.world.quadrant.set_value(2, 3, Entity.klingon)
        self.game.world.quadrant.klingon_ships = 100
        self.game.world.remaining_klingons = 0
        with patch('builtins.print') as mock_print, patch('builtins.input', return_value=1):
            self.game.photon_torpedoes()
            mock_print.assert_called_with("*** KLINGON DESTROYED ***")

        end_game_mock.assert_called_with(won=True, quit=False)
        self.assertEqual(self.game.world.quadrant.nb_klingons, -1)
    
    @patch.object(Game, "end_game", return_value=None)  # Mocking end_game method here
    def test_photon_torpedoes_starbase_destroyed(self, end_game_mock):
        self.game.world.ship.position.sector.x = 2
        self.game.world.ship.position.sector.y = 2
        self.game.world.quadrant.get_value = lambda x, y: Entity.starbase  # Mocking get_value() function
        self.game.world.quadrant.nb_bases = 1
        self.game.world.bases_in_galaxy = 1
        self.game.world.remaining_klingons = 0
        self.game.world.stardate = 200
        self.game.world.initial_stardate = 100
        self.game.world.mission_duration = 50
        with patch('builtins.input', return_value='1'):  # Set cd = 1
            with patch('builtins.print') as mock_print:
                self.game.photon_torpedoes()

        mock_print.assert_any_call("*** STARBASE DESTROYED ***")
        mock_print.assert_any_call("THAT DOES IT, CAPTAIN!! YOU ARE HEREBY RELIEVED OF COMMAND")
        mock_print.assert_any_call("AND SENTENCED TO 99 STARDATES AT HARD LABOR ON CYGNUS 12!!")
        self.assertEqual(self.game.world.bases_in_galaxy, 0)
        self.assertFalse(self.game.ship.docked)
        end_game_mock.assert_called_with(won=False)

    def test_photon_torpedoes_all_expended(self):

        self.game.world.ship.torpedoes = 0 

        with patch('builtins.print') as mock_print:
            self.game.photon_torpedoes()

        mock_print.assert_called_once_with("ALL PHOTON TORPEDOES EXPENDED")


    def test_photon_torpedoes_tubes_not_operational(self):
        self.game.world.ship.damage_stats[4] = -1

        with patch('builtins.print') as mock_print:
            self.game.photon_torpedoes()

        mock_print.assert_called_once_with("PHOTON TUBES ARE NOT OPERATIONAL")
