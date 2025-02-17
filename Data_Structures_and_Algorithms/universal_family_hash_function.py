# Universal Family Hash Function

from matrix_operations import create_zeroed_matrix
from generate_prime_numbers import isPrime
import random

def return_random_hash_function(rows=int, cols=int):
    # Generate a random m \times n matrix
    # return a random hash function wherein each entry is chosen as 1 with probability >= 1/2 and 0 with probability < 1/2
    hash_function = create_zeroed_matrix(rows, cols)
    for row in range(rows):
        for col in range(cols):
            hash_function[row][col] = random.randint(0,1)
    return hash_function

# Get a random triple (p, a, b) where p is prime and a,b are numbers betweeen 2 and p-1
def get_random_hash_function():
    n = random.getrandbits(64)
    if n < 0: 
        n = -n 
    if n % 2 == 0:
        n = n + 1
    while not isPrime(n, 20):
        n = n + 1
    a = random.randint(2, n-1)
    b = random.randint(2, n-1)
    return (n, a, b)

# hash function for a number
def hashfun(hfun_rep, num):
    (p, a, b) = hfun_rep
    return (a * num + b) % p

# hash function for a string.
def hash_string(hfun_rep, hstr):
    n = hash(hstr)
    return hashfun(hfun_rep, n)    