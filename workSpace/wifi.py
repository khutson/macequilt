import network
import time

#add ssid and password here as needed
ssids = [ ('tsati','hutonetwo'),
                ('NETGEAR84','yellowtrail736'),
                ]
                
def connect(ip=None,repl=False):

    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        sta_if.active(True)
        
        for ssid, pwd in ssids:
          print('connecting to network...',ssid)

          sta_if.connect(ssid, pwd)
          curtime = time.time()

          while not sta_if.isconnected() and (time.time()-curtime)<30 :
              pass
          if sta_if.isconnected():
            break

    print('network config:', sta_if.ifconfig())
    time.sleep(4)
    
    if repl and sta_if.isconnected():
      import webrepl
      webrepl.start()




if __name__ == '__main__':
  connect()


