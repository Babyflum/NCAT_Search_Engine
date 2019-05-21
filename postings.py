"""
Organize postings lists according to letters of words.
i.e. the postings list for 'hello' will be in folder
postings/h/he/hel/hell/hello/hello$/hello.txt.
"""
import os
import pickle
import lzma

def retrieve(term, path):
    """
    This function is used by the searcher to quickly retrieve the postings list,
    thus allowing the index to be kept small.
    Quick path retrieval is left to the operating system.
    """
    os.chdir(path)
    file = open(term + '$.dmp', mode='rb')
    postings_list = pickle.load(file)
    file.close()
    return postings_list

def read_postings(path, term):
    """
    Function that reads the postings list of a given term
    """
    os.chdir(path)
    term = term +'$'
    file = open(term + '.dmp', mode='r+b')
    postings_list = pickle.load(file)
    file.close()
    directory = '..'+('/..'*(len(term)))
    os.chdir(directory)
    return postings_list
    
    
def write_postings(term, postings_list, casefold=True, nonumbers=True):
    """
    function that generates a folder for a particular term.
    >>> write_postings('hello')
    >>> blub
    """
    if nonumbers is True:
        os.chdir('./postings_1M')
    elif casefold is True:
        os.chdir('./postings_casefold')
    else:
        os.chdir('./postings')
    term = term +'$'
    for n in range(1, len(term)+1):
        try:
            os.mkdir(term[:n])
            os.chdir(term[:n])
        except FileExistsError:
            os.chdir(term[:n])
    path = os.getcwd()
    file = open(term + '.dmp', mode='wb')
    pickle.dump(postings_list, file)
    file.close()
    directory = '..'+('/..'*(len(term)))
    os.chdir(directory)
    return path
    
    
    


