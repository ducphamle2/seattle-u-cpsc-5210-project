from superstartrek import World
import unittest
from unittest import TestCase
from unittest.mock import MagicMock


class Testing(TestCase):

    def test_mock_has_mission_ended(self):
        param_list = [(-1, True), (5, False)]
        for p1, p2 in param_list:
            with self.subTest():
                world = World()
                world.remaining_time = MagicMock(name='remaining_time')
                world.remaining_time.return_value = p1
                assert world.has_mission_ended() == p2


if __name__ == '__main__':
    unittest.main()
