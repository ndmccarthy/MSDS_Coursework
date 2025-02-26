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