import unittest
from unittest.mock import patch
from superstartrek import Game, World

class TestEndGame(unittest.TestCase):

    @patch('builtins.input', return_value='AYE')
    @patch('builtins.print')
    @patch('sys.exit', side_effect=lambda *args: None)  # Replace sys.exit with a no-op lambda function
    def test_end_game_won(self, mock_sys_exit, mock_print, mock_input):
        world = World()
        world.remaining_klingons = 10
        world.stardate = 150
        world.initial_stardate = 100
        game = Game()
        game.world = world
        game.end_game(won=True)

        # Verify the print statements
        mock_print.assert_any_call("CONGRATULATIONS, CAPTAIN! THE LAST KLINGON BATTLE CRUISER")
        mock_print.assert_any_call("MENACING THE FEDERATION HAS BEEN DESTROYED.\n")
        mock_print.assert_any_call("YOUR EFFICIENCY RATING IS 40.0\n\n")
        mock_print.assert_any_call("THE FEDERATION IS IN NEED OF A NEW STARSHIP COMMANDER")
        mock_print.assert_any_call("FOR A SIMILAR MISSION -- IF THERE IS A VOLUNTEER,")

        mock_input.assert_called_once_with("LET HIM STEP FORWARD AND ENTER 'AYE'? ")

        self.assertEqual(game.restart, True)

    @patch('builtins.input', return_value='AYE')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_end_game_lost(self, mock_sys_exit, mock_print, mock_input):
        world = World()
        world.remaining_klingons = 10
        world.stardate = 150
        world.initial_stardate = 100

        game = Game()
        game.world = world

        game.end_game(quit=False,enterprise_killed=True)

        # Verify the print statements
        mock_print.assert_any_call("\nTHE ENTERPRISE HAS BEEN DESTROYED. THE FEDERATION WILL BE CONQUERED.")
        mock_print.assert_any_call("IT IS STARDATE 150")
        mock_print.assert_any_call("THERE WERE 10 KLINGON BATTLE CRUISERS LEFT AT")
        mock_print.assert_any_call("THE END OF YOUR MISSION.\n\n")

        mock_input.assert_called_once_with("LET HIM STEP FORWARD AND ENTER 'AYE'? ")

        self.assertEqual(game.restart, True)