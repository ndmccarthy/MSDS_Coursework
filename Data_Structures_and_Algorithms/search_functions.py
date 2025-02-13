# Binary Search
# This algorithm requires you input a sorted list.
def binarySearch(lst, term, left, right):
    if left > right:
        return (False, "None")
    else:
        mid = (left + right)//2
        if lst[mid] == term:
            return (True, mid)
        else:
            if lst[mid] < term:
                return binarySearch(lst, term, mid+1, right)
            else:
                return binarySearch(lst, term, left, mid-1)

# Maximum and Minimum Elements
def maxElement(arr,left,right):
    max_elt = arr[left]
    max_index = 0
    if left != right:
        for ii in range(left+1,right+1):
            if arr[ii] > max_elt:
                max_elt = arr[ii]
                max_index = ii
        return (max_index, max_elt)
    else:
        return (left,arr[left])

def minElement(arr,left,right):
    min_elt = arr[left]
    min_index = 0
    if left != right:
        for ii in range(left+1,right+1):
            if arr[ii] < min_elt:
                min_elt = arr[ii]
                min_index = ii
        return (min_index, min_elt)
    else:
        return (left,arr[left])

# Search
def searchArray(array, v):
    for jj in range(len(array)):
        if v == array[jj]:
            print("{} is in this array at location {}.".format(v,jj))
            break
        else:
            if jj == len(array)-1:
                print("{} is not in this array.".format(v))