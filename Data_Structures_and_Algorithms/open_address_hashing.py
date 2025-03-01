"""
Open Address Hashing is an important implementation choice for hash tables.
It only allows one entry per table location and handles collisions by giving a different solution.
This solution is found by double hashing. 
Double hashing takes the result of the first hashing and adds the result of a second hashing with a different function.
This is incremented by the result of the second hashing until an open slot is found.
"""

from universal_family_hash_function import createHashFamily, hashfun

class OpenAddressHashTable:
    def __init__(self, size):
        self.tbl = [None]*size
        self.size = size
        self.hash_fam = createHashFamily(2)

    def hashInsert(self, key):
        ii = 0  #counter to see if we've gone through the entire table
        jj = hashfun(self.hash_fam[0], key)
        incr = hashfun(self.hash_fam[1], key)
        while ii <= self.size:
            if self.tbl[jj] == None:
                self.tbl[jj] = key
                break
            jj += incr
            ii += 1
    
    def hashSearch(self, key):
        # returns the index of the desired key, or None if does not exist
        ii = 0  #counter to see if we've gone through the entire table
        jj = hashfun(self.hash_fam[0], key)
        incr = hashfun(self.hash_fam[1], key)
        while ii <= self.size:
            if self.tbl[jj] == None:
                return None
            elif self.tbl[jj] == key:
                return jj
            jj += incr
            ii += 1
        return None

def returnAllUniqueElements(list_of_lists):
    # returns a list that includes each unique number included in the original list of lists
    # each list in the list of lists has the same length
    # initialize a hash table
    n = len(list_of_lists[0])
    htbl = OpenAddressHashTable(n)
    # initialize result list
    result = []
    # iterate through every element of every list
    for lst in list_of_lists:
        for item in lst:
            # check if
            if htbl.hashSearch(item) == None:
                # add the item to both the hash table and the result
                htbl.hashInsert(item)
                result.append(item)
    return result