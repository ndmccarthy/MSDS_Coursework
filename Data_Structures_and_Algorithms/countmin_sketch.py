"""
The Count-Min Sketch gives an approximate count (not necessarily accurate) of items in a list using hashing.
To do this, we must know the size of the list.
1. Use m number of counters.
2. Choose a hash function from a family for each.
3. Hash an item from the list to point to a counter and increment it.
Reduce the error probability by running k counter banks with their own hash functions and use the minimum count from each.
"""

from universal_family_hash_function import get_random_hash_function, hash_string

# Class for implementing a count min sketch "single bank" of counters
class CountMinSketch:
    # Initialize with `num_counters`
    def __init__ (self, num_counters):
        self.m = num_counters
        self.hash_fun_rep = get_random_hash_function()
        self.counters = [0]*self.m

    # given a word, increment its count in the countmin sketch
    def increment(self, word):
        counter = hash_string(self.hash_fun_rep, word) % self.m
        self.counters[counter] += 1
        
    # Given a word, get its approximate count
    def approximateCount(self, word):
        counter = hash_string(self.hash_fun_rep, word) % self.m
        return self.counters[counter]

# Initialize k different counters
def initialize_k_counters(k, m): 
    return [CountMinSketch(m) for ii in range(k)]

# increment each of the individual counters with the word
def increment_counters(count_min_sketches, word):
    for sketch in count_min_sketches:
        sketch.increment(word)
    
# Get the approximate count by querying each counter bank and taking the minimum
def approximate_count(count_min_sketches, word):
    return min([cms.approximateCount(word) for cms in count_min_sketches])