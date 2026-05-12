"""
reverse_string(s): Reverses a given string.
is_palindrome(s): Checks if a string is a palindrome (reads the same backward as forward. For example: "TACOCAT").
"""


def reverse_string(s: str):
    """
    Reverses a given string.

    >>> reverse_string("hello")
    'olleh'
    >>> reverse_string("tacocat")
    'tacocat'
    >>> reverse_string("")
    ''
    >>> reverse_string("a")
    'a'
    >>> reverse_string(123)
    Traceback (most recent call last):
        ...
    TypeError: Input must be a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    try:
        return s[::-1]
    except TypeError:
        raise TypeError("Input must be a string.")


def is_palindrome(s: str):
    """
    Returns True if the input string is a palindrome, returns False otherwise.
    >>> is_palindrome("hello")
    False
    >>> is_palindrome("tacocat")
    True
    >>> is_palindrome("a")
    True
    >>> is_palindrome(123)
    Traceback (most recent call last):
        ...
    TypeError: Input must be a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    try:
        s_low = s.lower()
        s_rev = reverse_string(s_low)
    except TypeError as e:
        raise TypeError("Input must be a string.") from e

    if s_low == s_rev:
        return True
    else:
        return False


"""
Part 3: doctest

    Embed tests in docstrings: Add doctests to the reverse_string and is_palindrome functions within string_utils.py.
        Include examples of expected function behavior using >>> and the expected output.

    Run the doctests: Execute the doctests using python -m doctest -v string_utils.py.
        Observe the results and make sure all doctests pass.
        
Bonus:
    Explore pytest fixtures for setting up and tearing down test resources.
"""
