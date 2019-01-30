"""
Module for generating a parse tree for the search string.
"""
from re import match


class TreeElement:
    """
    Generates a Tree Element.
    The key attribute can either be a word, an operator or an exact phrase.
    If the Tree Element is a leaf, the attributes left and right are set to None.
    """
    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        

class ParseTree:
    """
    The ParseTree Object is a tree which organizes the query recursively along the given or default bindings.
    A leaf represents a word or exact phrase to be searched.
    An inner node represents an operator.
    """
    def __init__(self):
        self.root = TreeElement(key=None)
        self.current = self.root

    def insert(self, x):
        """
        The insert method takes a string and creates the Tree.
        If the input is an opening parenthesis, it moves down one branch.
        If the input is a closing parenthesis, it moves up one branch.
        If the input is an operator, it generates an inner node.
        If the input is a word or exact phrase, it generates a leaf.
        :type x: string
        :param x: type string, can either be an opening or closing parenthesis, an operator, a word or an exact phrase.
        :return: None.
        """
        if x == '(':
            if self.current.left is not None:
                self.current.right = TreeElement(None, self.current)
                self.current = self.current.right
            else:
                self.current.left = TreeElement(None, self.current)
                self.current = self.current.left
        elif x == ')':
            self.current = self.current.parent
        elif match(r'AND|OR|NOT|WITHIN\d{1,3}|NEAR\d{1,3}', x):
            self.current.key = x
        else:
            if self.current.key is None:
                self.current.left = TreeElement(x, self.current)
            else:
                self.current.right = TreeElement(x, self.current)

    def generate(self, input_list):
        """
        The generate method calls the insert method over a list of the query.
        :param input_list: A list whose elements are the individual words, exact phrases, parentheses and operators of
        the query.
        :return: None.
        """
        for i in input_list:
            self.insert(i)

    def tree_list(self, node):
        """
        A method used to debug the ParseTree. It generates a recursive list, showing individual nodes as lists of format
        [left child, node key, right child]. If the node is a leaf, the left and right children are None.
        :param node: Tree Element.
        :return: recursive list of nodes.
        """
        if node.left is not None:
            # code to go down parse tree
            return [self.tree_list(node.left)] + [node.key] + [self.tree_list(node.right)]
        else:
            return [None, node.key, None]

    def __str__(self):
        node = self.current
        newexp = self.tree_list(node)
        return str(newexp)


if __name__ == "__main__":
    test = ['(', 'word1', 'AND', 'word2', ')', 'NOT', '(', 'word3', 'OR', '(', '(', 'word4', 'AND', '(', 'word5', 'AND',
            'word6', ')', ')', 'OR', '(', '(', 'word7', 'WITHIN15', 'word8', ')', 'AND', '"word9 word10"', ')', ')', ')'
            ]
    Tree = ParseTree()
    Tree.generate(test)
    print(Tree)