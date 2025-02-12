from helper_functions import swap

# Bubble Sort
def bubbleSort(array):
    for ii in range(len(array)):
        for jj in reversed(range(ii+1, len(array))):
            if array[jj] < array[jj-1]:
                array[jj-1],array[jj] = array[jj],array[jj-1]
    return array

# Insertion Sort
def insertSortInc(array):
    for jj in range(1,len(array)):
        key = array[jj]
        ii = jj-1
        while ii >= 0 and array[ii] > key:
            array[ii+1] = array[ii]
            ii -= 1
        array[ii+1] = key
    return array

def insertSortDec(array):
    for jj in range(1,len(array)):
        key = array[jj]
        ii = jj-1
        while ii >= 0 and array[ii] < key:
            array[ii+1] = array[ii]
            ii -= 1
        array[ii+1] = key
    return array

# Merge Sort
def merge(left,right):
    ii = 0
    jj = 0
    mid = len(left)-1
    end = len(right)-1
    result = []
    while ii <= mid and jj <= end:
        if left[ii] <= right[jj]:
            result.append(left[ii])
            ii += 1
        else:
            result.append(right[jj])
            jj += 1
    if ii <= mid:
        result.extend(left[ii:])
    else:
        result.extend(right[jj:])
    return result

def mergeSort(array):
    beg = 0
    end = len(array)-1
    mid = (end//2)+1
    if end <= 0:
        return array
    else:
        left = array[:mid]
        right = array[mid:]
        sorted_left = mergeSort(left)
        sorted_right = mergeSort(right)
        return merge(sorted_left,sorted_right)

# Quicksort
# partitions list using a pivot point recursively

def testIfPartitioned(lst, pivot_id):
    # test if all elements at indices < pivot_id are all <= pivot and all elements at indices > pivot_id are all > pivot
    # return TRUE if the array is correctly partitioned around pivot and return FALSE otherwise
    assert 0 <= pivot_id < len(lst)
    pivot = lst[pivot_id]
    for id in range(pivot_id):
        val = lst[id]
        if val > pivot:
            return False
    for id in range(pivot_id + 1, len(lst)):
        val = lst[id]
        if val <= pivot:
            return False
    return True

def tryPartition(lst):
    # implementation of Lomuto partitioning algorithm
    lst_size = len(lst)
    last_id = lst_size - 1
    pivot = lst[last_id] # choose last element as the pivot.
    ii,jj = -1,0 # initialize ii and jj
    for jj in range(last_id): # jj = 0 to n-2 (inclusive)
        # Invariant: lst[0] .. lst[ii] are <= pivot
        #            lst[ii+1]...lst[jj-1] are > pivot
        if lst[jj] <= pivot: 
            ii += 1
            swap(lst, ii+1, jj)
    swap(lst, ii+1, last_id) # place pivot in its correct place.
    return ii+1 # return the index where we placed the pivot

def simplePartition(arr, pivot):
    # partitions array according to the given pivot
    # track where the first id of the pivot region is
    p_region_start = len(arr)
    # track where the end of region 1 (elts < pivot) is
    region1_end = -1
    # region 2 will always be (region1_end + 1, p_region_start -1)
    # initilize id
    id = 0
    while id < p_region_start:
        elt = arr[id]
        if elt == pivot:
            p_region_start -= 1
            swap(arr, id, p_region_start)
        elif elt < pivot:
            region1_end += 1
            id += 1
        else:
            swap(arr, id, region1_end + 1)
            id += 1
    # place pivot region in correct place in array
    region2_start = region1_end + 1
    for id in range(p_region_start, len(arr)):
        swap(arr, region2_start, p_region_start)
        region2_start += 1
        p_region_start += 1
    return arr
            
def boundedSort(arr, max_val):
    for jj in range(1, max_val):
        simplePartition(arr, jj)