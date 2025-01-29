import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt


class Hyper:
    def __init__(self, limit, plot=True):
        self.output = None
        self.data = None
        self.limit = limit
        self.plot = plot



    @staticmethod
    def primfacs(p):
        i = 2
        primfac = []
        while i * i <= p:
            while p % i == 0:
                primfac.append(i)
                p = p / i
            i = i + 1
        if p > 1:
            primfac.append(round(p))
        return primfac

    def run(self):
        data = [[[0, 0, 0], [1, 1, 1]]]
        n = 2
        t = 0
        while True:
            factor = self.primfacs(n)
            # factor = [1] * (9 - len(factor)) + factor
            i = 0
            for f in range(0, len(factor), 3):
                tail = factor[f: f + 3]
                head = [1] * (3 - len(tail))
                chunk = head + tail
                # chunk = factor[f: f + 3]
                try:
                    data[i].append(chunk)
                except IndexError:
                    data.append([])
                    data[i].append(chunk)
                message = ""
                for k in data:
                    message += f"{len(k)}-"
                message = message[:-1] + f", n={n}, i={i}, chunk={chunk}"
                print(message)
                i += 1
            try:
                if len(data[t + 2]) >= self.limit:
                    break
            except IndexError:
                pass
            n += 1
        for d in data:
            print(f"len(d)={len(d)}")
        data1 = [
            data[t][: self.limit],
            data[t + 1][: self.limit],
            data[t + 2][: self.limit]
        ]
        # for d in data1:
        #     print(d)
        # sys.exit()
        data = [
            [
                # data1[0][j][0] + data1[1][j][0] + data1[2][j][0],
                # data1[0][j][1] + data1[1][j][1] + data1[2][j][1],
                # data1[0][j][2] + data1[1][j][2] + data1[2][j][2]
                data1[0][j][0] * data1[0][j][1] * data1[0][j][2],
                data1[1][j][0] * data1[1][j][1] * data1[1][j][2],
                data1[2][j][0] * data1[2][j][1] * data1[2][j][2]
            ]
            for j in range(self.limit)
        ]
        coeffs = [
            [1, 1, 1],
            # [-1, -1, -1],
            # [1, 1, -1],
            # [1, -1, 1],
            # [-1, 1, 1],
            # [-1, -1, 1],
            # [-1, 1, -1],
            # [1, -1, -1],
        ]
        appendix = [[], [], [], [], [], [], [], []]
        for c in range(len(coeffs)):
            for i in range(
                    c * self.limit // len(coeffs),
                    (c + 1) * self.limit // len(coeffs)
            ):
                appendix[c].append(
                    [
                        data[i][0] * coeffs[c][0],
                        data[i][1] * coeffs[c][1],
                        data[i][2] * coeffs[c][2]
                    ]
                )
        self.data = []
        for a in appendix:
            self.data += a
        # with open(f"data{t}.json", mode="w", encoding="utf-8") as js:
        #     js.write(json.dumps(self.data))
        data = self.data
        # for d in data:
        #     print(d)
        if self.plot:
            data = np.asarray(data)
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(projection='3d')
            ax.plot(data[:, 0], data[:, 1], data[:, 2])
            plt.show()


def main():
    h = Hyper(limit=16)
    h.run()


if __name__ == "__main__":
    main()
