'''
CNF-SAT stands for Conjuntive Normal Form Satisfiability.
It contains n boolean variables that are organized in clauses of m literals.
The clauses contain OR statements and are connected by AND statements.
It is possible for the literals to include NOT, which means it expects a False assignment to satisfy it.

This means that the variables must be assigned to True/False in such a way that each clause is satisfied at by at least one of the literals.

Note: 3-CNF-SAT is an NPC problem that is often used to determine whether other problems are NPC.
    The 3 in front means each clause has 3 literals.
'''

class SATInstance:
    # Constructor: provide n the number of variables and an initial list of clauses.
    # Note that variable numbers will go from 1 to n inclusive.
    def __init__(self, n, clauses):
        self.n = n
        self.m = len(clauses)
        self.clauses = clauses
        assert self.is_valid()

    # Check if all clauses are correct.
    # literals in each clause must be between 1 and n or -n and -1 
    def is_valid(self):
        assert self.n >= 1
        assert self.m >= 0
        for c in self.clauses:
            for l in c:
                assert (1 <= l and l <= self.n) or (-self.n <= l and l <= -1)
        return True
    
    # Add a new clause to the list of clauses
    def add_clause(self, c):
        #check the clause we are adding.
        for l in c:
            assert (1 <= l and l <= self.n) or (-self.n <= 1 and l <= -1)
        self.clauses.append(c)
    
    # Evaluate a literal against a partial truth assignment
    # return 0 if the partial truth assignment does not have the variable corresponding to the literal
    # return 1 if the partial truth assignment has the variable and the literal is true
    # return -1 if the partial truth assignment has the variable and the literal is false
    def evaluate_literal(self, partial_truth_assignment, literal):
        var = abs(literal) # literal may be negated. First remove any negation using abs
        if var not in partial_truth_assignment:
            return 0
        v = partial_truth_assignment[var]
        if 1 <= literal <= self.n:
            return 1 if v else -1
        else:
            return -1 if v else 1
    
    # since it is partial, we may have variables with no truth assignments.
    # return +1 if the formula is already satisfied under partial_truth_assignment: i.e, all clauses are true
    # return 0 if formula is indeterminate under partial_truth_assignment, all clauses are true or unresolved and at least one clause is unresolved.
    # return -1 if formula is already violated under partial_truth_assignment, i.e, at least one clause is false
    def evaluate(self, partial_truth_assignment):
        # intiate outcome to 1 (base assignment tells that all clauses were satisfied)
        func_outcomes = set()
        # work through each clause
        for clause in self.clauses:
            clause_outcomes = set()
            # retrieve the literals relating to the variables with assignments and evaluate
            for literal in clause:
                lit_outcome = self.evaluate_literal(partial_truth_assignment, literal)
                clause_outcomes.add(lit_outcome)
            # only one True (1) is needed to evaulate a clause as satisfied
            if 1 in clause_outcomes:
                func_outcomes.add(1)
            elif 0 in clause_outcomes:
                func_outcomes.add(0)
            # if there are no Trues (1) or unassigned literals (0), then the clause has been completely evaulated as False (-1)
            else:
                func_outcomes.add(-1)
        # evaluate func_outcomes set to get final result
        # to return False (-1), -1 must exist in the set
        if -1 in func_outcomes:
            return -1
        # to return indeterminate, 0 must exist in the set with no Falses (-1)
        elif 0 in func_outcomes:
            return 0
        # to return True (1), there can only be 1s in the set
        else:
            return 1
        
def extend_truth_assignment(truth_assign, j, b):
    truth_assign[j] = b
    return truth_assign
    
def forget_var_in_truth_assign(truth_assign, j):
    # remove variable from a dictionary
    if j in truth_assign:
        del truth_assign[j]
    return truth_assign

# Implement the DPLL pseudo code with the following modifications
#   return (True, partial_truth_assignment) if the formula is satisfiable
#   return (False, None) if the formula is unsatisfiable. 
# You may use the extend_truth_assignment and forget_var_in_truth_assign functions.
# Remember that a change in a dictionary is reflected back to the caller and this is important to keep in mind.
# Use the evaluate function in SATInstance class to evaluate a formula under partial truth assignment.
def dpll_algorithm(formula, partial_truth_assign, j):
    print("j is "+str(j))
    assert 1 <= j and j <= formula.n
    assert j not in partial_truth_assign
    # your code here
    
    forget_var_in_truth_assign(partial_truth_assign, j)
    return False, None

def solve_formula(formula):
    return dpll_algorithm(formula, {}, 1)
