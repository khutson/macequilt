from machine import Pin, PWM
import uasyncio as asyncio

class LED_async():
    def __init__(self, led_no):
        self.led = Pin(led_no,Pin.OUT)
        self.rate = 0
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())

    async def run(self):
        while True:
            if self.rate <= 0:
                await asyncio.sleep_ms(200)
            else:
                self.led.value(not self.led.value())
                await asyncio.sleep_ms(int(500 / self.rate))

    def flash(self, rate): # rate: blinks per second
        self.rate = rate

    def on(self):
        self.led.on()
        self.rate = 0

    def off(self):
        self.led.off()
        self.rate = 0
        
async def test(pin=5,delay=10,rate=1):
    led = LED_async(pin)
    print('test-on')
    led.on()
    print('waiting {} seconds'.format(delay))
    await asyncio.sleep(delay)
    print('test-rate={} per second'.format(rate))
    led.flash(rate)
    print('waiting {} seconds'.format(delay))
    await asyncio.sleep(delay)
    print('test-off')
    led.off()
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())  


