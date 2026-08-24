# Experiment: Factorial of a Number
# Question: Write a function that computes the factorial of a number.
# (Factorial of 0 is 1, and factorial of n is n*(n-1)*...*1.
# Factorial is defined only for integers greater than or equal to 0.)

def fact(n):
    if n == 0 or n == 1:
        return 1
    return n * fact(n - 1)

n = int(input("Enter a number: "))

if n < 0:
    print("Factorial not defined for negative numbers")
else:
    print("Factorial =", fact(n))