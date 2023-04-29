from superstartrek import World
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from parameterized import parameterized


class Testing(TestCase):

    @parameterized.expand([
        ("ended", -1, True),
        ("not ended", 5, False),
    ])
    def test_mock_has_mission_ended(self, name, p1, p2):
        world = World()
        world.remaining_time = MagicMock(name='remaining_time')
        world.remaining_time.return_value = p1
        self.assertEqual(world.has_mission_ended(), p2)


if __name__ == '__main__':
    unittest.main()
