from machine import Pin
from neopixel import NeoPixel
import time
import os


class ArtNeoPixel(NeoPixel):

    def __init__(self, pin, n, bpp=4):
        super().__init__(pin, n, bpp)
        print("{} lights on {}".format(self.n, self.pin))

    def random(self, display_time=5000, sleep_time=100, brightness=0.1):
        """
Randomly flashes all pixels.
All times in milliseconds.
brightness 0..1
        :rtype: None
        """
        print("running random colors on {} lights".format(self.n))

        for i in range(display_time // sleep_time):
            print("i={}".format(i))
            for j in range(self.n):
                self[j] = tuple([int(i * brightness) for i in os.urandom(3)])
            self.write()
            time.sleep_ms(sleep_time)
        self.fill((0, 0, 0))
        self.write()


if __name__ == "__main__":
    np = ArtNeoPixel(Pin(15, Pin.OUT), 30)
    print("Random...")
    np.random()
