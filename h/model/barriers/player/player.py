import math
import pprint
import random

from h.model.barriers.player import beep


class Player:

    def __init__(self, piano, hand):
        self.piano = piano
        self.hand = hand
        self.coord2freq = {}
        self.freq2coord = {}
        self.beep = None
        self.init()

    def init(self):
        self.set_state()
        pprint.pprint(self.coord2freq)
        self.beep = beep.Beep(self)

    def run(self):
        self.beep.play()

    def check(self, h, x, y, z):
        result = abs(x) == abs(h) or abs(y) == abs(h) or abs(z) == abs(h)
        return result

    def get(self, h, x, y, z):
        while True:
            dx, dy, dz = self.random(), self.random(), self.random()
            if not self.check(h, x + dx, y + dy, z + dz):
                continue
            if not self.coord2freq.__contains__(x + dx):
                continue
            if not self.coord2freq[x + dx].__contains__(y + dy):
                continue
            if not self.coord2freq[x + dx][y + dy].__contains__(z + dz):
                continue
            break
        return dx, dy, dz

    @staticmethod
    def random():
        return random.choice([-1, 0, 1])

    @staticmethod
    def duration(x, y, z):
        a = 5
        duration = a * abs(math.sin(x))
        duration += a * abs(math.sin(y))
        duration += a * abs(math.sin(z))
        return duration

    def set_state(self):
        freq = 0
        self.coord2freq = {}
        for x in range(-self.piano, self.piano + 1):
            if x == 0: continue
            self.coord2freq[x] = {}
            for y in range(-self.piano, self.piano + 1):
                if y == 0: continue
                self.coord2freq[x][y] = {}
                for z in range(-self.piano, self.piano + 1):
                    if z == 0: continue
                    self.coord2freq[x][y][z] = freq
                    self.freq2coord[freq] = {"x": x, "y": y, "z": z}
                    freq += 1


if __name__ == "__main__":
    # print(datetime.now())
    # winsound.Beep(1000, 1000)
    # print(datetime.now())
    p = Player(piano=12, hand=12)
    p.run()
