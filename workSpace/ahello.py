async def hello():
    for _ in range(10):
        print('Hello world.')
        await asyncio.sleep(1)

