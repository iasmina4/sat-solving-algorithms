import time
import tracemalloc

def dp(clauses):
    # Convert to sets and get all variables
    clauses = [set(clause) for clause in clauses]
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

        resolvents = []    # Generate resolvents by resolving each positive clause with each negative clause
        for a in pos:
            for b in neg:
                # remove x and -x from combined clause
                resolvent = (a | b) - {x, -x}
                if not resolvent:  # Empty clause found
                    return False  # UNSAT
                resolvents.append(resolvent)

        # Update clauses
        clauses = others + resolvents

        # If no clauses remain, formula is satisfied
        if not clauses:
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
#----------computation time and memory consumption-------------------
tracemalloc.start()
start_time =  time.perf_counter()
result = dp(cnf)
end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("SAT" if dp(cnf) else "UNSAT")
print(f"Time: {end_time - start_time:.6f} seconds")
print(f"Memory Usage: {peak / 1024:.2f} KB")