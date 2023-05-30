from unittest import TestCase
from unittest.mock import patch
from quadrant import Quadrant
from basic_structure import Point, QuadrantData, Position, Entity
from parameterized import parameterized

class TestQuadrant(TestCase):

    def test_quadrant__str__(self):
        # Setup
        quadrant = Quadrant(Point(1,1),QuadrantData(1, 1, 1), Position(Point(1, 1), Point(1,1)))
        quadrant.data = [[Entity.klingon for _ in range(1)] for _ in range(1)]

        # Call the method
        quadrant_str = quadrant.__str__()

        # Assertions
        self.assertEqual("+K+", quadrant_str)

    @parameterized.expand([
        (0, 0),  # test case for lower boundary
        (7, 7),  # test case for upper boundary
        (0, 7),  # test case for mixed boundary conditions
        (7, 0),  # test case for mixed boundary conditions
    ])
    def test_quadrant_initialization(self, point_x, point_y):
        point = Point(point_x, point_y)
        population = QuadrantData(0, 0, 0)
        ship_position = Position(point, point)
        quadrant = Quadrant(point, population, ship_position)
        self.assertEqual(quadrant.name, Quadrant.quadrant_name(point.x, point.y, False))

    @parameterized.expand([
        (-1, 0),  # test case for point.x below lower boundary
        (8, 0),  # test case for point.x above upper boundary
        (0, -1),  # test case for point.y below lower boundary
        (0, 8),  # test case for point.y above upper boundary
    ])
    def test_quadrant_initialization_out_of_bounds(self, point_x, point_y):
        point = Point(point_x, point_y)
        population = QuadrantData(0, 0, 0)
        ship_position = Position(point, point)
        with self.assertRaises(AssertionError):
            Quadrant(point, population, ship_position)
