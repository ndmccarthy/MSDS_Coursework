from binary_search_trees import *

def make_tree(l):
    assert len(l) >= 1
    rootNode = TreeNode(l[0])
    for elt in l[1:]:
        rootNode.insert(elt)
    return rootNode


print('-- Test 1 --')
l = [55, 40, 70, 20, 47, 10, 43, 52, 50, 51]
r = make_tree(l)
path_len = getLongestPathLength(r)
print(path_len)
assert path_len == 7
print('passed')
print('-- Test 2 --')
l = [55, 40, 70, 47,  43, 52, 50, 51]
r = make_tree(l)
path_len = getLongestPathLength(r)
print(path_len)
assert path_len == 7
print('-- Test 3 --')
l = [26, 17, 41, 14, 21, 30, 47, 10, 16, 19, 23, 28, 38, 7, 12, 15, 20, 35, 39, 3]
r = make_tree(l)
path_len = getLongestPathLength(r)
print(path_len)
assert path_len == 10
print('-- Test 4--')
l = [7, 4, 18, 3, 6, 11, 19, 2, 9, 14, 22, 12, 17, 20, 21]
r = make_tree(l)
path_len = getLongestPathLength(r)
print(path_len)
assert path_len == 9
print('All Tests Passed: 15 points!')