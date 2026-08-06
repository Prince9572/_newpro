# Experiment: Reverse a List using Recursion
# Question: Write a Recursive LISP function that takes one argument as a list
# and returns the reverse of the list.
# (Do not use reverse predicate.)

def reverse_list(lst):
    if not lst:
        return []
    return reverse_list(lst[1:]) + [lst[0]]

lst = list(map(int, input("Enter list elements: ").split()))
print("Reversed list =", reverse_list(lst))