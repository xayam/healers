from h.model.barriers.v2.thor8 import Thor8


class Two:

    def __init__(self):
        self.thor1 = Thor8()
        self.thor2 = Thor8()

    def __str__(self):
        return str(self.thor1) + "\n\n" + str(self.thor2)


def main():
    t = Two()
    print(t)


if __name__ == "__main__":
    main()