"""
This file contains functions and classes used for star search.
Most of it is based around ideas from Manning et al (2009).
In particular it tries out a permuterm solution of wildcard queries.
"""

class PermutermIndex:
    """
    The Permuterm Index is a dictionary that maps any permuterm to its corresponding term.
    lo$hel is mapped to "hello", n$ma is mapped to "man", etc.
    """
    def __init__(self, index=dict(), size=0):
        self.index = index
        self.size = size

    def generate(self, ii):
        """
        Function that generates a Permuterm Index from an Inverted Index.
        It calls Permutermer for each key in the inverted index.
        :param ii: the inverted index to be used.
        :return: no return value. self.index is filled with values.
        >>> PI = PermutermIndex()
        >>> II = {'hello': [1,2,3,4,5], 'man': [3,4,5,6]}
        >>> PI.generate(II)
        >>> cindex = {'ello$h': 'hello', 'llo$he': 'hello', 'lo$hel': 'hello', 'o$hell': 'hello', '$hello': 'hello', 'an$m': 'man', 'n$ma': 'man', '$man': 'man'}
        >>> PI.index == cindex
        True
        """
        for key in ii:
            permuterm_vocabulary = self.permutermer(key)
            for permuterm in permuterm_vocabulary:
                self.size += 1
                self.index[permuterm] = key

    def permutermer(self, term):
        """
        This method generates a permuterm vocabulary for each term.
        For a word like "hello" the permuterm vocabulary contains:
        ['ello$h', 'llo$he', 'lo$hel', 'o$hell', '$hello']
        :param term: input word.
        :return: list of all permuterms.
        >>> PI = PermutermIndex()
        >>> PI.permutermer('hello')
        ['ello$h', 'llo$he', 'lo$hel', 'o$hell', '$hello']
        """
        term = term + '$'
        vocabulary = list()
        for i in range(len(term)-1):
            term = term[1:] + term[0]
            vocabulary.append(term)
        return vocabulary