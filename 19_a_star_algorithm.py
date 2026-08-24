# Experiment: A* Algorithm
# Question: Implement A* algorithm using heuristics
# for shortest pathfinding. Preferably in Python.

import heapq

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 3)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}

h = {'A':6, 'B':4, 'C':2, 'D':5, 'E':1, 'F':0}

def astar(start, goal):
    pq = [(h[start], 0, start)]
    visited = set()

    while pq:
        f, g, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return g

        for nxt, cost in graph[node]:
            if nxt not in visited:
                heapq.heappush(pq, (g + cost + h[nxt], g + cost, nxt))

print("Shortest Cost:", astar('A', 'F'))