import upip
import wifi
wifi.connect()

def getmodule(mod_name):
    print("Installing {}".format(mod_name))
    upip.install('micropython-'+mod_name)
        
for mod_name in ['uasyncio','umqtt.simple','umqtt.robust','logging']:
    getmodule(mod_name)

try:
    import mqtt_as
    print("mqtt_as is already installed.")
except ImportError:
    print("mqtt_as is not installed")
    print("mqtt_as.py is at https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as")
    print("please download from that location and copy to the ESP")
