# Experiment: Evaluate Infix Arithmetic Expression
# Question: Write a function that evaluates a fully parenthesized
# infix arithmetic expression. For example, (1+(2*3)) should return 7.

exp = input("Enter expression: ")
print("Result =", eval(exp))