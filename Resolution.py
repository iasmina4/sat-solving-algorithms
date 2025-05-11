import time
import tracemalloc

def resolution(clauses):
    clauses = [frozenset(clause) for clause in clauses] # Convert each clause to a frozenset so they are hashable and can be used in sets
    new_clauses = set(clauses)
    active_clauses = set(clauses)

    while True:
        # Generate all possible resolvents
        resolvents = set()
        for ci in active_clauses: # Try resolving each pair of active clause and known clause
            for cj in new_clauses:
                if ci == cj: # Skip resolving a clause with itself
                    continue
                for res in resolve(ci, cj):
                    if not res:  # Found empty clause
                        return False  # => UNSAT
                    resolvents.add(res)

        if resolvents.issubset(new_clauses):   # If no new resolvents were found => all resolvable clauses have been explored
            return True  # SAT

        # Update clause sets
        new_resolvents = resolvents - new_clauses
        if not new_resolvents:
            return True  # SAT

        active_clauses = new_resolvents
        new_clauses.update(new_resolvents)


def resolve(ci, cj):
    #Resolve two clauses and return all possible resolvents
    resolvents = []
    for lit in ci:
        if -lit in cj:  # Combine both clauses and remove the complementary literals (lit and -lit)
            new_clause = (ci | cj) - {lit, -lit}
            resolvents.append(new_clause)
    return resolvents


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
#----------computation time and memory consumption-------------------
tracemalloc.start()
start_time =  time.perf_counter()
result = resolution(cnf)
end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()


print("UNSAT" if not resolution(cnf) else "SAT")
print(f"Time: {end_time - start_time:.6f} seconds")
print(f"Memory Usage: {peak / 1024:.2f} KB")
