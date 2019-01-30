"""
This program takes the input from the search box and checks if any mistakes were made.
Illegal queries include:
- Parentheses that were opened were not closed. (u"\u2713")
- Two or more operators next to each other with no search word in between. (u"\u2713")
- Operators right of opening parentheses. (w1 AND(w1..)) works but (w1 (AND w2)..) does not. (u"\u2713")
- Search tokens left of closing parentheses.
- Exact phrase quotation marks open but do not close. (u"\u2713")
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


def operator_neighbors(input_string):
    """
    This function checks whether operators are separated by words.
    :param input_string: raw input string
    :return: Boolean.
    >>> operator_neighbors('w AND w OR w WITHIN3 (w BUT NOT w) NEAR756 w ~ w, w|w')
    True
    >>> operator_neighbors('w AND AND w')
    False
    >>> operator_neighbors('w AND w ~ | w')
    False
    >>> operator_neighbors('w & w &NEAR76')
    False
    >>> operator_neighbors('w WITHIN5 NOT w')
    False
    """
    op_re1 = r'\&|\||AND|OR|BUT\sNOT|NOT|\~|\,|NEAR\d{1,3}|WITHIN\d{1,3}'
    regex = re.compile('(%s)\s*(%s)' % (op_re1, op_re1))
    if re.search(regex, input_string) is None:
        return True
    else:
        return False


def operator_parentheses(input_string):
    """
    This function checks if an operator follows an opening parenthesis or precedes a closing parenthesis.
    :param input_string: raw input string.
    :return: Boolean.
    >>> operator_parentheses('w AND (w OR w)')
    True
    >>> operator_parentheses('w AND (AND word)')
    False
    >>> operator_parentheses('w AND ( AND word)')
    False
    >>> operator_parentheses('w AND (w AND)')
    False
    >>> operator_parentheses('w AND (w AND )')
    False
    """
    op_re1 = r'\&|\||AND|OR|BUT\sNOT|NOT|\~|\,|NEAR\d{1,3}|WITHIN\d{1,3}'
    oppa_re = re.compile('(\(\s*(%s))|((%s)\s*\))' % (op_re1, op_re1))
    if re.search(oppa_re, input_string) is None:
        return True
    else:
        return False


def word_parentheses(input_string):
    """
    This function checks if a search token or an exact phrase directly precedes an opening parenthesis
    or if a search token is directly followed by a closing parenthesis.
    :param input_string: raw input string.
    :return: Boolean
    >>> word_parentheses('w OR ( w AND w)')
    True
    >>> word_parentheses('w OR w ( w AND w)')
    False
    >>> word_parentheses('w OR w (w AND w)')
    False
    >>> word_parentheses('w OR ( w AND w) w')
    False
    >>> word_parentheses('w OR w ( w AND w)w')
    False
    """
    # incomplete
    input_string = '  ' + input_string + '  '
    op_re1 = r'((?<!AND)(?<!OR)(?<!NOT)(?<!NEAR\d)(?<!NEAR\d\d)' \
             r'(?<!NEAR\d\d\d)(?<!WITHIN\d)(?<!WITHIN\d\d)(?<!WITHIN\d\d\d)(?<!\s\s))'
    op_re2 = r'((?!AND)(?!OR)(?!NOT)(?!NEAR\d)(?!NEAR\d\d)' \
             r'(?!NEAR\d\d\d)(?!WITHIN\d)(?!WITHIN\d\d)(?!WITHIN\d\d\d)(?!\s\s))'
    wopa_re = re.compile('%s\s*\(|\)\s*%s' % (op_re1, op_re2))
    if re.search(wopa_re, input_string) is None:
        return True
    else:
        return False


def quotation_marks(input_string):
    """
    This function checks if all opening quotation marks also close.
    :param input_string: raw input string.
    :return: Boolean
    >>> quotation_marks('"w w" OR "w w w" AND "w w w"')
    True
    >>> quotation_marks('"w w" OR "w w w" AND "w w')
    False
    """
    qcounter = 0
    for char in input_string:
        if char == '"':
            qcounter += 1
    if qcounter % 2 != 0:
        return False
    else:
        return True


def exact_phrase_operators(input_string):
    """
    This function checks if there are any operators within quotation marks.
    :param input_string: raw input string.
    :return: Boolean.
    >>> exact_phrase_operators('w AND w OR "w w w" NOT "w w"')
    True
    >>> exact_phrase_operators('w AND w OR "w NOT w"')
    False
    >>> exact_phrase_operators('w AND w OR "w WITHIN345 w"')
    False
    """
    op_re1 = r'\&|\||AND|OR|BUT\sNOT|NOT|\~|\,|NEAR\d{1,3}|WITHIN\d{1,3}'
    regex = re.compile(r'(".*(\&|\||AND|OR|BUT\sNOT|NOT|\~|\,|NEAR\d{1,3}|WITHIN\d{1,3}).*")*?')
    if re.search(regex, input_string) is None:
        return True
    else:
        print(re.search(regex, input_string))
        return False


def run(input_string):
    """
    This function takes the input string and runs all tests.
    :param input_string: Raw input string from search box.
    :return: Error message.
    """
    pass

if __name__ == '__main__':
    doctest.testmod()