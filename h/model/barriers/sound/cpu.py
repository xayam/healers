import sys

import chess
import matplotlib.pyplot as plt
import numpy as np

from h.model.barriers.sound.player import Player

np.random.seed(0)


class CPU:

    def __init__(self, function, grid=8):
        self.function = function
        self.grid = [
            [i, j]
            for i in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
            for j in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        ]
        self.player = Player()

    def run(self):
        count = 1
        calc = self.calc()
        while count <= 5000:
            print(f"{count}/5000")
            amplitudes = next(calc)
            self.player.play(amplitudes=amplitudes)
            count += 1
        self.player.save()

    def calc(self):
        generator = self.function()
        for x, y in generator:
            amplitudes = self.get(x, y)
            yield amplitudes

    def get(self, x=8.0, y=1.0):
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
            for c in self.grid
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
        board = chess.Board()
        for a in range(len(x)):
            sign = 1. if x[a] >= 0. else -1.
            piece = board.piece_at(a)
            if piece is None:
                result.append(0)
            else:
                result.append(
                    # [
                    128 + int(
                        128 * sign * (x[a] ** 2 + y[a] ** 2) /
                        piece.piece_type / 6
                    )
                    #     ,
                    #     self.grid[a][0], self.grid[a][1]
                    # ]
                )
        # sys.exit()
        return result
