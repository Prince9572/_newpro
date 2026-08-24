# Experiment: Decision Tree using Scikit-learn
# Question: Build and visualize decision trees using Python/sklearn.

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train Decision Tree
clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf.fit(X, y)

# Visualize Decision Tree
plt.figure(figsize=(10, 6))
plot_tree(
    clf,
    filled=True,
    feature_names=iris.feature_names,
    class_names=iris.target_names
)
plt.show()