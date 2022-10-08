'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip = None
        self.tf_idf = 0


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            """ Write logic to traverse the linked list.
                To be implemented."""
            head = self.start_node
            while head:
                traversal.append(head)
                head = head.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            head = self.start_node
            while head:
                traversal.append(head)
                head = head.skip
            return traversal

    def add_skip_connections(self):
        if self.length<=2:
            return
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        skip_node = self.start_node
        head = self.start_node
        self.skip_length = 0
        while head:
            skip = head
            finished = False
            for i in range(n_skips+1):
                if skip:
                    skip = skip.next
                else:
                    finished = True
                    break
            if finished:
                return
            head.skip = skip
            head = head.skip
            self.skip_length+=1
        # if n_skips>0:
        #     for i in range(n_skips):
        #         if skip_node.next:
        #             skip_node = skip_node.next
        # else:
        #     return
        # self.skip_length = 0
        # while head and skip_node:
        #     head.skip = skip_node
        #     self.skip_length+=1
        #     for i in range(n_skips):
        #         if skip_node and head:
        #             skip_node = skip_node.next
        #             head = head.next
        #         else:
        #             return

        

    def insert_at_end(self, value):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        
            
        _value,cnt = value
        end_node = Node(_value)
        end_node.tf_idf = cnt
        if not self.start_node:
            self.start_node = end_node
            self.end_node = end_node
        else:                
            self.end_node.next = end_node
            self.end_node = end_node
        self.length+=1
