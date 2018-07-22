import artneo
import uasyncio as asyncio
try:
     print(np)
except:
     np = artneo.ArtNeoPixel(15, 30, duration=20000)

np.cmd(cmd='random', start=500, duration=9000,
     lights=[17,18,19,20,21])
np.cmd(cmd='fade', duration=6000, color=(255,0,0),
     lights=[23,25,27,29])
np.cmd(cmd='fade', start=3000,
     lights=[22,24,26,28], color=(0,255,0), duration=7000)

np.cmd(cmd='chase', cycles=5, beat=400,
     lights=[i for i in range(12,17)])

np.cmd(cmd='bounce', duration=15000,
     lights=[i for i in range(5,12)])

np.run()
