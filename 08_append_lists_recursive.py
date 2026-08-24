# Experiment: Append Two Lists using Recursion
# Question: Write a Recursive LISP function that appends two lists together.

def append_lists(a, b):
    if not a:
        return b
    return [a[0]] + append_lists(a[1:], b)

list1 = list(map(int, input("Enter first list: ").split()))
list2 = list(map(int, input("Enter second list: ").split()))

print("Appended list =", append_lists(list1, list2))