This repository includes three Python-based SAT solvers for CNF formulas: DPLL, DP, and Resolution.

The **DPLL** solver implements unit propagation and pure literal elimination, and uses a splitting heuristic based on the frequency of literal occurrence to choose which variable to branch on. This improves performance by targeting the most "influential" literals first.

The **DP** (Davis–Putnam) algorithm eliminates variables through resolution. For each variable, it generates all possible resolvents between clauses containing the literal and its negation, simplifying the formula until it's solved or a contradiction is found.

The **Resolution** solver repeatedly resolves pairs of clauses to derive new clauses. If an empty clause is derived, the formula is unsatisfiable. If no new clauses can be generated, it's satisfiable.

Each script reports whether the formula is SAT or UNSAT, and includes timing and memory usage statistics.
