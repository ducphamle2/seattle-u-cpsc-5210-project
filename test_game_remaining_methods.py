from unittest import TestCase
from superstartrek import Game
from unittest.mock import patch
from parameterized import parameterized

class TestGameRemainingMethods(TestCase):

    def setUp(self):
        self.game = Game()


    @patch('superstartrek.print')
    def test_startup(self, print_mock):
        self.game.startup()
        self.assertTrue(print_mock.called)

    @patch('superstartrek.print')
    def test_new_quadrant_world_stardate_equal_to_initial_stardate(self, print_mock):
        self.game.new_quadrant()
        self.assertTrue(print_mock.called)
    
    @parameterized.expand([
        (120),
        (200),
        (-5000)
    ])
    @patch('superstartrek.print')
    def test_new_quadrant_ship_shields_less_than_equal_to_200(self, shields_value, print_mock):
        self.game.world.ship.shields = shields_value
        self.game.new_quadrant()
        print_mock.assert_called
        
