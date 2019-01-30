"""
Module that defines various functions for search.
searcher.run() gets parsed query, options and index as input
and outputs a list of document IDs that fit the criteria.
"""
# import doctest
from parse_tree import ParseTree
import re
from pprint import pprint

operators = ['AND', 'OR', 'BUT NOT']
stats = dict()
query_container = ""


def intersect(left_word, right_word, lws, rws, exact=False):
    """
    Function that computes Intersection (AND operator) of ID Lists for two input words.
    :param left_word: DocID list of left word.
    :param right_word: DocID list of right word.
    :param lws: String representation of left word.
    :param rws: String representation of right word.
    :return: DocID list of intersection of left and right words.
    """
    # lwc = left word counter
    # rwc = right word counter
    # lwc = left word counter
    # rwc = right word counter
    intersection_list = []
    lwc = 0
    rwc = 0
    lw_len = len(left_word)
    rw_len = len(right_word)
    min_len = min(lw_len, rw_len)

    if min_len == lw_len:
        while lwc < min_len and rwc < rw_len:
            # the while loop runs over both lists and stops when
            # the shorter list is done
            if int(left_word[lwc][0]) == int(right_word[rwc][0]):
                intersection_list.append((left_word[lwc][0],
                                          sorted(list(set(
                                              left_word[lwc][1] +
                                              right_word[rwc][1]
                                          )))))
                lwc += 1
                rwc += 1
            elif int(left_word[lwc][0]) < int(right_word[rwc][0]):
                lwc += 1
            else:
                rwc += 1
    else:
        while rwc < min_len and lwc < lw_len:
            # the while loop runs over both lists and stops when
            # the shorter list is done
            if int(left_word[lwc][0]) == int(right_word[rwc][0]):
                intersection_list.append((left_word[lwc][0],
                                          sorted(list(set(
                                              left_word[lwc][1] +
                                              right_word[rwc][1]
                                          )))))
                lwc += 1
                rwc += 1
            elif int(left_word[lwc][0]) < int(right_word[rwc][0]):
                lwc += 1
            else:
                rwc += 1
    if not exact:
        stats['(' + lws + ' AND ' + rws + ')'] = dict()
        stats['(' + lws + ' AND ' + rws + ')']['Results'] = intersection_list
        return intersection_list, '(' + lws + ' AND ' + rws + ')'
    else:
        return intersection_list, ''


def union(left_word, right_word, lws, rws):
    """
    Function that computes union (OR operator) of ID Lists for two input words.
    :param left_word: DocID list of left word.
    :param right_word: DocID list of right word.
    :param lws: String representation of left word.
    :param rws: String representation of right word.
    :return: DocID list of union of left and right words.
    """
    # lwc = left word counter
    # rwc = right word counter
    # lwc = left word counter
    # rwc = right word counter
    union_list = []
    lwc = 0
    rwc = 0
    lw_len = len(left_word)
    rw_len = len(right_word)
    min_len = min(lw_len, rw_len)

    if lw_len == min_len:
        while lwc < min_len and rwc < rw_len:
            # the while loop runs over both lists and stops when
            # the shorter list is done
            if int(left_word[lwc][0]) == int(right_word[rwc][0]):
                union_list.append((left_word[lwc][0],
                                          sorted(list(set(
                                              left_word[lwc][1] +
                                              right_word[rwc][1]
                                          )))))
                lwc += 1
                rwc += 1
            elif int(left_word[lwc][0]) < int(right_word[rwc][0]):
                union_list.append(left_word[lwc])
                lwc += 1
            else:
                union_list.append(right_word[rwc])
                rwc += 1
    else:
        while rwc < min_len and lwc < lw_len:
            # the while loop runs over both lists and stops when
            # the shorter list is done
            if int(left_word[lwc][0]) == int(right_word[rwc][0]):
                union_list.append((left_word[lwc][0],
                                          sorted(list(set(
                                              left_word[lwc][1] +
                                              right_word[rwc][1]
                                          )))))
                lwc += 1
                rwc += 1
            elif int(left_word[lwc][0]) < int(right_word[rwc][0]):
                union_list.append(left_word[lwc])
                lwc += 1
            else:
                union_list.append(right_word[rwc])
                rwc += 1

    # what's left of the longer list, is simply added at the end
    if lwc > rwc:
        union_list += right_word[rwc:]
    elif lwc < rwc:
        union_list += left_word[lwc:]
    else:
        pass

    stats['(' + lws + ' OR ' + rws + ')'] = dict()
    stats['(' + lws + ' OR ' + rws + ')']['Results'] = union_list
    return union_list, '(' + lws + ' OR ' + rws + ')'


def complement(left_word, right_word, lws, rws):
    """
    Function that computes complement (BUT NOT operator) of ID Lists for two input words
    such that the result is the complement of the right word in regards to the left word.
    In other words, if the left word is A and the right word is B, this function computes A\B.
    :param left_word: DocID list of left word.
    :param right_word: DocID list of right word.
    :param lws: String representation of left word.
    :param rws: String representation of right word.
    :return: DocID list of complement of right word in regards to the left word, i.e. all
    elements of the left word list which don't appear in the right word list.
    """
    # lwc = left word counter
    # rwc = right word counter
    # lwc = left word counter
    # rwc = right word counter
    complement_list = []
    lwc = 0
    rwc = 0
    lw_len = len(left_word)
    rw_len = len(right_word)
    min_len = min(lw_len, rw_len)

    if lw_len == min_len:
        while lwc < min_len and rwc < rw_len:
            # the while loop runs over both lists and stops when
            # the shorter list is done
            if int(left_word[lwc][0]) < int(right_word[rwc][0]):
                complement_list.append(left_word[lwc])
                lwc += 1
            elif int(left_word[lwc][0]) == int(right_word[rwc][0]):
                lwc += 1
                rwc += 1
            else:
                rwc += 1
    else:
        while rwc < min_len and lwc < lw_len:
            # the while loop runs over both lists and stops when
            # the shorter list is done
            if int(left_word[lwc][0]) < int(right_word[rwc][0]):
                complement_list.append(left_word[lwc])
                lwc += 1
            elif int(left_word[lwc][0]) == int(right_word[rwc][0]):
                lwc += 1
                rwc += 1
            else:
                rwc += 1

    complement_list += left_word[lwc:]

    stats['(' + lws + ' BUT NOT ' + rws + ')'] = dict()
    stats['(' + lws + ' BUT NOT ' + rws + ')']['Results'] = complement_list
    return complement_list, '(' + lws + ' BUT NOT ' + rws + ')'


def exact_phrase(query, ii):
    """
    Function that computes all docIDs and positions such that the words in the query
    occur exactly one after another.
    :param query: list of words in query in sequential order.
    :param ii: inverted index.
    :return: list of tuples (ID, [pos1,...]) where pos is position of first word in query
    within a given document.
    """
    try:
        result = ii[query[0]]
    except KeyError as w:
        print("{} cannot be found".format(w))
        return [], {}
    for word in query[1:]:
        # first create list of the intersection of all words in query
        # empty is only necessary because of how the intersect function creates
        # a string for the statistics container
        try:
            result, empty = intersect(result, ii[word], "", "", exact=True)
        except KeyError as w:
            print("{} cannot be found".format(w))
            return [], {}
    # create list of intersection IDs only
    result = [x[0] for x in result]
    # final result is list of tuples of form (ID, num), where num is position of first word
    final_result = []
    for ID in result:
        # returns position list of word in given ID
        for num in ii[query[0]][[w[0] for w in ii[query[0]]].index(ID)][1]:
            match = True
            i = 1
            # check if the words in query have positions right after one another
            while match and i < len(query):
                if num + i in ii[query[i]][[w[0] for w in ii[query[i]]].index(ID)][1]:
                    i += 1
                else:
                    match = False
            # only if all positions align do we add to the final list
            if match is True:
                if not final_result:
                    final_result.append((ID, [num]))
                elif final_result[-1][0] == ID:
                    final_result[-1][1].append(num)
                else:
                    final_result.append((ID, [num]))

    if not final_result:
        print("No exact match found")
        return [], {}
    else:
        query = '"' + ' '.join(query) + '"'
        stats[query] = dict()
        stats[query]["results"] = final_result
        return final_result, query


def proximity(first_word, second_word, lws, rws, options, distance):
    """
    Proximity search searches for two words that are within a specified distance from each other.
    The distance between the words is anything from 0 to the specified distance.
    :param first_word: of type docIDList: if option "within", this becomes the first word.
    :param second_word: of type docIDList: if option "within", this becomes the second word.
    :param options: "near" (order doesn't matter) or "within" (order matters)
    :param distance: how many words are in between the first and second word.
    :return: List of docIDs of words for which the conditions are met.
    """
    hash_print = dict()
    final_result = []
    if options == "near":
        # check if words are in the same document
        try:
            doclist, empty = intersect(first_word, second_word, "", "", exact=True)
            assert doclist
            doclist = [w[0] for w in doclist]
        except AssertionError:
            print("No matches found")
            return [], {}

        first_word_doclist = [w[0] for w in first_word]
        second_word_doclist = [w[0] for w in second_word]
        rw_lw = []
        lw_rw = []

        for ID in doclist:
            # returns position list of word in given ID
            for num in first_word[first_word_doclist.index(ID)][1]:
                match = False
                i = 1
                # check if the words in query have positions at most the specified distance
                while i <= distance:
                    if num + i in second_word[second_word_doclist.index(ID)][1]:
                        match = True
                        dist = int(i)
                        i += 1
                    else:
                        i += 1
                # if at least one match is found within the specified distance, we add it to the list
                if match is True:
                    if not final_result:
                        final_result.append((ID, [num]))
                    elif final_result[-1][0] == ID:
                        final_result[-1][1].append(num)
                    else:
                        final_result.append((ID, [num]))
            lw_rw = final_result
            # do the same check the other way around.
            for num2 in second_word[second_word_doclist.index(ID)][1]:
                match = False
                j = 1
                # check if the words in query have positions at most the specified distance
                while j <= distance:
                    if num2 + j in first_word[first_word_doclist.index(ID)][1]:
                        match = True
                        dist = int(j)
                        j += 1
                    else:
                        j += 1
                # if at least one match is found within the specified distance, we add it to the list
                if match is True:
                    if not final_result:
                        final_result.append((ID, [num2]))
                        rw_lw.append((ID, [num2]))
                    elif final_result[-1][0] == ID:
                        final_result[-1][1].append(num2)
                        if not rw_lw:
                            rw_lw.append((ID, [num2]))
                        else:
                            rw_lw[-1][1].append(num2)
                    else:
                        final_result.append((ID, [num2]))
                        rw_lw.append((ID, [num2]))

        hash_print["{} followed by {}".format(rws, lws)] = rw_lw
        hash_print["{} followed by {}".format(lws, rws)] = lw_rw
        stats['(' + lws + ' NEAR' + str(distance) + ' ' + rws + ')'] = dict()
        stats['(' + lws + ' NEAR' + str(distance) + ' ' + rws + ')']['Results'] = final_result
        string_result = '(' + lws + ' NEAR' + str(distance) + ' ' + rws + ')'

    elif options == "within":
        # check if words are in the same document
        try:
            doclist = intersect(first_word, second_word, "", "", exact=True)
            assert doclist
            doclist = [w[0] for w in doclist]
        except AssertionError:
            print("No matches found")
            return [], {}
        first_word_doclist = [w[0] for w in first_word]
        second_word_doclist = [w[0] for w in second_word]
        for ID in doclist:
            # returns position list of word in given ID
            for num in first_word[first_word_doclist.index(ID)][1]:
                match = False
                i = 1
                # check if the words in query have positions positions at most the specified distance
                while i <= distance:
                    if num + i in second_word[second_word_doclist.index(ID)][1]:
                        i += 1
                        match = True
                        distance = int(i)
                    else:
                        i += 1
                # if at least one match is found within the specified distance, we add it to the list
                if match is True:
                    if not final_result:
                        final_result.append((ID, [num]))
                    elif final_result[-1][0] == ID:
                        final_result[-1][1].append(num)
                    else:
                        final_result.append((ID, [num]))
        hash_print["{} followed by {}".format(lws, rws)] = final_result
        stats['(' + lws + ' WITHIN' + str(distance) + ' ' + rws + ')'] = dict()
        stats['(' + lws + ' WITHIN' + str(distance) + ' ' + rws + ')']['Results'] = final_result
        string_result = '(' + lws + ' WITHIN' + str(distance) + ' ' + rws + ')'
    return final_result, string_result


def run(current, ii):
    """
    A Post Order Traversal of the Parse Tree.
    Leaves either return the function exact phrase or the DocID list of a given word.
    Inner Nodes return boolean or proximity operations on two DocID lists.
    All individual actions return DocID lists.
    :param current: The current node in the Parse Tree.
    :param ii: The Inverted Index to be used
    :return: The final DocID list for a given query.
    """
    if not re.search(r'AND|OR|NOT|WITHIN\d{1,3}|NEAR\d{1,3}', current.key):
        if '"' in current.key:
            query_words = current.key[1:-1]
            query_list = query_words.split()
            return exact_phrase(query_list, ii)
        else:
            try:
                stats[current.key] = dict()
                stats[current.key]["results"] = ii[current.key]
                return ii[current.key], current.key
            except KeyError as w:
                print("{} cannot be found".format(w))
                return [], current.key
    else:
        lw, lws = run(current.left, ii)
        rw, rws = run(current.right, ii)
        if current.key == 'AND':
            return intersect(lw, rw, lws, rws, exact=False)
        elif current.key == 'OR':
            return union(lw, rw, lws, rws)
        elif current.key == 'NOT':
            return complement(lw, rw, lws, rws)
        elif re.match(r'WITHIN\d{1,3}', current.key):
            within_num = re.search(r'(?<=WITHIN)\d+', current.key).group()
            return proximity(lw, rw, lws, rws, options='within', distance=int(within_num))
        elif re.match(r'NEAR\d{1,3}', current.key):
            near_num = re.search(r'(?<=NEAR)\d+', current.key).group()
            return proximity(lw, rw, lws, rws, options='near', distance=int(near_num))

def run_main(current, ii):
    stats.clear()
    end_result, empty = run(current, ii)
    return end_result, stats
