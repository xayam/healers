import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)


def get_distances(x, y):
    C = [
        [i, j]
        for i in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        for j in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
    ]

    x1 = 0.0
    y1 = 0.0
    x2 = x
    y2 = y
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
        d.append([512 + round((2 * sign * (x[a] ** 2 + y[a] ** 2) + 1) / 2 * 512),
                  round(64 * (C[a][0] + 3.5)), round(64 * (C[a][1] + 3.5))])
    result = sorted(d, key=lambda k: k[0])
    # print(result)
    # plt.scatter(x, y)
    # plt.show()
    return result
