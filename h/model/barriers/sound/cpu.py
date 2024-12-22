import matplotlib.pyplot as plt
import numpy as np

from h.model.barriers.sound.player import Player

np.random.seed(0)


class CPU:

    def __init__(self, function, grid=8):
        self.function = function
        self.grid = grid
        self.player = Player()

    def run(self):
        while True:
            amplitudes = self.calc()
            self.player.play(amplitudes=amplitudes)

    def calc(self):
        for x, y in self.function():
            amplitudes = self.get(x, y)
            yield amplitudes

    def get(self, x=8.0, y=1.0):
        grid = [
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
                (c[1] - y1 + x1 * (y2 - y1) / (x2 - x1) - c[0] * (x2 - x1) / (
                            y2 - y1)) /
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
        result = []
        for a in range(len(x)):
            sign = 1. if x[a] >= 0. else -1.
            result.append(
                # [
                    2 * sign * (x[a] ** 2 + y[a] ** 2)
                #     ,
                #     grid[a][0], grid[a][1]
                # ]
            )
        return result
