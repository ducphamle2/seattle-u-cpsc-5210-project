import unittest
import sys
from superstartrek import Point, Position, Ship
from unittest import TestCase
import sys 
from unittest.mock import patch
from parameterized import parameterized
from superstartrek import Ship, Game, World
from io import StringIO

class TestingShip(TestCase):

    def test_ship_refill(self):
        ship = Ship()
        ship.refill()
        self.assertEqual(ship.energy_capacity, 3000)
        self.assertEqual(ship.torpedo_capacity, 10)

    @parameterized.expand([
        ("energy_greater_than_0_nominal", 1500, 1490),
        ("energy_equal_0_on_boundary", 2990, 0), 
        ("energy_smaller_0_off_boundary_lower", 2991, 0),
    ])
    def test_manuver_energy_energy_value(self, __name__, n, expected_energy):
        # fixture
        ship = Ship()
        # mock max value to always return the shields so we dont need to care about comparing with zero
        ship.maneuver_energy(n)
        self.assertEqual(ship.energy, expected_energy)

    @parameterized.expand([
        ("energy_smaller_0_shield_greater_than_0_should_not_return_0", 2990, 1, 1),
        ("energy_smaller_0_shield_equal_to_0_should_return_0", 2990, 0, 0),
        ("energy_smaller_0_shield_smaller_than_0_should_return_0", 2991, 0, 0),
    ])
    def test_manuver_energy_shield(self, __name__, n, shield_value, expected_shield):
        # fixture
        ship = Ship()
        ship.shields = shield_value
        # mock max value to always return the shields so we dont need to care about comparing with zero
        ship.maneuver_energy(n)
        self.assertEqual(ship.shields, expected_shield)
        
        
    @patch('star_trek_game.fnr', return_value=4)
    def ship_initializer(self):
        
        expected_devices = ("WARP ENGINES",
            "SHORT RANGE SENSORS",
            "LONG RANGE SENSORS",
            "PHASER CONTROL",
            "PHOTON TUBES",
            "DAMAGE CONTROL",
            "SHIELD CONTROL",
            "LIBRARY-COMPUTER",)
        
        ship = Ship()
        self.assertEqual(ship.position, Position(Point(4, 4), Point(4, 4)))
        self.assertEqual(ship.energy, 3000)
        self.assertEqual(ship.torpedoes, 10)
        self.assertEqual(ship.docked, False)
        self.assertEqual(ship.devices, expected_devices)
        self.assertEqual(ship.damage_stats, [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(ship.shields, 0)

    @parameterized.expand([
        ('shields_input_greater_than_0_valid', '1', 1),
        ('shields_input_smaller_than_energy_plus_shields_valid','100', 100),   
        ('shields_valid_value','50', 50),         
    ])
    def test_shield_control_shields_valid_input(self, __name__, input_value, expected_shields):
        ship = Ship()
        initial_energy = 101  #energy start value, considered as an upper boundary for shields 
        ship.energy = initial_energy
        initial_shileds = ship.shields
        
        with patch('builtins.input', return_value=input_value):
            with StringIO() as buffer:
                sys.stdout = buffer
                ship.shield_control()
                output = buffer.getvalue()

                assert ship.energy == initial_energy + initial_shileds - int(input_value)
                assert expected_shields == ship.shields

                assert "DEFLECTOR CONTROL ROOM REPORT:" in output
                assert f"  'SHIELDS NOW AT {ship.shields} UNITS PER YOUR COMMAND.'" in output

                sys.stdout = sys.__stdout__


    @parameterized.expand([
        ('abc',),
        ('1.2',), 
    ])
    def test_shield_control_raises_value_error_with_invalid_shields_input(self, input_value):
        ship = Ship()
        with patch('builtins.input', return_value=input_value):
            with self.assertRaises(ValueError) as context:
                ship.shield_control()
            
            self.assertEqual(str(context.exception), f"invalid literal for int() with base 10: '{input_value}'")


    def test_shield_control_shields_valid_input_very_large(self):
        ship = Ship()
        initial_energy = 99999999999999999999999999999999999999999999999999999999999999999999999999999999
        initial_shileds = ship.shields
        ship.energy = initial_energy
        # choose x smaller than initial_energy so it would be valid
        x = '99999999999999999999999999999999999999999999999999999999999999999999999999999998'
        x_int = int(x)
        with patch('builtins.input', return_value=x):
                ship.shield_control()

                assert ship.shields == x_int
                assert ship.energy == initial_energy + initial_shileds - x_int

    
    @parameterized.expand([
        ("damage_stats[6]_equals_minus_1_on_boundary", -1),
        ("damage_stats[6]_equals_minus_10_off_boundary_lower", -10)
    ])
    def test_shield_control_damage_stats_6_less_than_0(self, __name__, damage_stats):
        ship = Ship()
        ship.damage_stats[6] = damage_stats
        captured_output = StringIO()                  # Create StringIO object
        sys.stdout = captured_output                     #  and redirect stdout.
        ship.shield_control()                                  # Call function.
        sys.stdout = sys.__stdout__                     # Reset redirect.
        self.assertEqual(captured_output.getvalue(), 'SHIELD CONTROL INOPERABLE\n')
    
    @parameterized.expand([
        ("input_energy_value_minus_50_off_boundary_lower", '-50'),
        ("input_energy_value_minus_1_on_boundary", '-1')
    ])
    def test_shield_control_x_less_than_zero(self, __name__, input_value):
        ship = Ship()
        ship.damage_stats[6] = 6 # damage_stats[6] must have a positive value for this test.
        captured_output = StringIO()                  # Create StringIO object
        sys.stdout = captured_output        
        with patch('builtins.input', return_value=input_value):
            ship.shield_control()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), '<SHIELDS UNCHANGED>\n')
    
    def test_shield_control_shields_equals_x(self):
        ship = Ship()
        ship.damage_stats[6] = 6 #damage stats must be positive for this test
        ship.shields = 265
        captured_output = StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='265'):
            ship.shield_control()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), '<SHIELDS UNCHANGED>\n')

    def test_shield_control_x_greater_than_energy_plus_shields(self):
        ship = Ship()
        ship.damage_stats[6] = 6 # damage stats must be positive for this test
        ship.shields = 300
        ship.energy = 500
        captured_output = StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='1000'):
            ship.shield_control()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "SHIELD CONTROL REPORTS  'THIS IS NOT THE FEDERATION "
                "TREASURY.'\n"
                "<SHIELDS UNCHANGED>\n")   
        
class TestingGame(TestCase):

    @parameterized.expand([
        ("dirs_len_minus_one_equal_course_data", 3, 3, 0, True),
        ("dirs_len_smaller_than_course_data", 1, 3, 2, False),
        ("dirs_len_equal_to_course_data", 2, 3, 2, False),
        ("course_data_smaller_than_zero", 2, -1, -2, False)
    ])
    def test_navigation_process_course_data(self, __name__, dirs_len: int, user_input: int, expected_cd: int, expected_is_valid_course_data: bool):
        game = Game()
        with patch('builtins.input', return_value=user_input):
            cd, is_course_data_valid = game.navigation_process_course_data(dirs_len)
        self.assertEqual(cd, expected_cd)
        self.assertEqual(is_course_data_valid, expected_is_valid_course_data)

    @parameterized.expand([
        ("damage_stat_smaller_than_zero_warp_greater_than_0.2", 0.3, -0.01, "WARP ENGINES ARE DAMAGED. MAXIMUM SPEED = WARP 0.2\n", False),
        ("warp_is_zero", 0, -1, "", False),
        ("warp_smaller_than_zero", -0.01, -1, f"   CHIEF ENGINEER SCOTT REPORTS 'THE ENGINES WON'T TAKE WARP -0.01!'\n", False),
        ("damage_stats_greater_than_zero_warp_greater_than_eight", 8.01, 1, f"   CHIEF ENGINEER SCOTT REPORTS 'THE ENGINES WON'T TAKE WARP 8.01!'\n", False),
        ("damage_stats_greater_than_zero_warp_is_0.2", 0.2, 1, "", True),
        ("damage_stats_equal_zero_warp_is_8", 8, 0, "", True),
    ])
    def test_navigation_process_warp(self, __name__, warp_input: float, damage_stat: float, expected_print: str, expected_is_warp_valid: bool):
        game = Game()
        with patch('builtins.input', return_value=warp_input):
            captured_output = StringIO()                  # Create StringIO object
            sys.stdout = captured_output                     #  and redirect stdout.
            warp, is_warp_valid = game.navigation_process_warp(damage_stat)
            self.assertEqual(is_warp_valid, expected_is_warp_valid)
            self.assertEqual(warp, warp_input)
            self.assertEqual(captured_output.getvalue(), expected_print)

    @parameterized.expand([
        ("ship_energy_greater_than_warp_rounds", 1, 1, 9, 1, "", True),
        ("ship_energy_equal_warp_rounds", 1, 1, 8, 1, "", True),
        ("ship_energy_smaller_than_warp_rounds_ship_shields_smaller_than_warp_rounds_minus_energy", 1, 0, 7, 1, "ENGINEERING REPORTS   'INSUFFICIENT ENERGY AVAILABLE\n                       FOR MANEUVERING AT WARP 1!'\n", False),
        ("ship_energy_smaller_than_warp_rounds_damage_stat_smaller_than_0", 2, 1, 1, -0.01, "ENGINEERING REPORTS   'INSUFFICIENT ENERGY AVAILABLE\n                       FOR MANEUVERING AT WARP 2!'\n", False),
        ("ship_energy_smaller_than_warp_rounds_ship_shield_equal_wrap_round_minus_energy_damage_stat_equal_0", 0, 1, -1, 0, "ENGINEERING REPORTS   'INSUFFICIENT ENERGY AVAILABLE\n                       FOR MANEUVERING AT WARP 0!'\nDEFLECTOR CONTROL ROOM ACKNOWLEDGES 1 UNITS OF ENERGY\n                         PRESENTLY DEPLOYED TO SHIELDS.\n", False),
        ("ship_energy_smaller_than_warp_rounds_ship_shield_greater_than_wrap_round_minus_energy_damage_stat_greater_than_0", 0, 2, -1, 0.01, "ENGINEERING REPORTS   'INSUFFICIENT ENERGY AVAILABLE\n                       FOR MANEUVERING AT WARP 0!'\nDEFLECTOR CONTROL ROOM ACKNOWLEDGES 2 UNITS OF ENERGY\n                         PRESENTLY DEPLOYED TO SHIELDS.\n", False),
    ])
    def test_navigation_process_warp_rounds(self, __name__, warp: int, ship_shields: int, ship_energy: int, damage_stat: float, expected_print: str, expected_is_warp_rounds_valid: bool):
        game = Game()
        captured_output = StringIO()                  # Create StringIO object
        sys.stdout = captured_output                     #  and redirect stdout.
        warp_rounds, is_warp_rounds_valid = game.navigation_process_warp_rounds(warp, ship_shields, ship_energy, damage_stat)
        self.assertEqual(is_warp_rounds_valid, expected_is_warp_rounds_valid)
        self.assertEqual(warp_rounds, round(warp * 8))
        self.assertEqual(captured_output.getvalue(), expected_print)

    @parameterized.expand([
        ("world has ended", True, True),
        ("world has not ended", False, False)
    ])
    def test_navigation_check_world_has_ended(self, __name__, has_mission_ended: bool, expected_check_world_has_ended: bool):
        game = Game()
        world = World()
        # mocking methods that we do not care
        world.has_mission_ended = lambda : has_mission_ended
        game.end_game = lambda won, quit : None
        world_has_ended = game.navigation_check_world_has_ended(world)
        self.assertEqual(world_has_ended, expected_check_world_has_ended)


if __name__ == '__main__':
    unittest.main()

