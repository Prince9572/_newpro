# Experiment: Remove First Occurrence using Recursion
# Question: Write a Recursive LISP function that takes two arguments:
# first, an atom; second, a list. It returns a list after removing
# the first occurrence of that atom within the list.

def remove_first(x, lst):
    if not lst:
        return []
    if lst[0] == x:
        return lst[1:]
    return [lst[0]] + remove_first(x, lst[1:])

lst = list(map(int, input("Enter list elements: ").split()))
x = int(input("Enter element to remove: "))

print("Updated list =", remove_first(x, lst))
