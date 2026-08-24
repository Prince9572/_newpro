# Experiment: Depth-First Traversal of a Binary Tree
# Question: Write a function that performs a depth-first traversal
# of a binary tree. The function should return a list containing
# the tree nodes in the order they were visited.

class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None

def dfs(root):
    if not root:
        return []
    return [root.data] + dfs(root.left) + dfs(root.right)

# Sample Binary Tree
#       1
#      / \
#     2   3
#    / \
#   4   5

root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

print("DFS Traversal =", dfs(root))