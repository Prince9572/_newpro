# Experiment: Truth Table Generator
# Question: Generate truth tables and evaluate logic expressions.
# Preferably in Python.

import itertools

def truth_table(expr):
    vars = sorted(set(ch for ch in expr if ch.isalpha()))

    print(" | ".join(vars), "|", expr)
    print("-" * (6 * len(vars) + len(expr)))

    for vals in itertools.product([False, True], repeat=len(vars)):
        env = dict(zip(vars, vals))
        result = eval(expr, {}, env)
        print(" | ".join(str(int(env[v])) for v in vars), "|", int(result))

# Example logical expressions
expr1 = "(A and B) or (not A)"
expr2 = "(A or B) and (not (A and B))"  # XOR Logic

print("Truth Table for Expression 1:")
truth_table(expr1)

print("\nTruth Table for Expression 2:")
truth_table(expr2)