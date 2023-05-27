import unittest
from unittest import TestCase
from parameterized import parameterized
from superstartrek import Point, Game
import tempfile
import superstartrek as sst
from math import sqrt
from unittest.mock import patch

class PrintDirectionTest(TestCase):

    @parameterized.expand([
        # Test cases with positive delta1 and delta2
        (Point(0, 0), Point(3, 4), 4, 1, 8, 5.0),
        (Point(2, 2), Point(5, 7), 5, 2, 8, 5.830952),

        # Test cases with negative delta1 and positive delta2
        (Point(2, 2), Point(5, 7), -5, 2, 3.9, 5.830952),

        # Test cases with positive delta1 and negative delta2
        (Point(2, 3), Point(7, 1), 5, -2, 7, 5.385165),

        # Test cases with negative delta1 and delta2
        (Point(6, 6), Point(3, 3), -3, -3, 3, 4.242641),

    ])
    def test_print_direction(self, source, to, delta1, delta2, base, distance):
        output = []
        print_func = lambda msg: output.append(msg)
        
        with patch('builtins.print', print_func):
            sst.print_direction(source, to)

        if delta1 is not None and delta2 is not None:
            expected_direction = round(base + delta2 / delta1, 6) if delta1 >= delta2 else round(base + 2 - delta1 / delta2, 6)
            expected_output = [
                f"DIRECTION = {expected_direction}",
                f"DISTANCE = {round(distance, 6)}"
            ]
        else:
            expected_output = [f"DISTANCE = {round(distance, 6)}"]

        self.assertEqual(output, expected_output)