# This file is executed on every boot (including wake-boot from deepsleep)

import esp
esp.osdebug(None)

import wifi
wifi.connect(repl=True)

import gc
gc.collect()
#import webrepl
#webrepl.start()

