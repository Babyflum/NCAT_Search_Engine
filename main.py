import preprocessor
import searcher
import pickle
from parse_tree import ParseTree
# import statistics_container as stat
# import time
from pprint import pprint
import re


def unpickle():
    """
    Unpickles Index to be used for search. The result is a regular dictionary that represents the Inverted Index.
    :return: Inverted Index as a dictionary of format:
    {word1: [(ID1, [pos1, pos2,...]), (ID2, [pos1,...]), (...),...],
    word2: [(ID3, [pos1, pos2,...]), (...),...],
    ...,
    wordN: [..., (IDn, [..., posn])}
    """
    # pickle_file = input("Index to be used:")
    pickle_file = '100k_index.pickle'
    pickle_in = open(pickle_file, "rb")
    inverted_index = pickle.load(pickle_in)
    return inverted_index


def run_main(query, ii):
    """
    The main function of the search engine. Takes a query string and returns a list of DocIDs.
    :param query: The search string.
    :param ii: The Inverted Index to be used.
    :return: List of DocID tuples with list of positions (ID, [pos1, pos2,...]).
    """
    query = query.strip()
    if re.match(r'\b\w+\b$', query):
        stats = dict()
        stats[query] = dict()
        stats[query]['Result: '] = ii[query]
        return ii[query], stats
    elif re.match(r'".+?"$', query):
        query = query[1:-1].split()
        return searcher.exact_phrase(query, ii)
    else:
        processed_query = preprocessor.run(query)
        tree = ParseTree()
        tree.generate(processed_query)
        return searcher.run_main(tree.current, ii)


if __name__ == '__main__':
    II = unpickle()
    while True:
        user_input = input('Enter search string: ')
        if user_input == '':
            break
        end_result, stats = run_main(user_input, II)
        pprint(stats)
