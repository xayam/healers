import random
import threading

from concurrent.futures import ThreadPoolExecutor as pool

import winsound


class Beep:

    def __init__(self, player):
        self.player = player
        self.init()

    def init(self):
        pass

    def play(self):
        t = threading.Thread(
            target=self.thread,
            daemon=True,
        )
        t.start()
        t.join()

    def thread(self):
        with pool(max_workers=2 * self.player.hand) as executor:
            for h in range(1, self.player.hand + 1):
                executor.submit(self.beep, h)
            executor.shutdown()

    def beep(self, h):
        x, y, z = h // 2, h // 2, h
        while True:
            while True:
                dx, dy, dz = self.player.get(h, x, y, z)
                if not (dx == 0 and dy == 0 and dz == 0):
                    break
            x, y, z = x + dx, y + dy, z + dz
            freq = 54 + self.player.coord2freq[x][y][z]
            duration = 4 * (abs(x) + abs(y) + abs(z))
            winsound.Beep(freq, duration)
            if abs(h) == random.choice([222]):
                print(
                    "№" + str(h),
                    "x: " + str(x).rjust(2, " "),
                    "y: " + str(y).rjust(2, " "),
                    "z: " + str(z).rjust(2, " "),
                    "freq: " + str(freq).rjust(5, " "),
                    "duration: " + str(duration).rjust(3, " "),
                    sep=" | "
                )
