import uasyncio as asyncio

async def hello():
    for _ in range(10):
        print('Hello world.')
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()

hellofunc = hello()
loop.create_task(hellofunc)

loop.run_until_complete(asyncio.sleep_ms(15000))

# loop.run_until_complete(hellofunc)


