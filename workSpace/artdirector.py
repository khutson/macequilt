
from mqtt_as import MQTTClient
from config import config
import uasyncio as asyncio
from ucollections import deque
from machine import Pin

from wificonfig import MQTT_SERVER
# SERVER = '192.168.1.56'  # Change to suit

q = deque((),20)


# Subscription callback
def sub_cb(topic, msg):
    print((topic, msg))
    q.append((topic,msg))
    print("len(q) == {}".format(len(q)))

async def wifi_han(state):
    print('Wifi is ', 'up' if state else 'down')
    await asyncio.sleep(1)


# If you connect with clean_session True, must re-subscribe (MQTT spec 3.1.2.4)
async def conn_han(client):
    await client.subscribe('mac/#', 1)

# Define configuration
config['subs_cb'] = sub_cb
config['wifi_coro'] = wifi_han
config['connect_coro'] = conn_han
config['clean'] = True
config['server'] = MQTT_SERVER

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)



async def main(client,topic):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        return
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish('mac/asynctest', '{} {}'.format(n, client.REPUB_COUNT), qos=1)
        n += 1


class ArtDirector():
    """manages mqtt messages and other commands between ArtProject components"""

    def __init__(self, name, cmdq=q):
        self.name = name # project name
        self.cmdq = cmdq
        self.parts = {}

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.check_q())
        try:
            loop.run_until_complete(main(client, self.name))
        finally:
            client.close()  # Prevent LmacRxBlk:1 errors

    async def check_q(self):
        while True:
            print("check_q: q length == {}".format(len(self.cmdq)))
            if len(self.cmdq):
                topic, msg = self.cmdq.popleft()
                print("check_q: topic = {}".format(topic))
                print("check_q: msg   = {}".format(msg))
                if topic in self.parts:
                    try:
                        msg_json = json.loads(msg)
                    except ValueError:
                        print("Invalid JSON command: {}".format(msg))
                        break
                    self.parts[topic].cmd(msg_json)
            await asyncio.sleep_ms(4000)

    def add_part(self, part):
        """

        :type part: ArtPart
        """
        self.parts[part.name] = self.name + "/" + part
        
    def list_cmds(self):
        print("{} parts".format(len(self.parts)))
        for part in self.parts:
            print("PART: {}".format(part.name))
            for cmd in part.cmds:
                print(" CMD: {}".format(cmd))

if __name__ == '__main__':
    ad = ArtDirector('adtest')
    ad.run()

