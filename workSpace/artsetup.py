import upip
import importlib
import wifi
wifi.connect()

def checkandget(mod_name):
    try:
        importlib.__import__(mod_name)
        print("{} is already installed.".format(mod_name))
    except ImportError:
        print("Installing {}".format(mod_name))
        upip.install('micropython-'+mod_name)
        
for mod_name in ['uasyncio','umqtt.simple','umqtt.robust']:
    checkandget(mod_name)

try:
    importlib.__import__("mqtt_as")
    print("mqtt_as is already installed.")
except ImportError:
    print("mqtt_as is at https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as")
