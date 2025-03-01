'''
Bloom Filters
These are a fast set data structure based on hash tables that allow for easy inserts and lookups.
1) Get k random hash functions
2) Hash an item with each function to get different locations in a bitstring of zeros
3) Flip the given locations to ones.
To lookup, see if all the prescribed locations have been flipped.
This gives the probability of a false posative at (1-e^(-kn/m))^k, where n is the number of items and m is the number of bits.
It is impossible to have a false negative.
'''

from universal_family_hash_function import *
import math

class BloomFilter:
    def __init__(self, nbits, nhash):
        self.bits = [False]*nbits # Initialize all bits to False
        self.m = nbits
        self.k = nhash
        # get k random hash functions
        self.hash_fun_reps = [get_random_hash_function() for ii in range(self.k)]
    
    # Function to insert a word in a Bloom filter.
    def insert(self, key):
        
        for function in self.hash_fun_reps:
            if type(key) == str:
                bit = hash_string(function, key) % self.m
            else:
                bit = hashfun(function, key) % self.m
            if self.bits[bit] == False:
                self.bits[bit] = True
        
    # Check if a key belongs to the Bloom Filter
    def member(self, key):
        for function in self.hash_fun_reps:
            if type(key) == str:
                bit = hash_string(function, key) % self.m
            else:
                bit = hashfun(function, key) % self.m
            if self.bits[bit] == False:
                return False
        return True

def calculateBloomFilterInputs(n, p):
    # n is the expected number of elements that the bloom filter will count
    # p is the desired probability of false positives
    # returns a tuple of (m, k)
    # m is the number of bits used in the filter
    # k is the number of hash functions needed
    m = int((-n * math.log(p)) / (math.log(2) ** 2))
    k = int((m / n) * math.log(2))
    return (m, k)