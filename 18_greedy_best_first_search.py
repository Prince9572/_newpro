# Experiment: Greedy Best-First Search (Greedy BFS)
# Question: Apply Greedy BFS on a map with heuristics using Python.

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

heuristic = {
    'A': 6,
    'B': 4,
    'C': 2,
    'D': 5,
    'E': 1,
    'F': 0
}

def greedy(start, goal):
    open = [start]
    visited = []

    while open:
        open.sort(key=lambda x: heuristic[x])
        node = open.pop(0)

        if node not in visited:
            visited.append(node)
            print(node, end=" ")

            if node == goal:
                return

            open.extend(graph[node])

greedy('A', 'F')