from machine import Pin
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff
import os
import logging
from artpart import ArtPart
import uasyncio as asyncio

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ArtNeoPixel")


class ArtNeoPixel(ArtPart):

    def __init__(self, pin=15, n=30, bpp=3, name=None, duration=10000, director=None):

        super().__init__(name=name, duration=duration, director=director)

        if type(pin) is not Pin:
            pin = Pin(pin, Pin.OUT)
        self.np = NeoPixel(pin, n, bpp)
        self.refresh_rate = 15
        self.need_update = True
        self.running = True
        self.duration = duration  # ms
        log.debug("{} lights on {}".format(self.np.n, self.np.pin))
        self.cmds['random'] = self.random
        self.cmds['fade'] = self.fade
        self.cmds['bounce'] = self.bounce
        self.cmds['chase'] = self.chase
        self.cmds['clear'] = self.clear

    def __getitem__(self, key):
        return self.np[key]

    def __setitem__(self, key, value):
        self.np[key] = value

    def do_update(self):
        self.np.write()
        self.need_update = False
        return False

    def get_sublights(self, lights):
        if lights is None:
            lights = [j for j in range(self.np.n)]
        return len(lights), lights
    
    async def random(self, brightness=0.1,
                     duration=5000, beat=300,
                     start=0, lights=None, **kwargs):
        n, lights = self.get_sublights(lights)
        while self.running:
            await self.wait_for_start(start)
            begin_ms = ticks_ms()
            while duration is None or (ticks_diff(ticks_ms(), begin_ms) < duration):
                for j in lights:
                    col = [int(c * brightness) for c in os.urandom(3)]
                    self.np[j] = col
                self.need_update = True
                await asyncio.sleep_ms(beat)
            else:
                await self.clear(lights)
                return
          
    async def chase(self,
                    color=(255, 255, 255), bgcolor=(0, 0, 0),
                    cycles=4,
                    duration=None, beat=200,
                    start=0, lights=None, **kwargs):
        n, lights = self.get_sublights(lights)
        while self.running:
            await self.wait_for_start(start)
            begin_ms = ticks_ms()
            if duration is None:
                duration = cycles * beat * n
            else:
                cycles = duration // (beat * n)
            for i in range(cycles * n):
                if ticks_diff(ticks_ms(), begin_ms) > duration:
                    await self.clear(lights)
                    return
                self.np[lights[(i-1) % n]] = bgcolor
                self.np[lights[i % n]] = color
                self.need_update = True
                await asyncio.sleep_ms(beat)
        await self.clear(lights)

    async def bounce(self,
                     color=(255, 255, 255), bgcolor=(0, 0, 0),
                     cycles=4,
                     duration=None, beat=100,
                     start=0, lights=None, **kwargs):
        await self.wait_for_start(start)
        n, lights = self.get_sublights(lights)
        if duration is None:
            duration = cycles * beat * n
        else:
            cycles = duration // (beat * n)
        begin_ms = ticks_ms()

        while self.running:
            for i in range(cycles * 2 * n):
                if ticks_diff(ticks_ms(), begin_ms) > duration:
                    await self.clear(lights)
                    return
                for j in lights:
                    self.np[j] = bgcolor
                if (i // n) % 2 == 0:
                    self.np[lights[i % n]] = color
                else:
                    self.np[lights[n - 1 - (i % n)]] = color
                self.need_update = True
                await asyncio.sleep_ms(beat)

    async def fade(self,
                   color=(255, 255, 255),
                   cycles=3, step=8, beat=30,
                   duration=None, start=0, lights=None, **kwargs):
        await self.wait_for_start(start)
        n, lights = self.get_sublights(lights)
        if duration is None:
            duration = cycles * beat * n
        begin_ms = ticks_ms()
        while self.running and ticks_diff(ticks_ms(), begin_ms) <= duration:
            log.debug("start fade, ticks==%d", ticks_diff(ticks_ms(), begin_ms))
            for val in range(0, 256, step):
                # log.info("val={}".format(val))
                for j in range(n):
                    self.np[lights[j]] = [val & v for v in color]
                self.need_update = True
                await asyncio.sleep_ms(beat)
                if ticks_diff(ticks_ms(), begin_ms) > duration:
                    await self.clear(lights)
                    return
            for val in range(255, -1, -step):
                # log.info("val={}".format(val))
                for j in range(n):
                    self.np[lights[j]] = [val & v for v in color]
                self.need_update=True
                await asyncio.sleep_ms(beat)
                if ticks_diff(ticks_ms(), begin_ms) > duration:
                    await self.clear(lights)
                    return
            for j in range(n):
                self.np[lights[j]] = (0, 0, 0)
            log.debug("stop fade, ticks==%d", ticks_diff(ticks_ms(), begin_ms))
            self.need_update = True
        await self.clear(lights)

    async def clear(self,lights=None, start=0, **kwargs):
        await self.wait_for_start(start)
        if lights is None:
            self.np.fill((0, 0, 0))
        else:
            for i in range(len(lights)):
                self.np[lights[i]] = (0, 0, 0)
        self.np.write()

    async def stop(self, clear=True, **kwargs):
        if clear:
            self.np.fill((0, 0, 0))
            self.np.write()
        self.running = False
        log.info("{}: stopping".format(self.name))


async def test():
    np = ArtNeoPixel(15, 30)
    log.info("fade 10-14...")
    await np.fade(color=(255, 0, 0), lights=[i for i in range(10, 15)])
    
    log.info("Random for first half...")
    await np.random(lights=[i for i in range(np.np.n // 2)])
    log.info("Fade...")
    await np.fade()
    log.info("Bounce...")
    await np.bounce()
    log.info("Chase...")
    await np.chase(color=(80, 5, 5), pause_ms=50)
    log.info("Random...")
    await np.random()
    log.info("Clearing..")
    np.cmd(cmd="clear")
    
async def simul_test():
    log.info("and now...simultaneously...")
    np = ArtNeoPixel(15, 30, duration=20000)
    log.info("fade 0-7...")
    np.cmd(cmd='fade', color=(255, 0, 0), lights=[i for i in range(8)])
    log.info("Random 8-14...at 0 for 2500 and at 5000 for 3000 msec")
    np.cmd(cmd="random", start=0, duration=2500, lights=[i for i in range(8, 15)])
    np.cmd(cmd="random", start=5000, duration=3000, lights=[i for i in range(8, 15)])
    # log.info("Bounce 15-22...")
    # np.cmd(cmd="bounce", lights=[i for i in range(15, 23)])
    # log.info("Chase 23-29")
    # np.cmd(cmd="chase", color=(0, 255, 0), lights=[i for i in range(23,30)])
    np.run(1)
    log.info("Clearing..")
    np.stop()
    await asyncio.sleep(0)
    np.cmd(cmd="clear")
    await asyncio.sleep(0)


def run_tests():
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(test())
    loop.run_until_complete(simul_test())  


if __name__ == "__main__":
    run_tests()
    








