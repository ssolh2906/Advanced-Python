"""
Write test functions for reverse_string and is_palindrome using assert statements.
Use parameterized testing with @pytest.mark.parameterize to test multiple input values efficiently.
Test for expected exceptions using with pytest.raises(...). Modify string_utils.py if you haven't included the exception handling.
"""

import pytest
from string_utils import reverse_string, is_palindrome

class TestStringUtilsPytest:

    @pytest.mark.parametrize("input_string, expected_output", [
        ("hello", "olleh"),
        ("tacocat", "tacocat"),
        ("", ""),
        ("a", "a"),
    ])
    def test_reverse_string_valid(self, input_string, expected_output):
        assert reverse_string(input_string) == expected_output

    def test_reverse_string_exception(self):
        with pytest.raises(TypeError):
            reverse_string(123)

    @pytest.mark.parametrize("input_string, expected_output", [
        ("hello", False),
        ("tacocat", True),
        ("", True),
        ("a", True),
    ])
    def test_is_palindrome_valid(self, input_string, expected_output):
        assert is_palindrome(reverse_string(input_string)) == expected_output

    def test_is_palindrome_exception(self):
        with pytest.raises(TypeError):
            is_palindrome(123)


"""
3. Execute the tests using pytest test_string_utils_pytest.py.
 Examine the test results and ensure all tests pass.
"""
