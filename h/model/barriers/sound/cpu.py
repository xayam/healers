import random

import chess
# import matplotlib.pyplot as plt
import numpy as np

from h.model.barriers.sound.player import Player

np.random.seed(0)


class CPU:

    def __init__(self, function):
        self.function = function
        self.count = 50000
        self.maximum = self.count
        self.grid = [
            [i, j]
            for i in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
            for j in [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        ]
        self.epd_eval = "../chess/dataset.epdeval"
        self.random = random.SystemRandom(0)
        self.fens = self.get_fen_epd(count_limit=self.count)
        self.board = chess.Board()
        self.player = Player()

    def run(self):
        calc = self.calc()
        while self.count > 0:
            print(f"{self.count}/{self.maximum}")
            amplitudes = next(calc)
            self.player.play(amplitudes=amplitudes)
            self.count -= 1
        self.player.save()

    def calc(self):
        generator = self.function()
        for x, y in generator:
            amplitudes = self.get(x, y)
            yield amplitudes

    def get_fen_epd(self, count_limit=1):
        with open(self.epd_eval, mode="r") as f:
            dataevals = f.readlines()
        fens = []
        for _ in range(count_limit):
            dataeval = str(self.random.choice(dataevals)).strip()
            spl = dataeval.split(" ")
            fen = " ".join(spl[:-1])
            fens.append(fen)
        return fens

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
        self.board.set_fen(fen=self.fens[self.count - 1])
        for a in range(len(x)):
            sign = 1. if x[a] >= 0. else -1.
            piece = self.board.piece_at(a)
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
        # print(fen)
        return result
