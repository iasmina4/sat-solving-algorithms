# SAT Solvers: DPLL, DP and Resolution

The **DPLL** algorithm automatically assigns values to variables in unit clauses and simplifies the formula by assigning values to pure literals that appear with only one polarity. For branching, it selects the first literal found in the first clause.

The **DP** (Davis–Putnam) algorithm eliminates variables through resolution. For each variable, it generates all possible resolvents between clauses containing the literal and its negation, simplifying the formula until it's solved or a contradiction is found.

The **Resolution** solver repeatedly resolves pairs of clauses to derive new clauses. If an empty clause is derived, the formula is unsatisfiable. If no new clauses can be generated, it's satisfiable.

Each script reports whether the formula is SAT or UNSAT, and includes timing and memory usage statistics.
