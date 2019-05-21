"""
This program takes the input from the search box and checks if any mistakes were made.
Illegal queries include:
- Parentheses that were opened were not closed. (u"\u2713")
- Two or more operators next to each other with no search word in between. (u"\u2713")
- Operators right of opening parentheses. (w1 AND(w1..)) works but (w1 (AND w2)..) does not. (u"\u2713")
- Search tokens left of closing parentheses. (for now empty spaces will be treated as AND).
- Exact phrase quotation marks open but do not close. (u"\u2713")
- Operators within an exact phrase (this might be updated in later versions). (u"\u2713")
- WITHIN and NEAR operators without a distance number or with a distance number of more than 3 digits. (u"\u2713")
- Empty query. (u"\u2713")
"""

import re
import doctest


def query_is_empty(input_string):
    """
    This function checks whether the query is empty.
    :param input_string: raw input string.
    :return: Boolean.
    >>> query_is_empty('w AND w')
    True
    >>> query_is_empty('')
    False
    >>> query_is_empty('  ')
    False
    """
    if re.match(r'\A\s*\Z', input_string) is None:
        return True
    else:
        return False


def parentheses_are_uneven(input_string):
    """
    This function checks whether all opening parentheses have corresponding closing parentheses.
    :param input_string: raw input string.
    :return: Boolean.
    >>> parentheses_are_uneven('w (w w) w ((w(w w)w) w )')
    True
    >>> parentheses_are_uneven('w (w w) w ((w(w ww) w )')
    False
    >>> parentheses_are_uneven('w w w) w ((w(w w)w) w )')
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


def operators_with_no_words_in_between(input_string):
    """
    This function checks whether operators are separated by words.
    :param input_string: raw input string
    :return: Boolean.
    >>> operators_with_no_words_in_between('w AND w OR w WITHIN3 (w BUT NOT w) NEAR756 w ~ w, w|w')
    True
    >>> operators_with_no_words_in_between('w AND AND w')
    False
    >>> operators_with_no_words_in_between('w AND w ~ | w')
    False
    >>> operators_with_no_words_in_between('w & w &NEAR76')
    False
    >>> operators_with_no_words_in_between('w WITHIN5 NOT w')
    False
    """
    op_re1 = r'\&|\||AND|OR|BUT\sNOT|NOT|\~|\,|NEAR\d{1,3}|WITHIN\d{1,3}'
    regex = re.compile('(%s)\s*(%s)' % (op_re1, op_re1))
    if re.search(regex, input_string) is None:
        return True
    else:
        return False


def operator_following_opening_parenthesis_or_before_closing_parenthesis(input_string):
    """
    This function checks if an operator follows an opening parenthesis or precedes a closing parenthesis.
    :param input_string: raw input string.
    :return: Boolean.
    >>> operator_following_opening_parenthesis_or_before_closing_parenthesis('w AND (w OR w)')
    True
    >>> operator_following_opening_parenthesis_or_before_closing_parenthesis('w AND (AND word)')
    False
    >>> operator_following_opening_parenthesis_or_before_closing_parenthesis('w AND ( AND word)')
    False
    >>> operator_following_opening_parenthesis_or_before_closing_parenthesis('w AND (w AND)')
    False
    >>> operator_following_opening_parenthesis_or_before_closing_parenthesis('w AND (w AND )')
    False
    """
    op_re1 = r'\&|\||AND|OR|BUT\sNOT|NOT|\~|\,|NEAR\d{1,3}|WITHIN\d{1,3}'
    oppa_re = re.compile('(\(\s*(%s))|((%s)\s*\))' % (op_re1, op_re1))
    if re.search(oppa_re, input_string) is None:
        return True
    else:
        return False


# def word_parentheses(input_string):
#     """
#     This function checks if a search token or an exact phrase directly precedes an opening parenthesis
#     or if a search token is directly followed by a closing parenthesis.
#     :param input_string: raw input string.
#     :return: Boolean
#     >>> word_parentheses('w OR ( w AND w)')
#     True
#     >>> word_parentheses('w OR w ( w AND w)')
#     False
#     >>> word_parentheses('w OR w (w AND w)')
#     False
#     >>> word_parentheses('w OR ( w AND w) w')
#     False
#     >>> word_parentheses('w OR w ( w AND w)w')
#     False
#     """
#     # incomplete
#     # input_string = '  ' + input_string + '  '
#     # op_re1 = r'((?<!AND)(?<!OR)(?<!NOT)(?<!NEAR\d)(?<!NEAR\d\d)' \
#     #          r'(?<!NEAR\d\d\d)(?<!WITHIN\d)(?<!WITHIN\d\d)(?<!WITHIN\d\d\d)(?<!\s\s))'
#     # op_re2 = r'((?!AND)(?!OR)(?!NOT)(?!NEAR\d)(?!NEAR\d\d)' \
#     #          r'(?!NEAR\d\d\d)(?!WITHIN\d)(?!WITHIN\d\d)(?!WITHIN\d\d\d)(?!\s\s))'
#     # wopa_re = re.compile('%s\s*\(|\)\s*%s' % (op_re1, op_re2))
#     # if re.search(wopa_re, input_string) is None:
#     #     return True
#     # else:
#     #     return False
#     pass

def quotation_marks_are_uneven(input_string):
    """
    This function checks if all opening quotation marks also close.
    :param input_string: raw input string.
    :return: Boolean
    >>> quotation_marks_are_uneven('"w w" OR "w w w" AND "w w w"')
    True
    >>> quotation_marks_are_uneven('"w w" OR "w w w" AND "w w')
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


def operators_within_exact_phrase(input_string):
    """
    This function checks if there are any operators within quotation marks.
    :param input_string: raw input string.
    :return: Boolean.
    >>> operators_within_exact_phrase('w AND w OR "w w w" NOT "w w"')
    True
    >>> operators_within_exact_phrase('w AND w OR "w NOT w"')
    False
    >>> operators_within_exact_phrase('w AND w OR "w WITHIN345 w"')
    False
    >>> operators_within_exact_phrase('"w NOT w" OR w NOT w')
    False
    """
    # incomplete
    op_re1 = r'\&|\||AND|OR|BUT\sNOT|NOT|\~|\,|NEAR\d{1,3}|WITHIN\d{1,3}'
    qcount = 0
    strcount = 0
    opqu = 0
    clqu = 0
    for char in input_string:
        if char == '"':
            if qcount == 1:
                clqu = strcount
                qcount -= 1
            else:
                qcount += 1
                opqu = strcount
        if qcount == 0 and strcount != 0:
            if re.search(op_re1, input_string[opqu+1:clqu]) is not None:
                return False
        strcount += 1
    return True


def distance_must_be_between_1_and_999(input_string):
    """
    This function checks whether the NEAR and WITHIN operators have a distance specified.
    The distance is only legal if it is between 1 and 999.
    :param input_string: raw input string.
    :return: Boolean.
    >>> distance_must_be_between_1_and_999('w AND w WITHIN34 w OR w')
    True
    >>> distance_must_be_between_1_and_999('w OR w NEAR999 w')
    True
    >>> distance_must_be_between_1_and_999('w AND w WITHIN w OR w')
    False
    >>> distance_must_be_between_1_and_999('w OR w NEAR w OR w')
    False
    >>> distance_must_be_between_1_and_999('w AND w WITHIN1234 w OR w')
    False
    >>> distance_must_be_between_1_and_999('w OR w NEAR1234 w OR w')
    False
    >>> distance_must_be_between_1_and_999('w AND w WITHIN0 w OR w')
    False
    >>> distance_must_be_between_1_and_999('w AND w NEAR0 w OR w')
    False
    """
    dist_re = re.compile(r'(NEAR|WITHIN)(0|\D|\d{4,})')
    if re.search(dist_re, input_string) is None:
        return True
    else:
        return False


def run(input_string):
    """
    This function takes the input string and runs all tests.
    :param input_string: Raw input string from search box.
    :return: Error message.
    """
    funclist =[query_is_empty,
               parentheses_are_uneven,
               operators_with_no_words_in_between,
               operator_following_opening_parenthesis_or_before_closing_parenthesis,
               quotation_marks_are_uneven,
               operators_within_exact_phrase,
               distance_must_be_between_1_and_999]
    errorcount = 0
    errorlist = []
    for func in funclist:
        if func(input_string) is False:
            errorcount += 1
            errorlist.append("Error: {}".format(func.__name__))
    if errorcount != 0:
        return "{} Errors found.".format(errorcount), errorlist
    else:
        return True, []


if __name__ == '__main__':
    doctest.testmod()