from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython
from artneopixel import ArtNeoPixel
import json

# ESP8266 ESP-12 modules have blue, active-low LED on GPIO2, replace
# with something else if needed.
# led = Pin(2, Pin.OUT, value=1)
np=ArtNeoPixel(15,30)

# Default MQTT server to connect to
SERVER = "iot.eclipse.org"
SERVER = "192.168.1.56"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"manitou-iot"

state = 0

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    try:
        cmd = json.loads(msg)
        print("cmd: {}".format(cmd))
    except:
        print('not valid json')
    if cmd['cmd'] == "on":
        # led.value(0)
        np.fill((60,0,0))
        np.write()
        state = 1
    elif cmd['cmd'] == "off":
        # led.value(1)
        np.clear()
        state = 0
    elif cmd['cmd'] == "random":
        np.random()


def main(server=SERVER):
    print("connecting to {}".format(server))
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    print("subscribing to topic {}".format(TOPIC))
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    try:
        while 1:
            #micropython.mem_info()
            c.wait_msg()
    finally:
        c.disconnect()
        
if __name__ == '__main__':
    main()



