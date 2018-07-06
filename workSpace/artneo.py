from machine import Pin
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff
import os
import logging
from artpart import ArtPart
import uasyncio as asyncio

logging.basicConfig(level=logging.WARNING)


class ArtNeoPixel(ArtPart):

    def __init__(self, pin, n, bpp=3, name=None, duration=10000):

        super().__init__(name=name, duration=duration)

        if type(pin) is not Pin:
            pin = Pin(pin, Pin.OUT)
        self.np = NeoPixel(pin, n, bpp)
        self.refresh_rate = 15
        self.need_update = True
        self.running = True
        self.duration = duration  # ms
        # logging.info("{} lights on {}".format(self.n, self.pin))
        self.cmds = {'random': self.random,
                    'fade': self.fade,
                    'bounce': self.bounce,
                    'chase': self.chase}
        loop = asyncio.get_event_loop()
        loop.create_task(self.update())

    def __getitem__(self, key):
        return self.np[key]

    def __setitem__(self, key, value):
        self.np[key] = value

    async def update(self):
        """actually writes out pixel info every self.refresh_rate msecs
        runs asynchronously and should only be one running"""
        self.seq_start = ticks_ms()
        while self.running:
            self.seq_ms = ticks_diff(ticks_ms(), self.seq_start)
            if self.seq_ms > self.duration:
                self.seq_start = ticks_ms()
                self.seq_ms = 0
            if self.refresh_rate <= 0:
                await asyncio.sleep_ms(200)
            else:
                logging.debug("duration={}, seq_ms={},seq_start={}".format(
                        self.duration, self.seq_ms, self.seq_start))
                logging.debug("self[0]={}".format(self[0]))
                if self.need_update:
                    self.np.write()
                    self.need_update = False
                await asyncio.sleep_ms(self.refresh_rate)

    def get_sublights(self, lights):
        if lights is None:
            lights = [j for j in range(self.np.n)]
        return len(lights), lights
    
    async def random(self, brightness=0.1,
                     duration=5000, pause_ms=100,
                     start_ms=0, lights=None, **kwargs):
        await self.wait_for_start(start_ms)
        n, lights = self.get_sublights(lights)
        start_ms = ticks_ms()
        while self.running:
            while ticks_diff(ticks_ms(), start_ms) < duration:
                for j in lights:
                    col = [int(c * brightness) for c in os.urandom(3)]
                    self.np[j] = col
                self.need_update = True
                await asyncio.sleep_ms(pause_ms)
          
    async def chase(self,
                    color=(255, 255, 255), bgcolor=(0, 0, 0),
                    cycles=4,
                    duration=None, pause_ms=25,
                    start_ms=0, lights=None, **kwargs):
        n, lights = self.get_sublights(lights)
        while self.running:
            await self.wait_for_start(start_ms)
            begin_ms = ticks_ms()
            if duration is None:
                duration = cycles * pause_ms * n
            else:
                cycles = duration // pause_ms * (n + 1)
            for i in range(cycles * n):
                if ticks_diff(ticks_ms(), begin_ms) > duration:
                    break
                self.np[lights[(i-1) % n]] = bgcolor
                self.np[lights[i % n]] = color
                self.need_update = True
                await asyncio.sleep_ms(pause_ms)
  
    async def bounce(self,
                     color=(255, 255, 255), bgcolor=(0, 0, 0),
                     cycles=4,
                     duration=None, pause_ms=25,
                     start_ms=0, lights=None, **kwargs):
        await self.wait_for_start(start_ms)
        if duration is None:
            duration = cycles * pause_ms * n
        else:
            cycles = duration // pause_ms * (n + 1)
        n, lights = self.get_sublights(lights)

        while self.running:
            for i in range(cycles * 2 * n):
                for j in lights:
                    self.np[j] = bgcolor
                if (i // n) % 2 == 0:
                    self.np[lights[i % n]] = color
                else:
                    self.np[lights[n - 1 - (i % n)]] = color
                self.need_update = True
                await asyncio.sleep_ms(pause_ms)

    async def fade(self,
                   color=(255, 255, 255),
                   cycles=1, step=8,
                   duration=None, pause_ms=50, lights=None, **kwargs):
        n, lights = self.get_sublights(lights)
        while self.running:
            for c in range(cycles):
                for val in range(0, 256, step):
                    logging.info("val={}".format(val))
                    for j in range(n):
                        self.np[lights[j]] = [val & v for v in color]
                    self.need_update = True
                    await asyncio.sleep_ms(pause_ms)
                for val in range(255, -1, -step):
                    logging.info("val={}".format(val))
                    for j in range(n):
                        self.np[lights[j]] = [val & v for v in color]
                    self.need_update=True
                    await asyncio.sleep_ms(pause_ms)
                for j in range(n):
                    self.np[lights[j]] = (0, 0, 0)
                self.need_update = True


    def clear(self,lights=None):
        if lights is None:
            self.np.fill((0,0,0))
        else:
            for i in range(len(lights)):
                self.np[lights[i]] = (0,0,0)
        self.np.write()
        
async def test():
    np = ArtNeoPixel(15, 30)
    logging.info("fade 10-14...")
    await np.fade(cycles=4, pause_ms=10, color=(255, 0, 0), lights=[i for i in range(10, 15)])
    
    logging.info("Random for first half...")
    await np.random(lights=[i for i in range(np.n // 2)])
    logging.info("Fade...")
    await np.fade()
    logging.info("Bounce...")
    await np.bounce()
    logging.info("Chase...")
    await np.chase(color=(80, 5, 5), pause_ms=50)
    logging.info("Random...")
    await np.random()
    logging.info("Clearing..")
    np.clear()
    
async def simul_test():
    logging.info("and now...simultaneously...")
    np = ArtNeoPixel(15, 30, duration=20000)
    np.effect({'effect': 'random', 'lights': [26, 27, 28, 29], 'brightness': 0.5})
    loop = asyncio.get_event_loop()
    logging.info("fade 0-7...")
    loop.create_task(np.fade(cycles=4, pause_ms=10, color=(255, 0, 0), lights=[i for i in range(8)]))
    # logging.info("Random 8-14...")
    # loop.create_task( np.arandom(lights=[i for i in range(8,15)]))
    # logging.info("Bounce 15-22...")
    # loop.create_task( np.abounce(cycles=6,lights=[i for i in range(15,23)]))
    # logging.info("Chase 23-29")
    # loop.create_task( np.achase(color=(0,255,0),pause_ms=50,lights=[ i for i in range(23,30)]))
    await asyncio.sleep(10)
    logging.info("Clearing..")
    np.running = False
    await asyncio.sleep(0)
    np.clear()
    

def run_tests():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.run_until_complete(simul_test())  


if __name__ == "__main__":
    run_tests()
    







