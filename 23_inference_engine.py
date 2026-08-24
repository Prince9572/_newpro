# Experiment: Inference Engine using Forward Chaining
# Question: Create inference engines using chaining techniques.
# Preferably in Python.

facts = {"A", "B"}
rules = {
    ("A", "B"): "C",
    ("C",): "D",
    ("D",): "E"
}

changed = True
while changed:
    changed = False
    for cond, result in rules.items():
        if set(cond).issubset(facts) and result not in facts:
            facts.add(result)
            changed = True

print("Derived Facts:", facts)