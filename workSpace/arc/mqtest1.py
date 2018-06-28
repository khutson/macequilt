from mqtt_as import MQTTClient
from config import config
import uasyncio as asyncio

SERVER = 'iot.eclipse.org'  # Change to suit e.g. 'iot.eclipse.org'

def callback(topic, msg):
    print((topic, msg))

async def conn_han(client):
    await client.subscribe('manitou-iot', 1)

async def main(client):
    await client.connect()
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{}'.format(n), qos = 1)
        n += 1

config['subs_cb'] = callback
config['connect_coro'] = conn_han
config['server'] = SERVER

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors

