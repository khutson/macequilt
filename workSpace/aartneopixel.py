from machine import Pin
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff
import os
import uasyncio as asyncio


class ArtNeoPixel(NeoPixel):

    def __init__(self, pin, n, bpp=3):
        if type(pin) is int:
            pin = Pin(pin, Pin.OUT)
        super().__init__(pin, n, bpp)
        self.refresh_rate = 15
        print("{} lights on {}".format(self.n, self.pin))
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())

    async def run(self):
        while True:
            if self.refresh_rate <= 0:
                await asyncio.sleep_ms(200)
            else:
                self.write()
                await asyncio.sleep_ms(self.refresh_rate)
    
    def get_sublights(self,lights):
        if lights is None:
            lights = [ j for j in range(self.n)]
        return len(lights), lights


    def random(self, display_time=5000, pause_ms=100, brightness=0.1, lights=None):
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
            time.sleep_ms(pause_ms)
        self.fill((0, 0, 0))
        self.write()
    
    async def arandom(self, duration=5000, pause_ms=100, brightness=0.1, lights=None):
        if lights is None:
            lights = [ j for j in range(self.n)]
        start_ms = ticks_ms()
        while ticks_diff(ticks_ms(), start_ms) < duration:
            for j in lights:
                col = tuple([int(c * brightness) for c in os.urandom(3)])
                self[j] = col
            await asyncio.sleep_ms(pause_ms)

    def chase(self, color=(255,255,255), pause_ms=25, num_cycles=4, lights=None):
        if lights is None:
            lights = [ j for j in range(self.n)]
        n = len(lights)
        for i in range(num_cycles * n): 
            for j in lights:
                self[j]=(0, 0, 0)
            self[lights[i % n]] = color
            self.write()
            time.sleep_ms(pause_ms)
          
    async def achase(self, duration=None, color=(255,255,255), pause_ms=25, num_cycles=4, lights=None):
        n, lights = self.get_sublights(lights)
        start_ms = ticks_ms()
        if duration is None:
            duration = num_cycles * pause_ms
        else:
            num_cycles = duration // pause_ms + 1
        for i in range(num_cycles * n): 
            if ticks_diff(ticks_ms(), start_ms) > duration:
                break
            self[lights[(i-1) % n]] = (0,0,0)
            self[lights[i % n]] = color
            await asyncio.sleep_ms(pause_ms)


    def bounce(self, color=(63,0,0), pause_ms=25, num_cycles=4, lights=None):
        n, lights = self.get_sublights(lights)
        for i in range(4 * n):
            self.fill(color)
            if (i // n) % 2 == 0:
                self[i % n] = (0, 0, 0)
            else:
                self[n - 1 - (i % n)] = (0, 0, 0)
            self.write()
            time.sleep_ms(pause_ms)
  
    async def abounce(self, color=(63,0,0), pause_ms=25, num_cycles=4, lights=None):
        n, lights = self.get_sublights(lights)
        for i in range(4 * n):
            self.fill(color)
            if (i // n) % 2 == 0:
                self[i % n] = (0, 0, 0)
            else:
                self[n - 1 - (i % n)] = (0, 0, 0)
            await asyncio.sleep_ms(pause_ms)
  

    def fade(self, cycles=1, color=(255,255,255), pause_ms=10, lights=None):
        n, lights = self.get_sublights(lights)
        for c in range(cycles):
            for i in range(0, 2 * 256, 8):
                for j in range(n):
                    if (i // 256) % 2 == 0:
                        val = i & 0xff
                    else:
                        val = 255 - (i & 0xff)
                    self[lights[j]] = [val & v for v in color] 
                self.write()
                time.sleep_ms(pause_ms)

    def clear(self):
        self.fill((0,0,0))
        self.write()
        
async def test():
    np = ArtNeoPixel(15, 1)
    # print("fade 10-14...")
    # await np.afade(cycles=4, color=(255,0,0), lights=[i for i in range(10,15)])
    
    print("Random for first half...")
    await np.arandom(lights=[i for i in range(np.n//2)])
    # print("Fade...")
    # await np.afade()
    print("Bounce...")
    await np.abounce()
    print("Chase...")
    await np.achase(color=(80,5,5),pause_ms=50)
    print("Random...")
    await np.arandom()
    print("Clearing..")
    np.clear()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())  






