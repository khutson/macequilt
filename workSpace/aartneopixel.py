from machine import Pin
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff
import os
try:
    import uasyncio as asyncio
except ImportError:
    print("install uasyncio with import upip; upip.install('micropython-uasyncio')")


class ArtNeoPixel(NeoPixel):

    def __init__(self, pin, n, bpp=3,seq_duration=10000):
        if type(pin) is int:
            pin = Pin(pin, Pin.OUT)
        super().__init__(pin, n, bpp)
        self.refresh_rate = 15
        self.seq_duration = seq_duration # ms
        print("{} lights on {}".format(self.n, self.pin))
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())

    async def run(self):
        start_ms = ticks_ms()
        self.running = True
        while self.running:
            self.seq_ms = ticks_diff(ticks_ms(),start_ms)
            if self.seq_ms > self.seq_duration:
                start_ms = ticks_ms()
                self.seq_ms = 0
            if self.refresh_rate <= 0:
                await asyncio.sleep_ms(200)
            else:
                print("duration={}, seq_ms={},start_ms={}".format( \
                        self.seq_duration,self.seq_ms,start_ms))
                print("run: self[0]={}".format(self[0]))
                self.write()
                await asyncio.sleep_ms(self.refresh_rate)
    
    def get_sublights(self,lights):
        if lights is None:
            lights = [ j for j in range(self.n)]
        return len(lights), lights
    
    async def wait_for_start(self, start_ms):
        while start_ms > self.seq_ms:
            await asyncio.sleep_ms(0)
            
    async def arandom(self, duration=5000, pause_ms=100, 
                      brightness=0.1, lights=None,
                      start_ms=0):
        await self.wait_for_start(start_ms)
        n, lights = self.get_sublights(lights)
        start_ms = ticks_ms()
        while ticks_diff(ticks_ms(), start_ms) < duration:
            for j in lights:
                col = tuple([int(c * brightness) for c in os.urandom(3)])
                self[j] = col
            await asyncio.sleep_ms(pause_ms)
          
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
  
    async def abounce(self, color=(63,0,0), pause_ms=25, num_cycles=4, lights=None):
        n, lights = self.get_sublights(lights)
        for i in range(4 * n):
            self.fill(color)
            if (i // n) % 2 == 0:
                self[i % n] = (0, 0, 0)
            else:
                self[n - 1 - (i % n)] = (0, 0, 0)
            await asyncio.sleep_ms(pause_ms)
  

    async def afade(self, duration=None, cycles=1, 
                    color=(255,255,255), pause_ms=25, lights=None):
        n, lights = self.get_sublights(lights)
        for c in range(cycles):
            for i in range(0, 2 * 256, 8):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                print("i={}, val={}".format(i,val))
                for j in range(n):
                    self[lights[j]] = (val,val,val) # [val & v for v in color] 
                await asyncio.sleep_ms(pause_ms)

    async def afade2(self, duration=None, cycles=1, 
                    color=(255,255,255), pause_ms=200, lights=None):
        n, lights = self.get_sublights(lights)
        for c in range(cycles):
            for val in range(7, 256, 8):
                print("val={}".format(val))
                for j in range(n):
                    self[lights[j]] = [val & v for v in color] 
                await asyncio.sleep_ms(pause_ms)
            for val in range(248, -1, -8):
                print("val={}".format(val))
                for j in range(n):
                    self[lights[j]] = [val & v for v in color] 
                await asyncio.sleep_ms(pause_ms)

    def clear(self):
        self.fill((0,0,0))
        self.write()
        
async def test():
    np = ArtNeoPixel(15, 30)
    print("fade 10-14...")
    await np.afade(cycles=4, color=(255,0,0), lights=[i for i in range(10,15)])
    
    print("Random for first half...")
    await np.arandom(lights=[i for i in range(np.n//2)])
    print("Fade...")
    await np.afade()
    print("Bounce...")
    await np.abounce()
    print("Chase...")
    await np.achase(color=(80,5,5),pause_ms=50)
    print("Random...")
    await np.arandom()
    print("Clearing..")
    np.clear()
    
async def simul_test():
    print("and now...simultaneously...")
    np = ArtNeoPixel(15, 30,seq_duration=2)
    loop = asyncio.get_event_loop()
    print("fade 0-7...")
    loop.create_task( np.afade2(cycles=1, color=(255,0,0), lights=[i for i in range(8)]))
    #print("Random 8-14...")
    # loop.create_task( np.arandom(lights=[i for i in range(8,15)]))
    # print("Bounce 15-22...")
    # loop.create_task( np.abounce(lights=[i for i in range(15,23)]))
    # print("Chase...")
    # loop.create_task( np.achase(color=(80,5,5),pause_ms=50,lights=[ i for i in range(22,30)]))
    await asyncio.sleep(10)
    print("Clearing..")
    np.running=False
    await asyncio.sleep(0)
    np.clear()
    
def run_tests():
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(test())  
    loop.run_until_complete(simul_test())  


if __name__ == "__main__":
    run_tests()
    





