import time
import tracemalloc
import random

def generate_random_cnf(num_vars, num_clauses, clause_len=3):
    cnf = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < clause_len:
            var = random.randint(1, num_vars)
            lit = var if random.random() < 0.5 else -var
            clause.add(lit)
        cnf.append(list(clause))
    return cnf
def dpll(clauses, assignment=[]):
    if not clauses: #if no clauses left, formula is satisfied
        return True

    if any([clause == [] for clause in clauses]): #if there's an empty clause, the current assignment leads to a conflict => UNSAT
        return False

    # --- Unit Clause Propagation ---

    unit_clauses = [c[0] for c in clauses if len(c) == 1] #if a clause has only one literal, assign it to True
    while unit_clauses:
        lit = unit_clauses[0] #take the first unit literal
        assignment.append(lit) #add to current set of values
        clauses = simplify(clauses, lit) #simplify clauses based on this set of values
        if clauses is None: #conflict after simplification
            return False
        if not clauses: #all clauses satisfied
            return True

        unit_clauses = [c[0] for c in clauses if len(c) == 1] #look for more unit clauses after simplification

    # --- Pure Literal Elimination ---
    all_literals = [lit for clause in clauses for lit in clause]
    literal_set = set(all_literals)
    pure_literals = [lit for lit in literal_set if -lit not in literal_set]
    for pure_lit in pure_literals:
        assignment = assignment + [pure_lit] # Assign pure literal to True
        clauses = simplify(clauses, pure_lit) # Simplify CNF again
        if clauses is None:
            return False
        if not clauses:
            return True

    for clause in clauses:
        for lit in clause:
            break   #pick the first literal in the first clause
        break

    if dpll(simplify(clauses, lit), assignment + [lit]): #try assigning the literal to True
        return True

    return dpll(simplify(clauses, -lit), assignment + [-lit]) #if that fails, try assigning it to False


def simplify(clauses, lit):
    #simplify the CNF formula based on the assignment of `lit` = True
    new_clauses = []
    for clause in clauses:
        if lit in clause:
            continue  #clause is already satisfied
        if -lit in clause:
            #remove the negated literal from clause
            new_clause = [x for x in clause if x != -lit]
            if not new_clause:
                return None  #clause became empty => conflict
            new_clauses.append(new_clause)
        else:
            #literal not in clause at all => keep the clause as is
            new_clauses.append(clause)
    return new_clauses
'''
cnf = [
    [1, 2],
    [-1, 3],
    [-2, 4],
    [-3, -4],
    [3],
    [4]
]

cnf = [
    [1, 2],
    [3, 4],
    [5, 6],
    [-1, -3],
    [-1, -5],
    [-3, -5],
    [-2, -4],
    [-2, -6],
    [-4, -6]
]

cnf = [
    [1, 2],     
    [-1, 3],
    [-2, 4],
    [-3, 5],
    [-4, 5],
    [-5, 6],
    [6],
    [1]
]
'''
cnf_formula = generate_random_cnf(3, 20)
#----------computation time and memory consumption-------------------
tracemalloc.start()
start_time =  time.perf_counter()
result = dpll(cnf_formula)
end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("SAT" if dpll(cnf_formula) else "UNSAT")
print(f"Time: {(end_time - start_time) * 1000:.3f} ms")
print(f"Memory Usage: {peak / 1024:.2f} KB")
