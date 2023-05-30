from unittest import TestCase
from world import World
from parameterized import parameterized
from unittest.mock import patch

class TestWorld(TestCase):

    def test_world_remaining_time_should_return_remaining_time(self):
        # Setup
        world = World()
        world.initial_stardate = 100
        world.mission_duration = 10
        world.stardate = 20

        # Call the method
        remaining_time = world.remaining_time()

        # Assertions
        self.assertEqual(remaining_time, 90)

    @parameterized.expand([
        (1000, False),
        (0, False),
        (-0.01, True),
        (-1000, True),
    ])
    def test_world_has_mission_ended(self, remaining: float, expected_is_ended: bool):
        # Setup
        world = World()
        world.remaining_time = lambda: remaining

        # Call the method
        has_ended = world.has_mission_ended()

        # Assertions
        self.assertEqual(has_ended, expected_is_ended)

    @parameterized.expand([
        (0.99, 3),  # test case for r1 > 0.98
        (0.98, 3),  # test case for r1 = 0.98 (boundary case)
        (0.979, 2),  # test case for r1 just below 0.98 (boundary case)
    
        (0.97, 2),  # test case for 0.95 < r1 <= 0.98
        (0.95, 2),  # test case for r1 = 0.95 (boundary case)
        (0.949, 1),  # test case for r1 just below 0.95 (boundary case)
    
        (0.85, 1),  # test case for 0.80 < r1 <= 0.95
        (0.80, 1),  # test case for r1 = 0.80 (boundary case)
        (0.799, 0),  # test case for r1 just below 0.80 (boundary case)
    
        (0.75, 0),  # test case for r1 <= 0.80
    ])
    def test_remaining_klingons(self, random_return, expected_klingons):
        total_klingons = 100
        with patch('random.random', return_value=random_return):
            world = World(total_klingons=total_klingons)
            
            # The expected remaining klingons is calculated based on the mocked random value
            # As we have 8x8 quadrants and each quadrant will have expected_klingons because we mocked random.random()
            expected_remaining_klingons = total_klingons - (expected_klingons * 8 * 8)
            
            self.assertEqual(world.remaining_klingons, expected_remaining_klingons, "Remaining klingons calculation is incorrect")