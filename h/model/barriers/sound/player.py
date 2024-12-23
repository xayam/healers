import wave
import pygame

pygame.mixer.init()

class Player:

    def __init__(self):
        self.filename = "test.wav"
        self.wav = wave.open(self.filename, mode="w")
        self.wav.setnchannels(1)
        self.wav.setsampwidth(4)
        self.wav.setframerate(8000)

    def play(self, amplitudes):
        # print(amplitudes)
        data = bytes(amplitudes)
        self.wav.writeframes(data)

    def save(self):
        self.wav.close()
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass


def main():
    p = Player()
    p.play(amplitudes=[0, 5, 1, 2])


if __name__ == "__main__":
    main()
