# Experiment: BFS and DFS on a Graph
# Question: Implement BFS and DFS on a graph using Python
# and compare the traversal order.

from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

def bfs(start):
    q = deque([start])
    vis = {start}
    while q:
        v = q.popleft()
        print(v, end=" ")
        for i in graph[v]:
            if i not in vis:
                vis.add(i)
                q.append(i)

def dfs(v, vis=set()):
    vis.add(v)
    print(v, end=" ")
    for i in graph[v]:
        if i not in vis:
            dfs(i, vis)

print("BFS:", end=" ")
bfs('A')

print("\nDFS:", end=" ")
dfs('A')