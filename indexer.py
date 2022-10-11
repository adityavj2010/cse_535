'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict
N = 5000

class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        
        total_tokens = 0
        for _,val in tokenized_document:
            total_tokens+=val
        for t in tokenized_document:
            self.add_to_index(t, doc_id,total_tokens)

    def add_to_index(self, term_, doc_id_,total_tokens):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        term,cnt = term_
        if term not in self.inverted_index:
            self.inverted_index[term] = LinkedList()
        
        self.inverted_index[term].insert_at_end((doc_id_,cnt/total_tokens))

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        # self.inverted_index['hydroxychloroquin'].add_skip_connections()
        for ll in self.inverted_index.values():
            ll.add_skip_connections()

    def calculate_tf_idf(self):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        for ll in self.inverted_index.values():
            nodes = ll.traverse_list()
            doc_f = len(nodes)
            idf = N/doc_f
            for node in nodes:
                node.tf_idf*=idf
