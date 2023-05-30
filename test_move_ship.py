from world import World
from superstartrek import Game
from basic_structure import Point, Entity
from unittest import TestCase
from superstartrek import Game, World
from parameterized import parameterized

class TestShortRangeScan(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()

    @parameterized.expand([
        (Point(0, 0), Point(0,0), Point(0,0), Point(0,0), False),
        (Point(-1, 0), Point(5,0), Point(0,0), Point(0,0), True),
        (Point(-1000, 0), Point(2,0), Point(0,0), Point(0,0), True),
        (Point(7, 0), Point(7,0), Point(7,0), Point(7,0), False),
        (Point(8, 0), Point(2,0), Point(7,0), Point(7,0), True),
        (Point(0, -1), Point(0,-1), Point(0,0), Point(0,0), True),
        (Point(0, -1000), Point(0,2), Point(0,0), Point(0,0), True),
        (Point(0, 7), Point(0,7), Point(0,7), Point(0,7), False),
        (Point(0, 8), Point(0,2), Point(0,7), Point(0,7), True),
    ])
    def test_move_ship_verify_hit_edge_calculating_final_position(self, quadrant: Point, sector: Point, expected_quadrant: Point, expected_sector: Point, expected_hit_edge: bool):
        # Call the method
        hit_edge = self.game.move_ship_verify_hit_edge_calculating_final_position(quadrant, sector)

        # Assertions
        self.assertEqual(hit_edge, expected_hit_edge)
        self.assertEqual(quadrant, expected_quadrant)
        self.assertEqual(sector, expected_sector)

    @parameterized.expand([
        (Point(1, 1), Point(1,1), True),
        (Point(1, 2), Point(1,1), False),
        (Point(2, 1), Point(1,1), False),
        (Point(2, 2), Point(1,1), False),
    ])
    def test_move_ship_is_stay_in_quadrant(self, start_quadrant: Point, quadrant: Point, expected_result: bool):
        # Call the method
        result = self.game.move_ship_is_stay_in_quadrant(quadrant, start_quadrant)
        # assert
        self.assertEqual(result, expected_result)

    def test_move_ship_increment_sector(self):
        # call the method
        result = self.game.move_ship_increment_sector(2, 0.5, 2)
        self.assertEqual(result, 17)

    @parameterized.expand([
        (Point(1, 1), Point(1,1), 8, 8, Point(1,1), Point(0,0)),
        (Point(0, 0), Point(0,0), 0, 0, Point(0,0), Point(0,0)),
        (Point(1, 1), Point(1,1), 1000, 1000, Point(125,125), Point(0,0)),
    ])
    def test_move_ship_calculate_ship_position_quadrant_limits(self, quadrant: Point, sector: Point, sector_start_x: float, sector_start_y: float, expected_quadrant: Point, expected_sector: Point):
        # setup
        # Call the method
        self.game.move_ship_calculate_ship_position_quadrant_limits(quadrant, sector, sector_start_x, sector_start_y)
        # assert
        self.assertEqual(quadrant, expected_quadrant)
        self.assertEqual(sector, expected_sector)
        
    
    def test_move_ship_shut_down_sector_bad_navigation_void_entity_should_return_false(self):
        # setup
        # Call the method
        result = self.game.move_ship_shut_down_sector_bad_navigation(Point(0,0), Entity.void, 0, 0)
        self.assertEqual(result, False)

    def test_move_ship_shut_down_sector_bad_navigation_not_void_entity_should_return_true(self):
        # setup
        # Call the method
        result = self.game.move_ship_shut_down_sector_bad_navigation(Point(0,0), Entity.klingon, 0, 0)
        self.assertEqual(result, True)