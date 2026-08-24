# Experiment: Prime Number Check
# Question: Write a LISP/Python program that determines whether
# an integer is prime.

n = int(input("Enter a number: "))

if n < 2:
    print("Not Prime")
else:
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            print("Not Prime")
            break
    else:
        print("Prime")