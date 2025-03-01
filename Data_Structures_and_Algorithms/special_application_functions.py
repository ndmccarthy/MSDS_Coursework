from search_functions import maxElement,minElement
from fast_fourier_transforms import polynomial_multiply

# Maximum Subarray Problem
def findMaxSubarray(arr,low,high):
    # This divide and conquer iteration runs in nlogn time.
    if high == low:
        return (low,high,0)
    elif high == low+1:
        return (low,high,max(arr[high]-arr[low],0))
    else:
        mid = (low+high)//2
        left_results = findMaxSubarray(arr,low,mid)
        right_results = findMaxSubarray(arr,mid+1,high)
        right_max_elt = maxElement(arr,mid+1,high)
        left_min_elt = minElement(arr,low,mid)
        cross_diff = right_max_elt[1] - left_min_elt[1]
        left_diff = left_results[2]
        right_diff = right_results[2]
        max_diff = max(left_diff,right_diff,cross_diff)
        if max_diff == left_diff:
            return left_results
        elif max_diff == right_diff:
            return right_results
        else:
            return (left_min_elt[0],right_max_elt[0],cross_diff)

def maxSubArray(arr):
    # This iterative approach runs in n time.
    # This function was created as part of a project for Dynamic Programming Week 1.
    # It only outputs the difference of the max subarray, not the indices or elements that create it.
    n = len(arr)
    if n == 1:
        return 0
    low = 0
    high = 0
    max_diff = float('-inf')
    for ii in range(n):
        if arr[ii] < arr[low]:
            low = ii
            high = ii
        elif arr[ii] > arr[high]:
            high = ii
        diff = arr[high] - arr[low]
        if diff > max_diff:
                max_diff = diff
    return max_diff


def check_sum_exists(set_a, set_b, set_c, max_num):
    # return True if there exist n1 in a, n2 in B such that n1+n2 in C
    # return False otherwise
    # max_num signifies the maximum number in a, b, c
    # runs in nlogn time
    
    # STEP 1: Convert set_a and set_b into polynomials.
    # Make an array of length max_num filled with 0 for each set, then add 1s where the numbers are present in the original sets.
    # This makes it easy to determine whether a coefficient exists and does not add coefficients larger than 1 which can create incorrect solutions.
    a_coeffs = [0]*max_num
    b_coeffs = [0]*max_num
    for num in set_a:
        a_coeffs[num] = 1
    for num in set_b:
        b_coeffs[num] = 1

    # STEP 2: Multiply set_a and set_b.
    print("a_coeffs . ", a_coeffs)
    print("b_coeffs . ", b_coeffs)
    c_coeffs = polynomial_multiply(a_coeffs, b_coeffs)
    print("Co-efficients of the testcase are")
    coeffs_copy = []
    for num in c_coeffs:
        if(abs(num-0) < abs(num-1)):
            coeffs_copy.append(0)
        elif(abs(num-1) < abs(num-2)):
            coeffs_copy.append(1)
        else:
            coeffs_copy.append(2)
    print(coeffs_copy)
    
    # STEP 3: Check if there is a match between set_c and the product of set_a and set_b.
    # If the product of set_a and set_b exists for the same number in set_c, then there exists n1 in a, n2 in B such that n1+n2 in C.
    for num in set_c:
        if num <= max_num and coeffs_copy[num] > 0:
            return True
    return False
 
def fixPixelValues(px):
    # convert the RGB values into floating point to avoid an overflow that will give me wrong answers
    return [ float(px[0]), float(px[1]), float(px[2]) ]

def getSortedRank(a):
    # Return a list rank of the same size of a
    # rank[j] = i means that a[i] must be the j^th element in sorted order.
    n = len(a)
    a_marked = []
    r = [None]*(n)
    for id in range(n):
        elt = a[id]
        a_marked.append((elt, id))
    a_marked = sorted(a_marked)
    for id in range(n):
        tup = a_marked[id]
        (elt, og_idx) = tup
        r[og_idx] = id
    return r

def findMinAbsDiff(a=list):
    # minimizes the absolute difference between a[i] and a[j], where i < j
    # returns tuple (i, j)
    assert (len(a) > 2)
    diff = float('inf')
    ii = 0
    jj = 1
    first_id = ii
    sec_id = jj
    order = getSortedRank(a)
    while ii < len(a)-1:
        jj = ii + 1
        ii_id = order.index(ii)
        ii_elt = a[ii_id]
        jj_id = order.index(jj)
        jj_elt = a[jj_id]
        if ii_elt == jj_elt:
            return (ii_id, jj_id)
        tmp_diff = abs(ii_elt-jj_elt)
        if tmp_diff < diff:
            diff = tmp_diff
            if ii_id < jj_id:
                first_id, sec_id = ii_id, jj_id
            else:
                first_id, sec_id = jj_id, ii_id
        ii += 1
    return (first_id, sec_id)

def returnAllCommonElements(list_of_lists):
    # returns a set of the elements that occur in every list
    # each list is the same size
    # initialize results set
    current_results = set(list_of_lists[0]) # get rid of items as you loop through lists
    # look through every element of every list
    for lst in list_of_lists:
        new_results = set()
        for item in lst:
            if item in current_results:
                new_results.add(item)
        current_results = new_results
    return current_results

def findCommonSorted(list1, list2):
    # find the common elements between two sorted lists
    # initialize results and counters for lists
    results = []
    ii = 0
    jj = 0
    while ii < len(list1) and jj < len(list2):
        if list1[ii] == list2[jj]:
            results.append(list1[ii])
            ii += 1
            jj += 1
        elif list1[ii] > list2[jj]:
            jj += 1
        else:
            ii += 1
    return results

def findAllCommonElementsSorted(list_of_lists):
    assert len(list_of_lists) >= 2
    # same input and results as returnAllCommonElements, except the lists are all sorted
    results = list_of_lists[0]
    for lst in list_of_lists:
        results = findCommonSorted(results, lst)
    return results

def findMinContainingInterval(list1, list2):
    # Finds the interval [low, high] that is the smallest and both lists have at least one element within the interval
    # Assume a1, a2 are sorted
    # Return a tuple (lo, hi) of the interval.
    assert len(list1) > 0
    assert len(list2) > 0
    # initialize results and counters for lists
    lo = float('-inf')
    hi = float('inf')
    diff = hi-lo
    ii = 0
    jj = 0
    while ii < len(list1) and jj < len(list2) and diff != 0:
        elt1 = list1[ii]
        elt2 = list2[jj]
        tmp_diff = abs(elt1 - elt2)
        if tmp_diff < diff:
            diff = tmp_diff
            lo = min(elt1, elt2)
            hi = max(elt1, elt2)
            ii += 1
            jj += 1
        elif elt1 < elt2:
            ii += 1
        else:
            jj += 1
    return (lo, hi)