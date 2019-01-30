"""
This program takes the input from the search box and checks if any mistakes were made.
Illegal queries include:
- Parentheses that were opened were not closed.
- Two or more operators next to each other with no search word in between.
- Exact phrase quotation marks open but do not close.
- Operators within an exact phrase (this might be updated in later versions).
- WITHIN and NEAR operators without a distance number or with a distance number of more than 3 digits.
- Empty query.
"""

import re
import doctest


def check_parentheses(input_string):
    """
    This function checks whether all opening parentheses have corresponding closing parentheses.
    :param input_string: raw input string.
    :return: Boolean.
    >>> check_parentheses('w (w w) w ((w(w w)w) w )')
    True
    >>> check_parentheses('w (w w) w ((w(w ww) w )')
    False
    >>> check_parentheses('w w w) w ((w(w w)w) w )')
    False
    """
    pcounter = 0
    for char in input_string:
        if char == '(':
            pcounter += 1
        elif char == ')':
            pcounter -= 1
    if pcounter != 0:
        return False
    else:
        return True


def run(input_string):
    """
    This function takes the input string and runs all tests.
    :param input_string: Raw input string from search box.
    :return: Error message.
    """
    pass

if __name__ == '__main__':
    doctest.testmod()