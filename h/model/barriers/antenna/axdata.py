import os.path
from os import mkdir

import numpy as np
import matplotlib.pyplot as plt


PARAMS = [
    [
        16, # size
        "1/71", # scale
        "0.0001", # radius
        "1420" # freq MHz
    ],
    [
        16, # size
        "1/27", # scale
        "0.0001", # radius
        "432" # freq MHz
    ],
    [
        64, # size
        "1/128", # scale
        "0.0001", # radius
        "128" # freq MHz
    ],

]


class AXData:
    def __init__(self, size, scale, radius, freq_mhz, plot=True):
        self.output = None
        self.template = None
        self.data = None
        self.size = size
        self.scale = scale
        self.radius = radius
        self.freq_mhz = freq_mhz
        self.folder = f"ax{self.size}"
        self.filename = f"{self.folder}/AX{self.size}_{self.freq_mhz}MHz.nec"
        self.plot = plot
        self.init()

    def init(self):
        with open("template.nec", mode="r", encoding="utf-8") as template:
            self.template = template.read()

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
        print(f"AX{self.size}")
        print("[0, 0, 0]")
        print("[1, 1, 1]")
        for n in range(2, self.size):
            factor = self.primfacs(n)
            x, y, z = 0, 0, 0
            for f in range(0, len(factor), 3):
                tail = factor[f: f + 3]
                head = [1] * (3 - len(tail))
                chunk = head + tail
                chunk[0], chunk[1], chunk[2] = \
                    chunk[0] - x, chunk[1] - y, chunk[2] - z
                data.append(chunk)
                print(f"[{chunk[0]}, {chunk[1]}, {chunk[2]}]")
                # print(f"n={n}, head={head}, tail={tail}")
                x, y, z = chunk[0], chunk[1], chunk[2]
        print(f"SIZE={self.size}, len(data)={len(data)}")
        self.data = data
        if self.plot:
            data = np.asarray(data)
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(projection='3d')
            ax.plot(data[:, 0], data[:, 1], data[:, 2])
            plt.show()

    def nec(self):
        if not os.path.exists(self.folder):
            mkdir(self.folder)
        self.output = str(self.template).replace(
            "{{SCALE}}", self.scale, 1
        )
        self.output = str(self.output).replace(
            "{{RADIUS}}", self.radius, 1
        )
        self.output = str(self.output).replace(
            "{{FREQMHZ}}", self.freq_mhz, 1
        )
        x, y, z = 0, 0, 0
        self.data.append([x, y, z])
        gws = ""
        segment = 2
        for i in range(1, len(self.data)):
            gws += \
                f"GW {i} {segment} {x}*S {y}*S {z}*S " \
                f"{self.data[i][0]}*S {self.data[i][1]}*S {self.data[i][2]}*S R\n"
            x, y, z = self.data[i][0], self.data[i][1], self.data[i][2]
        self.output = str(self.output).replace(
            "{{GW}}", gws[:-1], 1
        )
        with open(self.filename, mode="w", encoding="utf-8") as output:
            output.write(self.output)


def main():
    for size, scale, radius, freq_mhz in PARAMS:
        ax = AXData(
            size=size,
            scale=scale,
            radius=radius,
            freq_mhz=freq_mhz
        )
        ax.run()
        ax.nec()


if __name__ == "__main__":
    main()
