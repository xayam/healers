import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)


class Square1Line:

    def __init__(self):
        self.grid_8x8 = None
        self.grid_512x512 = None
        self.init()

    def init(self):
        self.grid_8x8 = [
            [i, j]
            for i in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
            for j in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        ]
        self.grid_512x512 = []
        x = -255.5
        y = -255.5
        for i in range(512):
            for j in range(512):
                self.grid_512x512.append([x, y])
                y += 1
            x += 1

    def get_distances(self, x, y, grid=None):
        grid = self.grid_8x8 if grid is None else grid
        x1 = 0.0
        y1 = 0.0
        x2 = x
        y2 = y
        X = [
            [
                (c[1] - y1 + x1 * (y2 - y1) /
                 (x2 - x1) - c[0] * (x2 - x1) / (y2 - y1)) /
                ((y2 - y1) / (x2 - x1) - (x2 - x1) / (y2 - y1)),
                0
            ]
            for c in grid
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
            d.append([sign * (x[a] ** 2 + y[a] ** 2),
                      grid[a][0], grid[a][1]])
        result = sorted(d, key=lambda k: k[0])
        # print(result)
        # plt.scatter(x, y)
        # plt.show()
        return result
