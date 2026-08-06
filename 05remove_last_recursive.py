# Experiment: Remove Last Element using Recursion
# Question: Write a Recursive LISP function that takes one argument as a list
# and returns a list except the last element of the list.
# (Do not use butlast.)

def remove_last(lst):
    if len(lst) == 1:
        return []
    return [lst[0]] + remove_last(lst[1:])

lst = list(map(int, input("Enter list elements: ").split()))
print("List except last element =", remove_last(lst))