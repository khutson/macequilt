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

    async def arandom(self, duration=5000, pause_ms=100, brightness=0.1, lights=None):
        n,lights = self.get_sublights(lights)
        start_ms = ticks_ms()
        while ticks_diff(ticks_ms(), start_ms) < duration:
            for j in lights:
                col = tuple([int(c * brightness) for c in os.urandom(3)])
                self[j] = col
            await asyncio.sleep_ms(pause_ms)

async def test():
    print('initing np')
    np = ArtNeoPixel(15, 1)
    print('await arandom')
    await np.arandom()
    print("Finished.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())  


