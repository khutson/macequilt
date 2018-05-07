from machine import Pin
from neopixel import NeoPixel
import time
import os

np = None

def setup(pin_number=15,num_lights=30):
    
    pin=Pin(pin_number,Pin.OUT)
    np=NeoPixel(pin,num_lights)
    return np

def run(pin_number=15,num_lights=30):
    global np
    if np is None:
      np = setup(pin_number,num_lights)
    n = np.n
    
    # random
    display_time = 5000 #sec
    sleep_time = 100 #msec
    brightness = 0.1 #0..1
    for i in range(display_time//sleep_time):
        for j in range(n):
          np[j] = tuple([int(i*brightness) for i in os.urandom(3)]) 
        np.write()
        time.sleep_ms(sleep_time)
    np.fill((0,0,0))
    np.write()


if __name__ == "__main__":
   setup()
   run()

