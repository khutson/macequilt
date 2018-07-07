
#import lightson
#lightson.run()

def run(coro, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro(*args, **kwargs))
