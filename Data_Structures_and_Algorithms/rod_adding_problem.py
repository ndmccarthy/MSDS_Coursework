"""
You are given a list of 𝑛 rods of various lengths as a list [1[0], l[1],...,l[n-1]].
Your job is to attach the rods in some order to make a single rod of length  𝚕[𝟶]+𝚕[𝟷]+⋯+𝚕[𝚗⎯𝟷].
However, if you attach two rods of length  ℓ,𝑚, you have to pay a cost  ℓ+𝑚.
"""
import heapq

def findOptimalJoiningCost(lengths: list):
    # initialize cost counter
    cost = 0
    # make the lengths list into a heap
    heapq.heapify(lengths)
    # work through the heap until there is one item left
    while len(lengths) > 1:
        # extract the minumum item from the heap (twice)
        rod1 = heapq.heappop(lengths)
        rod2 = heapq.heappop(lengths)
        # add the items together, then add their sum to the cost and insert the sum back into the heap
        new_rod = rod1 + rod2
        cost += new_rod
        heapq.heappush(lengths, new_rod)
    return cost