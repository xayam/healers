import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, decomposition

np.random.seed(0)

X = [
    [x, y]
    for x in range(1, 9)
    for y in range(1, 9)
    if x != 0 and y != 0
]
print(X)

x1 = 0
y1 = 0
x2 = 8
y2 = 3
X = [
    [
        (c[1] - y1 + x1 * (y2 - y1) / (x2 - x1) - c[0] * (x2 - x1) / (y2 - y1)) / \
        ((y2 - y1) / (x2 - x1) - (x2 - x1) / (y2 - y1)),
        0
    ]
    for c in X
]
X = [
    [
        c[0],
        y1 + (y2 - y1) / (x2 - x1) * (c[0] - x1)
    ]
    for c in X
]
x = [c[0] for c in X]
y = [c[1] for c in X]
mean_x = sum(x) / len(x)
mean_y = sum(y) / len(y)
x = [2 * (mean_x - c) / (max(x) - min(x)) for c in x]
y = [2 * (mean_y - c) / (max(y) - min(y)) for c in y]
d = []
for a in range(len(x)):
    sign = 1. if x[a] >= 0. else -1.
    d.append(sign * (x[a] ** 2 + y[a] ** 2))
print(d)
plt.scatter(x, y)
plt.show()