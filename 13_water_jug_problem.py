# Experiment: Water Jug Problem
# Question: Write a LISP/Python program for the Water Jug Problem.

a, b, target = map(int, input("Enter jug1 jug2 target: ").split())

x = y = 0

while x != target and y != target:
    print(x, y)

    if x == 0:
        x = a
    elif y == b:
        y = 0
    else:
        t = min(x, b - y)
        x -= t
        y += t

print(x, y)
print("Target reached!")