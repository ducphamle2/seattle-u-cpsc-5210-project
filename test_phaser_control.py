from world import World
from ship import Ship
from quadrant import Quadrant
from basic_structure import Point, QuadrantData, Position, KlingonShip
from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized
from world import World
from ship import Ship
from superstartrek import Game

class PhaserControlTest(TestCase):

    @parameterized.expand([
        ("ship_damage_less_than_0_returns_false", -1, False),
        ("ship_damage_equal_0_returns_true", 0, True),
        ("ship_damage_greater_than_0_returns_true", 10, True),
    ])
    def test_check_phasers_operational(self, __name__, ship_damage, expected_result):
        game = Game()
        ship = Ship()
        ship.damage_stats[3] = ship_damage
        assert game.check_phasers_operational(ship) == expected_result


    @parameterized.expand([
        ("no_klingons_returns_true_when_klingons_negative", -1, True),
        ("no_klingons_returns_true_when_klingons_zero", 0, True),
        ("no_klingons_returns_false_when_klingons_exist", 10, False),
    ])
    def test_check_no_klingons(self, __name__, nb_klingons, expected_result):
        game = Game()
        world = World()
        world.quadrant.nb_klingons = nb_klingons
        assert game.check_no_klingons(world) == expected_result

    @patch('superstartrek.print')
    def test_check_computer_accuracy_damage_stats_at_7_less_than_0(self, print_mock):
        game = Game()
        game.world = World()
        game.world.ship.damage_stats[7] = -8
        game.check_computer_accuracy(game.world.ship)
        print_mock.assert_called_with('COMPUTER FAILURE HAMPERS ACCURACY')


    @parameterized.expand([
        (["10"], 10, 20),  # case where user input is less than ship energy
        (["-10", "10"], None, 20),  # case where first user input is negative
        (["0", "10"], None, 20),  # case where first user input is zero
        (["30", "10"], 10, 20),  # case where first user input is more than ship energy
    ])
    def test_get_phaser_firepower(self, input_values, expected, ship_energy):
        game = Game()  # Initialize an instance of game
        ship = Ship()
        ship.energy = ship_energy  # Set the ship's energy
        
        with patch('builtins.input', side_effect=input_values):
            result = game.get_phaser_firepower(ship)
            # print(f"input_values: {input_values}, expected: {expected}, result: {result}")
            assert result == expected

    @parameterized.expand([
        (50, 10, 40),  # Test case where initial energy is 50 and firepower is 10, so final energy should be 40
        (20, 20, 0),  # Test case where initial energy is 20 and firepower is 20, so final energy should be 0
        (30, 40, -10)  # Test case where initial energy is 30 and firepower is 40, so final energy should be -10
    ])
    def test_adjust_ship_energy(self, initial_energy, firepower, final_energy):
        game = Game()
        ship = Ship()
        ship.energy = initial_energy

        game.adjust_ship_energy(ship, firepower)

        assert ship.energy == final_energy

    @parameterized.expand([
        (50, 0, 50),  # Test case where damage_stat is 0, firepower should stay the same
        (20, 1, 20),  # Test case where damage_stat is 1, firepower should stay the same
    ])
    def test_adjust_phaser_firepower_no_damage(self, initial_firepower, damage_stat, expected_firepower):
        game = Game()
        ship = Ship()
        ship.damage_stats[7] = damage_stat

        result = game.adjust_phaser_firepower(ship, initial_firepower)

        assert result == expected_firepower

    @parameterized.expand([
        (50, -1, 0.5),  # Test case where damage_stat is -1
        (20, -10, 0.2),  # Test case where damage_stat is -10
    ])
    def test_adjust_phaser_firepower_with_damage(self, initial_firepower, damage_stat, expected_multiplier):
        game = Game()
        ship = Ship()
        ship.damage_stats[7] = damage_stat

        with patch.object(game, 'get_random_multiplier', return_value=expected_multiplier):
            result = game.adjust_phaser_firepower(ship, initial_firepower)

        assert result == initial_firepower * expected_multiplier

    @parameterized.expand([
        (100, 1, 100),  # case where there is only one Klingon
        (100, 3, 33),  # case where there are three Klingons
        (0, 1, 0),  # case where phaser firepower is zero
    ])
    def test_get_phaser_per_klingon(self, phaser_firepower, nb_klingons, expected_phaser_per_klingon):
        game = Game()  # Initialize an instance of game
        world = World()  # Initialize an instance of World
        world.quadrant.nb_klingons = nb_klingons  # Set the number of Klingons

        result = game.get_phaser_per_klingon(world, phaser_firepower)

        assert result == expected_phaser_per_klingon


    @parameterized.expand([
        # Case 1: One Klingon ship with shield already at 0
        (100, [Point(0, 0)], [0]),  
        
        # Case 2: One Klingon ship with shield of 100, damage (h) inflicted will be less than 15 of shield
        (10, [Point(0, 0)], [100]),  

        # Case 3: Two Klingon ships, one with shield of 100 and another with shield of 0. 
        # The damage (h) inflicted will be 200, enough to destroy the ship with the shield, leading to game won.
        (200, [Point(0, 0), Point(0, 1)], [100, 0])  
    ])
    @patch('superstartrek.Game.get_h')
    def test_fire_phasers_on_klingon(self, phaser_energy, klingon_positions, klingon_shields, mock_get_h):
        game = Game()  # Initialize an instance of game
        ship = Ship()  # Initialize an instance of ship
        world = World()  # Initialize an instance of World
        
        world.quadrant = Quadrant(Point(0, 0), QuadrantData(len(klingon_positions), 0, 0), Position(Point(0, 0), Point(0, 0)))  # Set the quadrant of the world
        world.quadrant.klingon_ships = [KlingonShip(pos, shield) for pos, shield in zip(klingon_positions, klingon_shields)]  # Populate the klingon ships
        world.quadrant.nb_klingons = len(klingon_positions)  # Set the number of Klingons
        world.remaining_klingons = len(klingon_positions)  # Set the remaining Klingons

        mock_get_h.return_value = phaser_energy  # Set a mock value for get_h method to be the phaser_energy

        game.fire_phasers_on_klingon(world, ship, world.quadrant.klingon_ships, phaser_energy)

        # Assert here that the klingon ships have the expected remaining shield
        for idx, klingon_ship in enumerate(world.quadrant.klingon_ships):
            if klingon_shields[idx] == 0:
                # If the initial shield was 0, it should still be 0
                expected_remaining_shield = 0
            elif phaser_energy <= 0.15 * klingon_shields[idx]:
                # If the phaser_energy was less than or equal to 15% of the initial shield, no damage should be done
                expected_remaining_shield = klingon_shields[idx]
            elif phaser_energy > klingon_shields[idx]:
                # If the phaser_energy was higher than the initial shield, the ship should be destroyed (shield = 0)
                expected_remaining_shield = 0
            else:
                # If the phaser_energy was higher than 15% of the initial shield but less than the shield itself, the shield should decrease by the phaser_energy
                expected_remaining_shield = klingon_shields[idx] - phaser_energy

            assert klingon_ship.shield == expected_remaining_shield




