import uasyncio as asyncio

async def hello():
    for _ in range(10):
        print('Hello world.')
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())  


