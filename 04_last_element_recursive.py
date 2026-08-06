# Experiment: Last Element of a List using Recursion
# Question: Write a Recursive LISP function that takes one argument as a list
# and returns the last element.

def last(lst):
    if len(lst) == 1:
        return lst[0]
    return last(lst[1:])

lst = list(map(int, input("Enter list elements: ").split()))
print("Last element =", last(lst))