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

def dp(clauses):
    # Convert to sets and get all variables
    clauses = [frozenset(clause) for clause in clauses]
    clause_set = set(clauses)
    symbols = {abs(lit) for clause in clauses for lit in clause}

    while symbols:
        # Select the next variable to eliminate
        x = None
        for s in symbols:
            if any(s in clause or -s in clause for clause in clauses):
                x = s
                break
        if x is None:  # No variables left in clauses
            break

        symbols.remove(x)   # Remove the selected symbol from future consideration

        # Split clauses into positive, negative and others(clauses unaffected by x)
        pos = [c for c in clauses if x in c]
        neg = [c for c in clauses if -x in c]
        others = [c for c in clauses if x not in c and -x not in c]

        resolvents = set()   # Generate resolvents by resolving each positive clause with each negative clause
        for a in pos:
            for b in neg:
                res = frozenset((a | b) - {x, -x})
                if not res:
                    return False
                resolvents.add(res)

        clause_set = set(others) | resolvents
        if not clause_set:
            return True

    return True  # SAT

# ------------------ CNF Formula --------------------
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
cnf_formula = generate_random_cnf(3, 10)
#----------computation time and memory consumption-------------------
tracemalloc.start()
start_time =  time.perf_counter()
result = dp(cnf_formula)
end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("SAT" if result else "UNSAT")
print(f"Time: {(end_time - start_time) * 1000:.3f} ms")
print(f"Memory Usage: {peak / 1024:.2f} KB")

