

class Cube3:

    def __init__(self, scheme):
        self.scheme = scheme
        self.init()

    def init(self):
        pass

    def __str__(self):
        return str(self.scheme)

    def rotate08(self):
        pass

    def rotate17(self):
        pass

    def rotate26(self):
        pass

    def rotate53(self):
        pass

    def rotate80(self):
        pass

    def rotate71(self):
        pass

    def rotate62(self):
        pass

    def rotate35(self):
        pass


def main():
    c = Cube3(scheme=((0, 4, 8), (2, 3, 7), (1, 5, 6)))
    print(c)


if __name__ == "__main__":
    main()
