"""
The preprocessor takes the legal raw input data and returns a list that reflects default binding,
which is then used to generate the parsing tree.
"""

import re
import doctest


def test_parentheses(input_string):
    """
    This function is supposed to take an input string and test whether the parenteses are already
    set. If they are, it removes duplicate parentheses.
    :param input_string: input_string.
    :return: corrected string.
    """
    output_string = re.sub(r'\((\s*?|\s*?")AND\s+', '(', input_string)
    output_string = re.sub(r'\s+AND(\s*?|\s*?")\)', ')', output_string)
    return output_string


def normalize_input(query_input):
    """
    This function takes the raw query and returns a query with normalized operators.
    :param query_input: the raw query.
    :return: The normalized query.
    >>> normalize_input('"word1 word2 word3" AND "word4 word5"')
    '"word1 word2 word3" AND "word4 word5"'
    >>> normalize_input('word1, word2 AND word3 word4 ~ word5')
    'word1 OR word2 AND word3 AND word4 NOT word5'
    >>> normalize_input('"word1 word2" word3| "word4 word5 word6" NOT word7 NEAR7 word8')
    '"word1 word2" AND word3 OR "word4 word5 word6" NOT word7 NEAR7 word8'
    >>> normalize_input('word1 &word2 ~ word3|word4 &  word5&word6| word7 WITHIN15 word8  "word9 word10"')
    'word1 AND word2 NOT word3 OR word4 AND word5 AND word6 OR word7 WITHIN15 word8 AND "word9 word10"'
    """
    # remove trailing spaces
    query_input = query_input.strip()

    # expand whitespaces around parentheses
    query_parentheses = re.sub(r'\(', '( ', query_input)
    query_parentheses = re.sub(r'\)', ' )', query_parentheses)

    # replace all commas and | by OR, replace all ~ and BUT NOT by NOT and all & by AND.
    not_regex = re.compile(r'\s*(?P<not_op>~|BUT\sNOT|NOT)\s*')
    or_regex = re.compile(r'\s*(?P<or_op>\||,|OR)\s*')
    and_regex = re.compile(r'\s*(?P<and_op>\&|AND)\s*')
    query_not = re.sub(not_regex, ' NOT ', query_parentheses)
    query_or = re.sub(or_regex, ' OR ', query_not)
    query_and = re.sub(and_regex, ' AND ', query_or)

    # replace all WITHINn and NEARn by the same but with whitespace around it.
    for match in re.findall(r'NEAR\d{1,3}', query_and):
        query_and = query_and.replace(match, ' NEAR' + re.search(r'\d+', match).group() + ' ')
    for match in re.findall(r'WITHIN\d{1,3}', query_and):
        query_and = query_and.replace(match, ' WITHIN' + re.search(r'\d+', match).group() + ' ')

    # make all whitespaces single
    query_whitespaced = re.sub(r'\s\s+', ' ', query_and)

    # replace whitespaces between search words by AND except for exact phrases
    big_and_regex = re.compile(
        r'((?<!AND)(?<!OR)(?<!NOT)(?<!NEAR\d)(?<!NEAR\d\d)'
        r'(?<!NEAR\d\d\d)(?<!WITHIN\d)(?<!WITHIN\d\d)(?<!WITHIN\d\d\d)(?<!\()(?<!\))\s+'
        r'(?!\))(?!\()(?!AND)(?!OR)(?!NOT)(?!NEAR\d)(?!NEAR\d\d)'
        r'(?!NEAR\d\d\d)(?!WITHIN\d)(?!WITHIN\d\d)(?!WITHIN\d\d\d))')
    query_big_and = " ".join([re.sub(big_and_regex, ' AND ', x)
                              if re.split(r'"', query_whitespaced).index(x) % 2 == 0
                              else '"' + x + '"'
                              for x in re.split(r'"', query_whitespaced)])

    # finish by making whitespaces single again and remove trailing whitespaces
    query_final = re.sub(r'\s\s+', ' ', query_big_and)
    query_final = query_final.strip()

    return query_final


def binding(query):
    """
    This function takes the normalized query and returns a string with default binding.
    :param query: normalized query
    :return: normalized query with parentheses set to default binding.
    """
    if 'NOT' in query:
        num = query.find('NOT')
        query = '( ' + binding(query[:num - 1]) + ' )' + ' NOT ' + '( ' + binding(query[num + 4:]) + ' )'
        return query
    elif 'OR' in query:
        num = query.find('OR')
        query = '( ' + binding(query[:num - 1]) + ' )' + ' OR ' + '( ' + binding(query[num + 3:]) + ' )'
        return query
    elif 'AND' in query:
        num = query.find('AND')
        query = '( ' + binding(query[:num - 1]) + ' )' + ' AND ' + '( ' + binding(query[num + 4:]) + ' )'
        return query
    elif 'NEAR' in query:
        num = query.find('NEAR')
        near_num = re.search(r'(?<=NEAR)\d+(?=\s)', query).group()
        near_dist = len(near_num)
        query = '( ' + binding(query[:num - 1]) + ' )' + ' NEAR' + near_num + ' ( ' + binding(
            query[num + 5 + near_dist:]) + ' )'
        return query
    elif 'WITHIN' in query:
        num = query.find('WITHIN')
        within_num = re.search(r'(?<=WITHIN)\d+(?=\s)', query).group()
        within_dist = len(within_num)
        query = '( ' + binding(query[:num - 1]) + ' )' + ' WITHIN' + within_num + ' ( ' + binding(
            query[num + 7 + within_dist:]) + ' )'
        return query
    else:
        return '&' + query + '&'


def binding_main(query):
    query = binding(query)
    query = re.sub(r'\(\s&|&\s\)', '', query)
    return query


def alternate_binding(input_string):
    """
    This function takes the input string and checks whether parentheses are already set.
    If there are it conducts the default binding in such a way that the preferred binding
    is not changed. Otherwise it simply returns the default binding.
    :param input_string: Normalized query of type string.
    :return: Query with correct binding of type string.
    """
    plevel = 0
    opindex = []
    cpindex = []
    index_pairs = []
    strc = 0
    # First, we count how many opening and closing parentheses are on a given level.
    # In a string such as (...)...(..(...)..) we have two parentheses pairs on the highest level
    # and one within two parentheses, i.e. a lower level.
    while strc < len(input_string):
        if input_string[strc] == '(':
            plevel += 1
            if plevel == 1:
                opindex.append(strc)
        if input_string[strc] == ')':
            plevel -= 1
            if plevel == 0:
                cpindex.append(strc)
                index_pairs.append((opindex[0], cpindex[-1]))
                opindex = opindex[1:]
                cpindex = cpindex[:-1]
        strc += 1
    # if the loop does not count any parentheses on a given level, it returns the default binding.
    if not index_pairs:
        result_string = binding_main(input_string)
    # else it recursively calls alternate_binding on all strings within the parentheses.
    else:
        q_terms = []
        result_string = ''
        start = 0
        for pair in index_pairs:
            result_string += input_string[start:pair[0] + 2]
            alternate_string = alternate_binding(input_string[pair[0] + 2:pair[1] - 1])
            q_terms.append(['( ' + alternate_string + ' )', len(alternate_string) + 4])
            result_string += alternate_string
            start = pair[1] - 1
        result_string += input_string[start:]
        for term in q_terms:
            # In a string like ...(...)... the parentheses and everything within
            # is replaced by #. Default binding is done on the resulting string.
            result_string = result_string.replace(term[0], '#' * term[1])
        result_string = binding_main(result_string)
        for term in q_terms:
            # Finally the original string is put back in place.
            result_string = result_string.replace('#' * term[1], term[0], 1)
    return result_string


def generate_list(query):
    """
    This function takes the input with parentheses and gives back a list for further use by the ParseTree.
    :param query: normalized query with correct binding.
    :return: List containing as elements parentheses, words, exact phrases and operators.
    """
    result_list = []
    temp_list = [x.split()
                 if re.split(r'"', query).index(x) % 2 == 0
                 else ['"' + x + '"']
                 for x
                 in re.split(r'"', query)]
    for x in temp_list:
        result_list += x
    return result_list


def run(query):
    normalized_query = normalize_input(query)
    binding_query = alternate_binding(normalized_query)
    query_list = generate_list(binding_query)
    return query_list


if __name__ == '__main__':
    doctest.testmod()
    test_all = '(w1 & w2 | w3 | w4) NEAR7w5 ~ (w6 WITHIN8w7 & w8) & (w9 | w10)'
    test_all2 = '(w1 & w2 | w3 | w4) NEAR7(w5 ~(w6 WITHIN8w7)& w8)& w9 | w10'
    test_all3 = '(w1 & w2 | w3 | w4) NEAR7 (w5 ~(w6 WITHIN8 "w7 w8")& w8)& "w9 w10" | w10'
    test_all4 = '(w1 & w2  w3  w4) NEAR7 (w5 ~(w6 WITHIN8 "w7 w8")& w8)& "w9 w10" | w10'

    print(run(test_all))
    print(run(test_all2))
    print(run(test_all3))
    print(run(test_all4))
