from unittest import TestCase
from world import World
from parameterized import parameterized

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
