import itertools
from world import World
from ship import Ship
from superstartrek import Game
from basic_structure import Point, KlingonShip
from unittest import TestCase
from unittest.mock import patch

class TestKlingonsFire(TestCase):
    def setUp(self):
        self.game = Game()  # Initialize an instance of game
        self.ship = Ship()  # Initialize an instance of ship
        self.world = World()  # Initialize an instance of World

    @patch.object(Game, "end_game", return_value=None)  # Mocking end_game method here
    def test_no_klingons_in_quadrant(self, mock_end_game):
        """Test when there are no Klingons in the quadrant."""
        initial_shields = self.ship.shields
        self.world.quadrant.nb_klingons = 0
        self.game.klingons_fire()
        self.assertEqual(self.ship.shields, initial_shields)

    @patch.object(Game, "end_game", return_value=None)  # Mocking end_game method here
    def test_ship_docked(self, mock_end_game):
        """Test when the ship is docked."""
        self.ship.docked = True
        initial_shields = self.ship.shields
        self.world.quadrant.nb_klingons = 5
        self.game.klingons_fire()
        self.assertEqual(self.ship.shields, initial_shields)

    @patch('superstartrek.Game.get_h')
    @patch.object(Game, "end_game")
    def test_klingons_fire_on_ship_destroyed(self, mock_end_game, mock_get_h):
        """Test when Klingons fire on the ship."""
        self.ship.shields = 100  # Initialize the ship's shields to 100
        initial_shields = self.ship.shields
        mock_get_h.return_value = 100 
        self.world.quadrant.nb_klingons = 5
        klingon_ship = KlingonShip(Point(1, 1), 100.0)
        self.world.quadrant.klingon_ships.append(klingon_ship)
        self.game.world = self.world
        self.world.ship = self.ship
        self.game.ship = self.ship
        self.game.klingons_fire()
        self.assertNotEqual(self.game.ship.shields, initial_shields)
        self.assertEqual(self.game.ship.shields, 0)
        mock_end_game.assert_called_with(won=False, quit=False, enterprise_killed=True)

    @patch('superstartrek.Game.get_h')
    @patch('random.random')
    @patch.object(Game, "end_game")
    def test_damage_to_ship(self, mock_end_game, mock_random, mock_get_h):
        """Test damage to ship's device."""
        self.ship.shields = 1000  # Initialize the ship's shields to 1000 to ensure h/ship.shields > 0.02
        initial_device_damage = self.ship.damage_stats.copy()  # Copy the initial damage stats
        mock_random.side_effect = itertools.cycle([0.5, 0.3])
        self.world.quadrant.nb_klingons = 1
        klingon_ship = KlingonShip(Point(1, 1), 100.0)
        self.world.quadrant.klingon_ships.append(klingon_ship)
        self.game.world = self.world
        self.world.ship = self.ship
        self.game.ship = self.ship
        mock_get_h.return_value = 25 
        self.game.klingons_fire() 
        self.assertNotEqual(self.game.ship.damage_stats, initial_device_damage)  # Check that the damage stats have changed
        