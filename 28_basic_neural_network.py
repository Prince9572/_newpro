# Experiment: Basic Neural Network using NumPy
# Question: Build a basic neural network with one layer in NumPy.
# Preferably in Python.

import numpy as np

# Input data
X = np.array([
    [0, 0, 1],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])

# Output labels
y = np.array([[0], [1], [1], [0]])

# Initialize weights
np.random.seed(42)
weights = np.random.randn(3, 1)

# Sigmoid activation
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Sigmoid derivative
def sigmoid_derivative(x):
    return x * (1 - x)

# Train the neural network
for epoch in range(10000):
    output = sigmoid(np.dot(X, weights))
    error = y - output
    weights += np.dot(X.T, error * sigmoid_derivative(output)) * 0.1

# Display results
print("Trained Weights:\n", weights)
print("Predictions:\n", output)