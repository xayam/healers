

class Cube3:

    def __init__(self, scheme):
        self.scheme = [
            [*scheme[1]],
            [*scheme[0]],
            [*scheme[2]]
        ]
        self.state = []
        self.init()

    def init(self):
        pass

    def __str__(self):
        return str(self.scheme)

    def rotate(self):
        self._rotate08()
        self._rotate17()
        self._rotate26()
        self._rotate53()
        self._rotate80()
        self._rotate71()
        self._rotate62()
        self._rotate35()

    def _rotate08(self):
        pass

    def _rotate17(self):
        pass

    def _rotate26(self):
        pass

    def _rotate53(self):
        pass

    def _rotate80(self):
        pass

    def _rotate71(self):
        pass

    def _rotate62(self):
        pass

    def _rotate35(self):
        pass


def main():
    c = Cube3(scheme=((0, 4, 8), (2, 3, 7), (1, 5, 6)))
    print(c)


if __name__ == "__main__":
    main()
