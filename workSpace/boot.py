# This file is executed on every boot (including wake-boot from deepsleep)

import esp
esp.osdebug(None)

import wifi
wifi.connect()

#import webrepl
#webrepl.start()

import gc
gc.collect()


