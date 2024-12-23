import math

from h.model.barriers.sound.cpu import CPU


class Generator:

    def __init__(self):
        self.cpu = CPU(function=self.melody)

    def melody(self):
        t = -1.0
        while True:
            x = math.sin(9 * t + math.pi / 2)
            y = math.sin(8 * t)
            if t >= 1.0:
                t -= 2 / self.cpu.maximum
            else:
                t += 2 / self.cpu.maximum
            if x == 0.0 or y == 0.0 or x == y:
                continue
            yield x, y

    def start(self):
        self.cpu.run()


def main():
    g = Generator()
    g.start()


if __name__ == "__main__":
    main()
