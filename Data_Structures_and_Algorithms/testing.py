from CNF_SAT import *

print('-- formula 1 --')
f1 = SATInstance(4, [ [ 1, 2, -4], [-2, -3, 1], [-1, -2, -3] ])
(e, t) = solve_formula(f1)
print(e, t)
assert e, 'f1 should be satisfiable'
assert t != None, 'does not return a truth assignment'
assert f1.evaluate(t) == 1, 'Truth assignment does not evaluate to expected value of true'

print('-- formula 2 -- ')
f2 = SATInstance(5, [[1,2,-5],[-4,-2,-1], [1, 3, 5], [-1, -5, -2], [1, 2, -4]])
(e2, t2) = solve_formula(f2)
print(e2, t2)
assert e2, 'f2 must be satisfiable'
assert t2 != None, 'does not return a truth assignment'
assert f2.evaluate(t2) == 1, 'Truth assignment does not evaluate to expected value of true'

print('--formula 3 --')
f3 = SATInstance(5, [[1, 2, -5, -4], [1, 2, -5, 4], [-1], [-2,-5], [5]])
(e3, t3) = solve_formula(f3)
print(e3, t3)
assert not e3, 'f3 is unsatisfiable'
assert t3 == None

print('--formula 4--')
f4 = SATInstance(10, [
  [-1, -5, -4, 8],
  [1, 5, 8, 2],
   [2, 1, 3, 9],
    [-2, 4, 5, 6, -7],
    [-1, 2, -1, 7, 8],
    [2, -3, 1, 4, 9 ],
    [1, 10],
    [-10],
    [1, 5, 8, 3, 10]
])

(e4, t4) = solve_formula(f4)
print(e4, t4)
assert e4, 'f4 must be satisfiable'
assert t4 != None, 'does not return a truth assignment'
assert f4.evaluate(t4) == 1, 'Truth assignment does not evaluate to expected value of true'

print('--formula 5--')
f5 = SATInstance(16,[
     [1, 2], [-2 , -4],[3, 4], [-4, -5], [5, -6], [6, -7], [6, 7], [7, -16],
     [8, -9],[8, -14], [9, 10], [9, -10], [-10, -11], [10, 12], [11, 12], [13, 14],
     [14, -15], [15, 16]])
(e5, t5) = solve_formula(f5)
print(e5, t5)
assert e5, 'f5 is satisfiable'
assert t5 != None
assert f5.evaluate(t5) == 1, 'Truth assignment does not evaluate to expected value of true'

print('All tests passed: 20 points')