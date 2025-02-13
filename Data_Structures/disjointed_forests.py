"""
Union Find Data Structures

These are used to keep track of disjoint forests of trees. It is especially helpful for determining minimal spanning trees (MSTs).
Union by rank is also used to create trees that avoid linked lists.
"""

from graphs import WeightedUndirectedGraph

class DisjointForests:
    def __init__(self, nodes):
        # the disjoint forest represents a preset number of nodes in existence with the indices available in lists of parents and rank
        assert nodes >= 1, 'Empty disjoint forest is disallowed'
        self.nodes = nodes
        self.parents = [None]*nodes
        self.rank = [None]*nodes
        
    def dictionary_of_trees(self):
        # converts the disjoint forest structure into a dictionary of trees
        # keys are representative nodes and they map to a set of nodes that are in their tree
        trees = {}
        for node in range(self.nodes):
            if self.is_representative(node):
                trees[node] = set(node)
            if self.parents[node] != None:
                root = self.find(node)
                assert root in trees
                trees[root].add(node)
        return trees
    
    def make_set(self, vertex):
        # creates a tree by making a vertex representative
        assert 0 <= vertex < self.nodes
        assert self.parents[vertex] == None, 'You are calling make_set on an element multiple times -- not allowed.'
        self.parents[vertex] = vertex
        self.rank[vertex] = 1
        
    def is_representative(self, vertex):
        return self.parents[vertex] == vertex 
    
    def get_rank(self, vertex):
        return self.rank[vertex]
    
    def find(self, vertex):
        # finds the representative node for the given vertex
        assert 0 <= vertex < self.nodes
        assert self.parents[vertex] != None, 'You are calling find on an element that is not part of the family yet. Please call make_set first.'
        # traverse parent pointer until reach a root
        parent = self.parents[vertex]
        change_parent = []
        while self.is_representative(parent) == False:
            change_parent.append(parent)
            parent = self.parents[parent]
        # change entry in parents list so they all point directly to the represenative
        for node in change_parent:
            if self.parents[node] != parent:
                self.parents[node] = parent
        return parent
    
    def union(self, node, vertex):
        assert 0 <= node < self.nodes
        assert 0 <= vertex < self.nodes
        assert self.parents[node] != None
        assert self.parents[vertex] != None
        # find the representatives of each
        node_rep = self.find(node)
        vertex_rep = self.find(vertex)
        # if reps are not the same, find higher ranked root
        if node_rep != vertex_rep:
            node_rank = self.get_rank(node_rep)
            vertex_rank = self.get_rank(vertex_rep)
            # change rank of root (node_rep) if ranks were the same
            if node_rank == vertex_rank:
                self.rank[node_rep] += 1
                node_rank = self.get_rank(node_rep)
            highest_rank = max(node_rank, vertex_rank)
            if node_rank == highest_rank:
                root = node_rep
                child = vertex_rep
            else:
                root = vertex_rep
                child = node_rep
            # change child's parent to root
            self.parents[child] = root