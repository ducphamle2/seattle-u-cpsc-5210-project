from superstartrek import World


def test_world():
    world = World()
    print(world.remaining_time())
    print(world.has_mission_ended())
