from superstartrek import World
import unittest


class Testing(unittest.TestCase):
    def test_world(self):
        world = World()
        print(world.remaining_time())
        print(world.has_mission_ended())


if __name__ == '__main__':
    unittest.main()
