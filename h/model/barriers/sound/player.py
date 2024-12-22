import wave


class Player:

    def __init__(self):
        self.wav = wave.open("test.wav", mode="w")
        self.wav.setnchannels(1)
        self.wav.setsampwidth(4)
        self.wav.setframerate(16000)

    def play(self, amplitudes):
        data = bytes(amplitudes)
        self.wav.writeframes(data)

    def save(self):
        self.wav.close()


def main():
    p = Player()
    p.play(amplitudes=[-3.5, 5.0, 1.0, -2.0])


if __name__ == "__main__":
    main()
