from world import World
from ship import Ship
from superstartrek import Game
from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized

class TestShortRangeScan(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()


    def test_damage_control_reset_damage_stats(self):
        # Setup
        damage_stats_list = [0,-0.01,-1000,1000,1,2,3,4]
        # Call the method
        self.game.damage_control_reset_damage_stats(damage_stats_list)

        # Assertions
        self.assertEqual(damage_stats_list, [0, 0, 0, 1000,1,2,3,4])

    @parameterized.expand([
        (-1000, 1),
        (0, 10),
        (-0.01, 1),
        (1000, 10),
    ])
    @patch('builtins.print')
    def test_damage_control_process_display_damage_control_report(self, damage_stats: float, expected_call_count: int, mock_print):
        # setup
        damage_stats_list = [0,-0.01,-1000,1000,1,damage_stats,3,4]
        # call the method
        self.game.damage_control_process_display_damage_control_report(damage_stats_list,("foo","foo","foo","foo","foo","foo","foo","foo"))
        # assert
        self.assertEqual(mock_print.call_count, expected_call_count)

    @parameterized.expand([
        (0, 0, 0, False),
        (-0.01, 0,0.1,True),
        (-0.01, 0.99,0.9,True),
        (-0.01, 0.98,0.9,True),
        (-0.01, 1000,0.9,True),
    ])
    def test_damage_control_calculate_damage_sum(self, damage_stats: float, delay_in_repairs_at_base: float, expected_damage_sum: float, expected_is_valid: bool):
        # setup
        damage_stats_list = [damage_stats,0,0,0,0,0,0,0]
        # call the method
        damage_sum, is_valid = self.game.damage_control_calculate_damage_sum(damage_stats_list, delay_in_repairs_at_base)
        # assert
        self.assertEqual(damage_sum, expected_damage_sum)
        self.assertEqual(is_valid, expected_is_valid)

    def test_damage_control_ship_not_docked_should_return_without_calling_calculating_damage_sum(self):
        # setup
        self.game.world.ship = Ship()
        self.game.world.ship.docked = False
        with patch.object(self.game, 'damage_control_calculate_damage_sum', wraps=self.game.damage_control_calculate_damage_sum) as wrapped_damage_control_calculate_damage_sum:
            # Call the method
            self.game.damage_control()
            # assert
            wrapped_damage_control_calculate_damage_sum.assert_not_called()

    @patch('builtins.input')
    def test_damage_control_ship_need_not_repair_ship_should_return_without_calling_input(self, mock_input):
        # setup
        self.game.world.ship = Ship()
        self.game.world.ship.docked = True
        with patch.object(self.game, 'damage_control_calculate_damage_sum', wraps=self.game.damage_control_calculate_damage_sum) as wrapped_damage_control_calculate_damage_sum:
            with patch.object(self.game, 'damage_control_reset_damage_stats', wraps=self.game.damage_control_reset_damage_stats) as wrapped_damage_control_reset_damage_stats:
                # Call the method
                self.game.damage_control()
                # assert
                wrapped_damage_control_reset_damage_stats.assert_not_called()
                wrapped_damage_control_calculate_damage_sum.assert_called_once()
                self.assertEqual(mock_input.call_count, 0)

    @patch('builtins.input')
    def test_damage_control_ship_need_wont_authorize_order_will_return_without_calling_reset_damage_stats(self, mock_input):
        # setup
        self.game.world.ship = Ship()
        self.game.world.ship.docked = True
        self.game.world.ship.damage_stats = [-1 for _ in range(8)]
        with patch.object(self.game, 'damage_control_reset_damage_stats', wraps=self.game.damage_control_reset_damage_stats) as self_wrapped_damage_control_reset_damage_stats:
            mock_input.return_value = 'N'
            # Call the method
            self.game.damage_control()
            # assert
            self_wrapped_damage_control_reset_damage_stats.assert_not_called()
            self.assertEqual(mock_input.call_count, 1)

    @patch('builtins.input')
    def test_full_damage_control_should_go_through_all_logic_in_the_function(self, mock_input):
        # setup
        self.game.world.ship = Ship()
        self.game.world.ship.docked = True
        self.game.world.ship.damage_stats = [-1 for _ in range(8)]
        self.game.world.stardate = 10
        self.game.world.quadrant.delay_in_repairs_at_base = 0
        mock_input.return_value = 'Y'
        # Call the method
        self.game.damage_control()
        self.assertEqual(self.game.world.stardate, 10.9)

        
