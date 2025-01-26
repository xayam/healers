import os

import numpy as np
import matplotlib.pyplot as plt

SIZE = 128

PARAMS = [
    # [
    #     16,  # size
    #     "1/71",  # scale
    #     "0.0001",  # radius
    #     "1420"  # freq MHz
    # ],
    # [
    #     16,  # size
    #     "1/27",  # scale
    #     "0.0001",  # radius
    #     "432"  # freq MHz
    # ],
    [
        64,  # size
        "1/128",  # scale
        "0.0001",  # radius
        "128"  # freq MHz
    ],

]


class AXData:
    def __init__(self, size, plot=True):
        self.output = None
        self.template = None
        self.data = None
        self.size = size
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
        data = [[[0, 0, 0], [1, 1, 1]]]
        n = 2
        while True:
            factor = self.primfacs(n)
            i = 0
            for f in range(0, len(factor), 3):
                tail = factor[f: f + 3]
                head = [1] * (3 - len(tail))
                chunk = head + tail
                try:
                    data[i].append(chunk)
                except IndexError:
                    data.append([])
                    data[i].append(chunk)
                print(f"n={n}, i={i}, chunk={chunk}")
                i += 1
            try:
                if len(data[2]) == 16:
                    break
            except IndexError:
                pass
            n += 1
        for d in data:
            print(f"len(d)={len(d)}")
        data1 = [data[0][:16], data[1][:16], data[2][:16]]
        self.data = [
            [
                data1[0][j][0] * data1[0][j][1] * data1[0][j][2],
                data1[1][j][0] * data1[1][j][1] * data1[1][j][2],
                data1[2][j][0] * data1[2][j][1] * data1[2][j][2]
            ]
            for j in range(16)
        ]
        data = self.data
        if self.plot:
            data = np.asarray(data)
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(projection='3d')
            ax.plot(data[:, 0], data[:, 1], data[:, 2])
            plt.show()

    def nec(self):
        folder = "axdata2"
        scale = "1.0"
        radius = "0.001"
        freq_mhz = "1420"
        filename = f"{folder}/ax{self.size}_{freq_mhz}Mhz.nec"
        if not os.path.exists(folder):
            os.mkdir(folder)
        self.output = str(self.template).replace(
            "{{SCALE}}", scale, 1
        )
        self.output = str(self.output).replace(
            "{{RADIUS}}", radius, 1
        )
        self.output = str(self.output).replace(
            "{{FREQMHZ}}", freq_mhz, 1
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
        with open(filename, mode="w", encoding="utf-8") as output:
            output.write(self.output)


def main():
    ax = AXData(size=SIZE)
    ax.run()
    ax.nec()


if __name__ == "__main__":
    main()
