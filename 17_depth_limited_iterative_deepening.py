# Experiment: Depth-Limited Search (DLS) and Iterative Deepening Search (IDS)
# Question: Simulate Depth-Limited and Iterative Deepening Search in Python.

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

def dls(node, goal, limit):
    if node == goal:
        return True
    if limit <= 0:
        return False
    for i in graph[node]:
        if dls(i, goal, limit - 1):
            return True
    return False

def ids(start, goal, depth):
    for i in range(depth + 1):
        if dls(start, goal, i):
            return i
    return -1

goal = 'F'
depth = 3

print("Found at Depth:", ids('A', goal, depth))