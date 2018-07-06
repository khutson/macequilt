from mqtt_as import config
from sys import platform

# Include any cross-project settings.

if platform == 'esp32':
    config['ssid'] = 'NETGEAR84'  # EDIT if you're using ESP32
    config['wifi_pw'] = 'yellowtrail736'
