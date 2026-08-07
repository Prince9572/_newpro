# Experiment: Introduction to PROLOG and Program Structure
# Question: Introduction to PROLOG and program structure.

print("PROLOG (Programming in Logic)")
print("-" * 40)

print("Introduction:")
print("• PROLOG stands for PROgramming in LOGic.")
print("• It is a declarative programming language.")
print("• It is based on Predicate Logic.")
print("• It is mainly used in Artificial Intelligence (AI).")

print("\nApplications:")
print("- Expert Systems")
print("- Natural Language Processing")
print("- Automated Reasoning")
print("- Knowledge Representation")

print("\nProgram Structure:")
print("1. Facts")
print("2. Rules")
print("3. Queries")

print("\nExample Facts:")
print("parent(john, mary).")
print("parent(mary, alice).")

print("\nExample Rule:")
print("grandparent(X, Y) :- parent(X, Z), parent(Z, Y).")

print("\nExample Query:")
print("?- grandparent(john, Y).")