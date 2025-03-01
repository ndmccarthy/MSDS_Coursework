from special_application_functions import findMinContainingInterval

from random import randint

def arrayHasEltInInterval(a, l, u):
    assert l <= u
    for elt in a:
        if l <= elt and elt <= u:
            return True
    return False

print('-- Test 1 --')
a1 = [ 1, 4, 8, 9, 14, 15, 18 ]
a2 = [ 5, 10,  19, 23]
(l, u) = findMinContainingInterval(a1, a2)
print(l, u)
assert u -l == 1
assert arrayHasEltInInterval(a1, l, u)
assert arrayHasEltInInterval(a2, l, u)
print('passed')

print('-- Test 2 --')
a1 = [1, 5, 10, 11, 18, 21, 28, 37]
a2 = [ -4, 16, 32, 34]
(l, u) =  findMinContainingInterval(a1, a2)
print(l, u)
assert u - l == 2
assert arrayHasEltInInterval(a1, l, u)
assert arrayHasEltInInterval(a2, l, u)
print('passed')

print('-- Test 3 -- ')
a1 = list(range(0, 100000, 5))
a2 = list(range(257, 1000000, 7))
(l, u) =  findMinContainingInterval(a1, a2)
print(l, u)
assert u - l == 0
assert arrayHasEltInInterval(a1, l, u)
assert arrayHasEltInInterval(a2, l, u)
print('passed')

print('-- Test 4--')
a1 = sorted([ randint(-1000000, 1000000) for i in range(100000)])
a2 = sorted([ randint(0, 1000) for i in range(100)])
(l, u) =  findMinContainingInterval(a1, a2)
print(l, u)
assert arrayHasEltInInterval(a1, l, u)
assert arrayHasEltInInterval(a2, l, u)

print('All Tests Passed: 10 points.')
