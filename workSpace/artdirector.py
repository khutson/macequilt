import gc
from mqtt_as import MQTTClient
from config import config
import uasyncio as asyncio
from ucollections import deque # xxx need to change to uasyncio.queues
import json

from wificonfig import MQTT_SERVER
from artpart import ArtPart

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("ArtDirector")
gc.collect()
q = deque((), 20)


# Subscription callback
def sub_cb(topic, msg):
    print((topic, msg))
    q.append((topic,msg))
    print("len(q) == {}".format(len(q)))

async def wifi_han(state):
    print('Wifi is {}'.format('up' if state else 'down'))
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


class ArtDirector():
    """manages mqtt messages and other commands between ArtProject parts"""

    def __init__(self, name, cmdq=q):
        self.name = name # project name
        self.cmdq = cmdq
        self.running = False
        self.parts = {}
        self.cmds = {"stop":self.stop}
        log.debug("%s initialized", self.name)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.check_q())
        log.debug("running main")
        try:
            loop.run_until_complete(self.main(client, self.name))
        finally:
            log.debug("closing mqtt client")
            client.close()  # Prevent LmacRxBlk:1 errors

    async def stop(self):
        self.running = False

    async def main(self, client, topic):
        try:
            await client.connect()
        except OSError:
            log.warning('Connection failed.')
            return
        n = 0
        self.running = True
        while self.running:
            # xxx needs to handle publishing commands/statuses from the parts
            await asyncio.sleep(10)
            log.debug('publish %d', n)
            # If WiFi is down the following will pause for the duration.
            await client.publish('mac/asynctest', json.dumps({"count":n}), qos=1)
            n += 1

    async def check_q(self):
        while True:
            if self.running:
                log.debug("check_q: q length == {}".format(len(self.cmdq)))
                if len(self.cmdq):
                    topic, msg = self.cmdq.popleft()
                    topic = str(topic,'utf-8')
                    msg = str(msg, 'utf-8')
                    log.debug("check_q: topic = {}".format(topic))
                    # log.debug("check_q: msg   = {}".format(msg))
                    try:
                        msg_json = json.loads(msg)
                        log.debug("check_q: json = {}".format(msg_json))
                    except ValueError:
                        log.error("Invalid JSON command: {}".format(msg))
                        break
                    if topic in self.parts:
                        self.parts[topic].cmd(msg_json)
            await asyncio.sleep_ms(4000) # xxx need to shorten for production

    def add_part(self, part):
        """

        :type part: ArtPart
        """
        self.parts[self.name + "/" + part.name] = part
        part.director = self
        
    def help(self):
        print("ArtDirector(name='{}') with {} parts:".format(self.name,len(self.parts)))
        for partname, part in self.parts.items():
            print("PART: {}".format(partname))
            for cmd in part.cmds:
                print(" CMD: {}".format(cmd))

if __name__ == '__main__':
    ad = ArtDirector('adtest')
    ad.run()

