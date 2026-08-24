# Experiment: Alternate Elements from Two Lists using Recursion
# Question: Write a recursive LISP function that takes 2 lists as
# arguments and returns a list containing alternate elements from each list.

def alternate(l1, l2):
    if not l1:
        return l2
    if not l2:
        return l1
    return [l1[0], l2[0]] + alternate(l1[1:], l2[1:])

list1 = list(map(int, input("Enter first list: ").split()))
list2 = list(map(int, input("Enter second list: ").split()))

print("Result =", alternate(list1, list2))
