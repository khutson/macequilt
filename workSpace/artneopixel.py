from machine import Pin
from neopixel import NeoPixel
import time
import os


class ArtNeoPixel(NeoPixel):

    def __init__(self, pin, n, bpp=3):
        if type(pin) is int:
            pin = Pin(pin, Pin.OUT)
        super().__init__(pin, n, bpp)
        print("{} lights on {}".format(self.n, self.pin))

    def random(self, display_time=5000, sleep_time=100, brightness=0.1, lights=None):
        """
Randomly flashes all pixels.
All times in milliseconds.
brightness 0..1
        :rtype: None
        """
        if lights is None:
            lights = [ j for j in range(self.n)]
        # print("running random colors on {} lights".format(self.n))
        for i in range(display_time // sleep_time):
            for j in lights:
                col = tuple([int(c * brightness) for c in os.urandom(3)])
                self[j] = col
            self.write()
            time.sleep_ms(sleep_time)
        self.fill((0, 0, 0))
        self.write()

    def cycle(self, color=(255,255,255), pause_time=25):
      for i in range(4 * self.n):
          self.fill((0, 0, 0))
          self[i % self.n] = color
          self.write()
          time.sleep_ms(pause_time)

    def bounce(self, pause_time=60):
        n = self.n
        for i in range(4 * n):
            self.fill((0, 0, 63))
            if (i // n) % 2 == 0:
                self[i % n] = (0, 0, 0)
            else:
                self[n - 1 - (i % n)] = (0, 0, 0)
            self.write()
            time.sleep_ms(pause_time)


    def fade(self, cycles=1, color=(255,255,255), pause_time=10, lights=None):
        if lights is None:
            lights = [ i for i in range(self.n)]
        n = len(lights)
        for c in range(cycles):
            for i in range(0, 2 * 256, 8):
                for j in range(n):
                    if (i // 256) % 2 == 0:
                        val = i & 0xff
                    else:
                        val = 255 - (i & 0xff)
                    self[lights[j]] = [val & v for v in color] 
                self.write()
                time.sleep_ms(pause_time)

    def clear(self):
        self.fill((0,0,0))
        self.write()
        
def run_test():
    np = ArtNeoPixel(Pin(15, Pin.OUT), 30)
    print("fade 10-14...")
    np.fade(cycles=4, color=(255,0,0), lights=[i for i in range(10,15)])
    
    print("Random for first half...")
    np.random(lights=[i for i in range(np.n//2)])
    print("Fade...")
    np.fade()
    print("Bounce...")
    np.bounce()
    print("Cycle...")
    np.cycle(color=(80,5,5),pause_time=5)
    print("Random...")
    np.random()
    print("Clearing..")
    np.clear()

if __name__ == "__main__":
    run_test()




