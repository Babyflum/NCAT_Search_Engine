import re
import pickle
import time

inverted_index = {}


def read_file(file_name):
    """
    Reads CSV file and creates dictionary of form
    {ID: (MemberID, Wordlist of PostContent)} called file_dict.

    Then generates Inverted Index.

    >>> ii = InvertedIndex()
    >>> ii.read_file("test.csv")
    >>> ii.file_dict['2']
    ('1', ['How', 'do', 'you', 'charge', 'Per', 'click', 'Per', 'impression', 'Per', 'hour', 'We', 'charge', 'for', 'approximate', 'value', 'delivered'])
    >>> ii.inverted_index['How']
    ['2', '3', '4']
    """
    post2 = open(file_name, mode="r", encoding="utf8")
    file_dict = {}
    # format PostContent to accommodate for some errors such as
    # "hey?No, hello!jim, " etc and remove punctuation
    regex = re.compile("([.?!;:(),\[\]]+)(\w)")
    regex2 = re.compile("[.?!;:]+")
    regex3 = re.compile("(\w)([.?!;:(),\[\]]+)")

    for row in post2.readlines():
        # split == ",". Initial " remains
        row = re.sub(regex, r" \2", row)
        row = re.sub(regex3, r"\1 ", row)
        row = re.sub(regex2, "", row)
        row = re.sub(" {2}", " ", row)
        line = row.split("\",\"")
        if len(line) < 9:
            # ignore rows with not enough columns
            pass
        else:
            # initial " removed
            line[0] = line[0][1:]
            # dictionary will be of the form {ID: (MemberID, Wordlist of PostContent)}
            file_dict[line[0]] = (line[5], line[8].split())

    return file_dict


def generate_index(file_dict):
    """
    Generate Inverted Index as dictionary of form
    {'word', list of IDs}.
    >>> fd = {
    '33':('3',['this','is','a','test']),
    '345':('4',['repeat','this','repeat','this])
    '346':('3',['another','test','another','another','another'])
    '556':('4',['this','is','a','repeat','of','this])}
    >>> ii = generate_index(fd)
    >>> print(ii)
    '{'this': [('33', [1]), ('345', [2,4])}'
    """
    for ID in file_dict:
        # pos looks at position of word in wordlist
        pos = 0
        # go through wordlists
        for word in file_dict[ID][1]:
            pos += 1
            if word not in inverted_index:
                # generate ID, position list tuple
                inverted_index[word] = [(ID, [pos])]
            elif word in inverted_index:
                # since IDs are sorted in input, this only checks the last added ID
                if inverted_index[word][-1][0] == ID:
                    inverted_index[word][-1][1].append(pos)
                else:
                    inverted_index[word].append((ID, [pos]))

    return inverted_index


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
    Pickles (or serializes) hash table in folder for easy access by Search Function.
    """

    pickle_out = open("100k_index.pickle", "wb")
    pickle.dump(name, pickle_out)
    pickle_out.close()


if __name__ == "__main__":
    time1 = time.time()
    file_name = input("Name of File to be indexed:")
    FD = read_file(file_name)
    generate_index(FD)
    pickle_file(inverted_index)
    time2 = time.time()
    print("%.5f seconds" % (time2 - time1))
    answer = input("Do you want to write a .csv file of the index? y/n:")

    while True:
        if answer == ("y" or "Y"):
            write_file(input("Name for .csv file:"))
            break
        elif answer != ("n" or "N"):
            answer = input("Please only type in one of the following: y,Y,n,N:")
        else:
            break
    '''
    fd = {
        '33': ('3', ['this', 'is', 'a', 'test']),
        '345': ('4', ['repeat', 'this', 'repeat', 'this']),
        '346': ('3', ['another', 'test', 'another', 'another', 'another']),
        '556': ('4', ['this', 'is', 'a', 'repeat', 'of', 'this', 'and', 'this'])}
    ii = generate_index(fd)

    pprint.pprint(ii)
    '''
