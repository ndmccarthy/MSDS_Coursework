from shortest_path import *

def checkPath(width, height, circles, path):
    assert path[0] == (0,0), 'Path must begin at (0,0)'
    assert path[-1] == (width, height), f'Path must end at {(width, height)}'
    (cur_x, cur_y) = path[0]
    for (new_x, new_y) in path[1:]:
        dx = new_x - cur_x
        dy = new_y - cur_y
        assert (dx,dy) in [(1,0),(-1,0), (0,1),(0,-1)]
        assert 0 <= new_x and new_x <= width
        assert 0 <= new_y and new_y <= height
        assert not ptInCircle(new_x, new_y, circles)
        cur_x, cur_y = new_x, new_y
    return
print('-- Test 1 -- ')

circles = [(2,2,0.5), (1,2,1)]
p = findPath(3, 3, circles)
print(p)
checkPath(3, 3, circles, p)
print('-- Test 2 -- ')

circles1 = [(2,2,1), (1,2,1)]
p1 = findPath(3, 3, circles1)
print(p1)
assert p1 == [], 'Answer does not match with ours'

print('-- Test 3 -- ')
p2 = findPath(5,5, circles1)
print(p2)
checkPath(5, 5, circles1, p2)

print('-- Test 4 --')

circles3 = [(1,2,0.5), (2,2,1), (3,3,1),(4,3,1)]
p3 = findPath(5, 5, circles3)
print(p3)
checkPath(5, 5, circles3, p3)

print('-- Test 5 --')
circles5 = [ (4,1, 1), (4,4,1),(2,6,1)]
p5 = findPath(6,6,circles5)
print(p5)
assert p5 == []
print('All tests passed: 15 points!')