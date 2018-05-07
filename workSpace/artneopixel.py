from machine import Pin
from neopixel import NeoPixel
import time
import os


class ArtNeoPixel(NeoPixel):

  def __init__(self, pin, n, bpp=4):
      super().__init__(pin, n, bpp)
      print("{} lights on {}".format(self.n,self.pin))


  def random(self):
   
    # random
    print("running random colors on {} lights".format(self.n))
    display_time = 5000 #sec
    sleep_time = 100 #msec
    brightness = 0.1 #0..1
    for i in range(display_time//sleep_time):
      print("i={}".format(i))
      for j in range(self.n):
        self[j] = tuple([int(i*brightness) for i in os.urandom(3)]) 
      self.write()
      time.sleep_ms(sleep_time)
    self.fill((0,0,0))
    self.write()


if __name__ == "__main__":
  np=ArtNeoPixel(Pin(15,Pin.OUT),30)
  print("Random...")
  np.random()
  
