'''
Program that takes the unaltered query and checks whether the preprocessor
can  clean it up, i.e. whether the query is legal.
'''
import re
import doctest

def empty_query(query):
    '''
    Tests for empty query or query containing only whitespaces.
    >>> empty_query("")
    False
    >>> empty_query("   ")
    False
    >>> empty_query("  sad ")
    True
    '''
    pattern = re.compile("\s+")
    if query == "" or pattern.fullmatch(query):
        return False
    else:
        return True

def empty_parentheses(query):
    '''
    Tests whether there are parentheses with no content.
    >>> empty_parentheses("word1 AND () word2")
    False
    >>> empty_parentheses("word1 AND (   )")
    False
    >>> empty_parentheses("word1 AND (word2 AND word3)")
    True
    '''
    if "(" or ")" in query:
        pattern = re.compile("\((\s+|)\)")
        if pattern.search(query):
            return False
        else:
            return True
    else:
        return True

def operator_uniqueness(query):
    '''
    Returns False when operator groups are mixed.
    There are three operator groups.
    1. AND, OR, BUT NOT
    2. &, |, ~
    3. one whitespace, standing for AND; one comma standing for OR
    >>> operator_uniqueness("word1 AND word2 word3")
    False
    >>> operator_uniqueness("word1 & word2 OR word3")
    False
    >>> operator_uniqueness("word1, word2 | word3")
    False
    >>> operator_uniqueness("word1, word2 word3")
    True
    >>> operator_uniqueness("word1 AND word2 BUT NOT word3")
    True
    '''
    pattern = re.compile("()")

def run(query):
    '''
    Main function which runs all other functions sequentially, returning
    either False, if one of the tests does not pass or True, if it does.
    '''
    pass

if __name__ == "__main__":
    doctest.testmod()
