from h.model.barriers.v2.cube3 import Cube3


class Thor8:

    scheme0 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))
    scheme1 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))
    scheme2 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))
    scheme3 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))
    scheme4 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))
    scheme5 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))
    scheme6 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))
    scheme7 = ((0, 4, 8), (2, 3, 7), (1, 5, 6))

    def __init__(self):
        self.schemes = [
            self.scheme0, self.scheme1, self.scheme2, self.scheme3,
            self.scheme4, self.scheme5, self.scheme6, self.scheme7
        ]
        self.state = [Cube3(scheme=scheme) for scheme in self.schemes]


def main():
    pass


if __name__ == "__main__":
    main()
