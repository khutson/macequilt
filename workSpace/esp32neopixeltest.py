from neopixel import NeoPixel
import machine
import time

np = NeoPixel(machine.Pin(4),1)

for r in range(255):
  for g in range(255):
    for b in range(255):
      np[0]=((r,g,b))
      np.write()
      time.sleep_ms(10)
      

