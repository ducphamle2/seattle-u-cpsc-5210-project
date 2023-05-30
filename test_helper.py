from unittest import TestCase
from unittest.mock import patch
from helper import get_user_float, klingon_shield_strength

class TestHelper(TestCase):

    @patch('builtins.input')
    def test_get_user_float_exception(self, input_mock):
        # Setup
        input_mock.side_effect = ['foo', 3]

        # Call the method
        result = get_user_float('')

        # Assertions
        self.assertEqual(input_mock.call_count, 2)
        self.assertEqual(result, 3)
        self.assertEqual(klingon_shield_strength, 200)