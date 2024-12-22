import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)

C = [
    [x, y]
    for x in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
    for y in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
]
print(C)

x1 = 0.0
y1 = 0.0
x2 = 8.0
y2 = 1
X = [
    [
        (c[1] - y1 + x1 * (y2 - y1) / (x2 - x1) - c[0] * (x2 - x1) / (y2 - y1)) /
        ((y2 - y1) / (x2 - x1) - (x2 - x1) / (y2 - y1)),
        0
    ]
    for c in C
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
x = [(mean_x - c) / (max(x) - min(x)) for c in x]
y = [(mean_y - c) / (max(y) - min(y)) for c in y]
d = []
for a in range(len(x)):
    sign = 1. if x[a] >= 0. else -1.
    d.append([2 * sign * (x[a] ** 2 + y[a] ** 2), C[a][0], C[a][1]])
result = sorted(d, key=lambda k: k[0])
print(result)
plt.scatter(x, y)
plt.show()
