import network
import time
from machine import Pin
from wificonfig import ssids

def status():
    sta_if = network.WLAN(network.STA_IF)
    print('network config:', sta_if.ifconfig())

def connect(repl=False, ip=None ):
    led=Pin(2,Pin.OUT)
    led.off()
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        sta_if.active(True)

        for ssid, pwd in ssids:
            print('connecting to network...', ssid)

            sta_if.connect(ssid, pwd)
            curtime = time.time()

            while not sta_if.isconnected() and (time.time() - curtime) < 30:
                pass
            if sta_if.isconnected():
                if ip:
                    ifc=list(sta_if.ifconfig())
                    ifc[0]=ip
                    sta_if.ifconfig(tuple(ifc))
                break

    led.on()
    print('network config:', sta_if.ifconfig())
    # time.sleep(4)

    if repl and sta_if.isconnected():
        led.off()
        import webrepl
        webrepl.start()
        led.on()


if __name__ == '__main__':
    connect()



