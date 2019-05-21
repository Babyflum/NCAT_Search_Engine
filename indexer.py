import re
import pickle
import time
import postings
import gc
# import pprint
import sys

inverted_index = {}
counting_index = {}

def read_file(file_name):
    """
    Reads CSV file and creates dictionary of form
    {ID: (MemberID, Wordlist of PostContent)} called file_dict.

    Then generates Inverted Index.

    >>> ii = InvertedIndex()
    >>> ii.read_file("test.csv")
    >>> ii.file_dict['2']
    ('1', ['How', 'do', 'you', 'charge', 'Per', 'click',
    ... 'Per', 'impression', 'Per', 'hour', 'We', 'charge',
    ... 'for', 'approximate', 'value', 'delivered'])
    >>> ii.inverted_index['How']
    ['2', '3', '4']
    """
    raw_data = open(file_name, mode="r", encoding="utf8")
    file_dict = {}
    andclean = re.compile(r'\&+')
    contractionclean = re.compile(r'[\'`´]+')
    cleanup = re.compile(r'[.?!;:(),/"]+|( - )')
    # f = open('pctest.csv', mode='w')
    for row in raw_data.readlines():
        columns = row.split('\",\"')
        if len(columns) < 9:
            # ignore rows with not enough columns
            pass
        else:
            # remove initial quotation mark
            ID = columns[0][1:]
            postContent = columns[8]
            memberID = columns[5]
            # clean up the post content so that only words are left.
            postContent = re.sub(cleanup, r' ', postContent)
            # contractions like I'm are turned into Im.
            # this is only a temporary solution.
            postContent = re.sub(contractionclean, r'', postContent)
            # ampersands are turned into and.
            postContent = re.sub(andclean, r'and', postContent)
            # whitespaces are singled.
            postContent = re.sub(r'\s+', r' ', postContent)
            # remove leading and trailing whitespaces.
            postContent = postContent.strip()
            file_dict[ID] = (memberID, postContent.split())
            # just for test purposes
            # write into a csv file all of the cleaned up post content.
            # f.write(postContent + ';\n')
    # f.close()
    return file_dict


def generate_index_new(file_dict, casefold=True, nonumbers=True):
    """
    Function that generates a temporary index in memory and once
    it reaches a certain threshold, writes the temporary index
    onto the actual inverted index and deletes the temporary index
    from memory. This should save disk-read and disk_write time.
    """
    tmp_index = dict()
    prefilter = re.compile(r'[^a-zA-Z0-9-]+')
    numberfilter = re.compile(r'[0-9]')
    id_counter = 0
    batchcounter = 1
    for ID in file_dict:
        if id_counter % 10000 == 0:
            print("{} IDs checked".format(id_counter))

        # this part of the code cleans the temporary index
        # all data is stored on disk and the inverted index is updated
        # the temporary index is then deleted from memory and
        # a new temporary index is generated in its stead.
        if id_counter % 100000 == 0:
            batchcounter += 1
            print("BATCH TRANSMISSION Nr.{}".format(batchcounter-1))
            for word in tmp_index:
                if word not in inverted_index:
                    # generate ID, position list tuple
                    path = postings.write_postings(word, tmp_index[word],
                                                   casefold)
                    inverted_index[word] = path
                elif word in inverted_index:
                    lst = postings.read_postings(inverted_index[word], word)
                    # since IDs are sorted in input
                    # this only checks the last added ID
                    lst += tmp_index[word]
                    postings.write_postings(word, lst, casefold)
            del(tmp_index)
            tmp_index = dict()
        
        # pos looks at position of word in wordlist
        pos = 0
        # go through wordlists
        for word in file_dict[ID][1]:
            pos += 1
            if casefold is True:
                word = word.casefold()
            # filter out words which contain non-alphanumeric characters
            # or start or end with a hyphen
            if (re.search(prefilter, word) is not None or len(word) > 20
                    or re.match(r'.+\-$|\-.+', word)):
                continue
            if nonumbers is True:
                if re.search(numberfilter, word) is not None:
                    continue

            # here we increment the counting index
            if word in counting_index:
                counting_index[word] += 1
            else:
                counting_index[word] = 1

            # back to the original function
            if word not in tmp_index:
                # generate ID, position list tuple
                tmp_index[word] = [[ID, [pos]]]
            elif word in tmp_index:
                # since IDs are sorted in input, this only checks the last added ID
                if tmp_index[word][-1][0] == ID:
                    tmp_index[word][-1][1].append(pos)
                else:
                    tmp_index[word].append([ID, [pos]])
        id_counter += 1

    # transmit remaining index
    print("LAST BATCH TRANSMISSION")
    for word in tmp_index:
        if word not in inverted_index:
            # generate ID, position list tuple
            path = postings.write_postings(word, tmp_index[word],
                                           casefold)
            inverted_index[word] = path
        elif word in inverted_index:
            lst = postings.read_postings(inverted_index[word], word)
            # since IDs are sorted in input
            # this only checks the last added ID
            lst += tmp_index[word]
            postings.write_postings(word, lst, casefold)
    del(tmp_index)


def write_file(name):
    """
    Writes .csv file of inverted index.
    Name is string containing name of file to create and write into.
    """
    if name == file_name:
        print("Do not overwrite existing file")
        return None
    else:
        if ".csv" in name:
            name = name
        else:
            name = name + ".csv"
        file = open(name, mode="w")
        for word in inverted_index:
            file.write("{};{}\n".format(word, inverted_index[word]))
        file.close()


def pickle_file(name):
    """
    Pickles (or serializes) hash table in folder for
    easy access by Search Function.
    """

    pickle_out = open("100k_index.pickle", "wb")
    pickle.dump(name, pickle_out)
    pickle_out.close()


if __name__ == "__main__":
    time1 = time.time()
    file_name = input("Name of File to be indexed:")
    print("reading file")
    FD = read_file(file_name)
    print("generating index")
    generate_index_new(FD)
    del(FD)
    time2 = time.time()
    print("pickling index")
    file = open('1Mii.pickle', mode='wb')
    pickle.dump(inverted_index, file)
    file.close()
    print("%.5f seconds" % (time2 - time1))
    print("Size of index: %d" % sys.getsizeof(inverted_index))

    ci_file = open('1Mci.pickle', mode='wb')
    pickle.dump(counting_index, ci_file)
    ci_file.close()
