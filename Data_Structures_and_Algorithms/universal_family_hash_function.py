# Universal Family Hash Function

from matrix_operations import create_zeroed_matrix
import random

def return_random_hash_function(rows=int, cols=int):
    # Generate a random m \times n matrix
    # return a random hash function wherein each entry is chosen as 1 with probability >= 1/2 and 0 with probability < 1/2
    hash_function = create_zeroed_matrix(rows, cols)
    for row in range(rows):
        for col in range(cols):
            hash_function[row][col] = random.randint(0,1)
    return hash_function