# Experiment: Uniform Cost Search
# Question: Implement Uniform Cost Search for pathfinding
# in weighted graphs using Python.

import heapq

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 3)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}

def ucs(start, goal):
    pq = [(0, start)]
    visited = set()

    while pq:
        cost, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return cost

        for nxt, w in graph[node]:
            if nxt not in visited:
                heapq.heappush(pq, (cost + w, nxt))

print("Minimum Cost:", ucs('A', 'F'))