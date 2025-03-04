'''
CNF-SAT stands for Conjuntive Normal Form Satisfiability.
It contains n boolean variables that are organized in clauses of m literals.
The clauses contain OR statements and are connected by AND statements.
It is possible for the literals to include NOT, which means it expects a False assignment to satisfy it.

This means that the variables must be assigned to True/False in such a way that each clause is satisfied at by at least one of the literals.

Note: 3-CNF-SAT is an NPC problem that is often used to determine whether other problems are NPC.
    The 3 in front means each clause has 3 literals.
'''

from graphs_classes import UndirectedGraph

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

def dpll_algorithm(formula: SATInstance, partial_truth_assign: dict, j: int):
    # return (True, partial_truth_assignment) if the formula is satisfiable
    # return (False, None) if the formula is unsatisfiable. 
    # j is the id of the current variable we are considering
    print("j is "+str(j))
    assert 1 <= j <= formula.n, "Invalid Variable ID"
    assert j not in partial_truth_assign
    T_truth_assign = extend_truth_assignment(partial_truth_assign, j, True)
    T_evaluation = formula.evaluate(T_truth_assign)
    if T_evaluation == 1:
        return True, T_truth_assign
    elif T_evaluation == 0:
        (success, final_truth_assign) = dpll_algorithm(formula, T_truth_assign, j+1)
        if success:
            return True, final_truth_assign
    forget_var_in_truth_assign(partial_truth_assign, j)
    F_truth_assign = extend_truth_assignment(partial_truth_assign, j, False)
    F_evaluation = formula.evaluate(F_truth_assign)
    if F_evaluation == 1:
        return True, F_truth_assign
    elif F_evaluation == 0:
        (success, final_truth_assign) = dpll_algorithm(formula, F_truth_assign, j+1)
        if success:
            return True, final_truth_assign
    return False, None

def solve_formula(formula):
    return dpll_algorithm(formula, {}, 1)

def is_three_coloring(graph: UndirectedGraph, coloring: dict):
    n = graph.vertices
    for ii in range(n):
        if ii not in coloring:
            return False # every vertex must receive a color
        ii_color = coloring[ii]
        if ii_color < 1 or ii_color > 3:
            return False # coloring must be between 1 and 3 inclusive
        edges = graph.adj_list[ii]
        for jj in edges:
            jj_color = coloring[jj]
            if jj_color == ii_color:
                return False
    return True

# create method of encoding variables by node value
def encode(ii: int, clause: list):
    usable = []
    for literal in clause:
        new_lit = abs(literal) + (ii*3)
        if abs(literal) != literal: # if the literal was negative, meaning "NOT"
            new_lit = new_lit * -1
        usable.append(new_lit)
    return usable

def translate_three_coloring(graph: UndirectedGraph):
    # Input: a graph that is an instance of the `UndirectedGraph` class
    # Output: an instance of `SATInstance` that encodes the 3 coloring problem
    n_boolean_vars = graph.vertices * 3 # 3 boolean variables for each vertex
    formula = SATInstance(n_boolean_vars, []) # no clauses yet
    edges = graph.adj_list
    # look at every vertex
    for ii in range(graph.vertices):
        # create clause: vertex i must be colored 1, 2, or 3
        c1 = encode(ii, [1, 2, 3])
        # create clause: vertex i cannot have more than one color
        c2 = encode(ii, [-1, -2])
        c3 = encode(ii, [-2, -3])
        c4 = encode(ii, [-3, -1])
        # add clauses
        formula.add_clause(c1)
        formula.add_clause(c2)
        formula.add_clause(c3)
        formula.add_clause(c4)
        # for every edge (i,j), vertex i and vertex j cannot both have the same color
        for jj in edges[ii]:
            items = [-1, -2, -3]
            ii_coded = encode(ii, items)
            jj_coded = encode(jj, items)
            c5 = [ii_coded[0], jj_coded[0]]
            c6 = [ii_coded[1], jj_coded[1]]
            c7 = [ii_coded[2], jj_coded[2]]
            # add all clauses (encoded) to the formula
            formula.add_clause(c5)
            formula.add_clause(c6)
            formula.add_clause(c7)
    return formula

def extract_graph_coloring_from_truth_assignment(graph: UndirectedGraph, truth_assign: dict):
    # Input: graph --> an instance of UndirectedGraph with n vertices
    #        truth_assign --> dictionary with key in range 1 ... 3*n mapping each key to true/false output from SAT solver.
    # Output: A dictionary mapping vertices 0,..., n-1 to colors {1, 2, 3} 
    # translate truth assignments back to color assignments
    color_assignments = {}
    # iterate through node values
    for ii in range(graph.vertices):
        # retrieve the variables to look for assignments
        variables = encode(ii, [1, 2, 3])
        # only one of these variables should be True, showing an assignment to that color
        for var in variables:
            colored = truth_assign[var]
            if colored:
                # get color number and assign
                color = var - 3*ii
                color_assignments[ii] = color
    return color_assignments
    
def solve_three_coloring(graph):
    s = translate_three_coloring(graph)
    print(s.clauses)
    res, truth_assign = solve_formula(s)
    print(res)
    print(truth_assign)
    if res: 
        return extract_graph_coloring_from_truth_assignment(graph, truth_assign)
    else: 
        return None