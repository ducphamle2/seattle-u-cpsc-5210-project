from unittest import TestCase
from superstartrek import Game
from unittest.mock import patch

class TestGameStartup(TestCase):

    def setUp(self):
        self.game = Game()

    @patch('superstartrek.print')
    def test_startup(self, print_mock):
        self.game.startup()
        self.assertTrue(print_mock.called)
