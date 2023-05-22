from superstartrek import World, Game, Ship, Point, KlingonShip
from unittest import TestCase
import sys 
from unittest.mock import patch
from parameterized import parameterized
from superstartrek import Ship, Game, World

# @patch('superstartrek.Game.fnd')
# @patch('superstartrek.fnr')
class TestKlingonsFire(TestCase):
    def setUp(self):
        self.game = Game()  # Initialize an instance of game
        self.ship = Ship()  # Initialize an instance of ship
        self.world = World()  # Initialize an instance of World

    def test_no_klingons_in_quadrant(self):
        """Test when there are no Klingons in the quadrant."""
        initial_shields = self.ship.shields
        self.world.quadrant.nb_klingons = 0
        self.game.klingons_fire()
        self.assertEqual(self.ship.shields, initial_shields)

    def test_ship_docked(self):
        """Test when the ship is docked."""
        self.ship.docked = True
        initial_shields = self.ship.shields
        self.world.quadrant.nb_klingons = 5
        self.game.klingons_fire()
        self.assertEqual(self.ship.shields, initial_shields)

    # @patch('random.random')
    # @patch.object(Game, "end_game")
    # def test_klingons_fire_on_ship(self, mock_end_game, mock_random):
    #     """Test when Klingons fire on the ship."""
    #     initial_shields = self.ship.shields
    #     mock_random.return_value = 0.5
    #     self.world.quadrant.nb_klingons = 5
    #     klingon_ship = KlingonShip(Point(1, 1), 100)
    #     self.world.quadrant.klingon_ships.append(klingon_ship)
    #     self.game.world = self.world
    #     self.game.ship = self.ship
    #     self.game.klingons_fire()
    #     self.assertNotEqual(self.ship.shields, initial_shields)
    #     mock_end_game.assert_called_with(won=False, quit=False, enterprise_killed=True)

    # @patch('random.random')
    # def test_klingons_fire_destroy_ship(self, mock_random, mock_fnd, mock_fnr):
    #     """Test when Klingons fire and destroy the ship."""
    #     mock_random.return_value = 0.5
    #     mock_fnd.return_value = 2000  # Large number to ensure the ship will be destroyed
    #     mock_fnr.return_value = 0
    #     self.world.quadrant.nb_klingons = 5
    #     klingon_ship = KlingonShip(Point(1, 1), 100)
    #     self.world.quadrant.klingon_ships.append(klingon_ship)
    #     self.game.klingons_fire()
