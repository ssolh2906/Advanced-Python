"""
Define a test class that inherits from unittest.TestCase.
Write test methods for reverse_string and is_palindrome using appropriate assertions.
Include tests for both valid and invalid inputs, edge cases, and expected behavior.
Organize tests logically within the class.
"""

from unittest import TestCase
from string_utils import reverse_string, is_palindrome


class TestStringUtils(TestCase):
    # Test reverse_string function
    def test_reverse_string_valid(self):
        self.assertEqual(reverse_string("my string"), "gnirts ym")
        self.assertEqual(reverse_string(""), "")

    def test_reverse_string_invalid(self):
        self.assertRaises(TypeError, reverse_string, 123)
        self.assertRaises(TypeError, reverse_string, ["Invalide input"])
        self.assertRaises(TypeError, reverse_string, None)

    def test_reverse_string_edge_cases(self):
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("a"), "a")
        self.assertEqual(reverse_string("12345"), "54321")

    def test_reverse_string_non_string_input(self):
        self.assertRaises(TypeError, reverse_string, 1)

    # Test is_palindrome function
    def test_is_palindrome_valid(self):
        pass

    def test_is_palindrome_invalid(self):
        pass

    def test_is_palindrome_edge_cases(self):
        pass

    def test_is_palindrome_non_string_input(self):
        pass


"""
3. Run the tests: Execute the tests using python -m unittest test_string_utils.py.
Observe the test results and ensure all tests pass.
"""

if __name__ == '__main__':
    import unittest

    unittest.main()
