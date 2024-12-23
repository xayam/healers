import math

from h.model.barriers.sound.cpu import CPU


class Generator:

    def __init__(self, function):
        self.function = function
        self.cpu = CPU(function=self.function)

    def start(self):
        self.cpu.run()


def main():

    def melody():
        t = 0.0
        while True:
            x = math.sin(9 * t + math.pi / 2)
            y = math.sin(8 * t)
            t += math.pi / 500
            if x == 0.0 or y == 0.0:
                continue
            yield x, y

    g = Generator(function=melody)
    g.start()

if __name__ == "__main__":
    main()
