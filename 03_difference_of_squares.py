# Experiment: Difference of Squares
# Question: Write a LISP function to compute the difference of squares.
# (If x > y return x² – y², otherwise y² – x².)

x = int(input("Enter first number: "))
y = int(input("Enter second number: "))

if x > y:
    print("Difference of squares =", x*x - y*y)
else:
    print("Difference of squares =", y*y - x*x)