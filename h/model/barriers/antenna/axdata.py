import numpy as np
import matplotlib.pyplot as plt


SIZES = [16, 64]


class AXData:
    def __init__(self, size, plot=True):
        self.size = size
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
        data = [[0, 0, 0], [1, 1, 1]]
        for n in range(2, self.size):
            factor = self.primfacs(n)
            if len(factor) in [1, 2, 3]:
                tail = [1] * (3 - len(factor))
                data.append(tail + factor)
        print(f"AX{self.size}")
        for x, y, z in data:
            print(f"[{x}, {y}, {z}]")
        print(f"SIZE={self.size}, len(data)={len(data)}")
        if self.plot:
            data = np.asarray(data)
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(projection='3d')
            ax.plot(data[:, 0], data[:, 1], data[:, 2])
            plt.show()


def main():
    for size in SIZES:
        ax = AXData(size=size)
        ax.run()


if __name__ == "__main__":
    main()
