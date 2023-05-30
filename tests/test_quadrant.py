from unittest import TestCase
from unittest.mock import patch
from quadrant import Quadrant
from basic_structure import Point, QuadrantData, Position, Entity

class TestQuadrant(TestCase):

    def test_quadrant__str__(self):
        # Setup
        quadrant = Quadrant(Point(1,1),QuadrantData(1, 1, 1), Position(Point(1, 1), Point(1,1)))
        quadrant.data = [[Entity.klingon for _ in range(1)] for _ in range(1)]

        # Call the method
        quadrant_str = quadrant.__str__()

        # Assertions
        self.assertEqual("+K+", quadrant_str)
