from machine import Pin, PWM
import uasyncio as asyncio

class LED_async():
    def __init__(self, led_no):
        self.led = Pin(led_no)
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

    def flash(self, rate):
        self.rate = rate

    def on(self):
        self.led.on()
        self.rate = 0

    def off(self):
        self.led.off()
        self.rate = 0

if __name__ == '__main__':
    led = LED_async(16)
    led.on()
    asyncio.sleep_ms(1000)
    led.off()
    
