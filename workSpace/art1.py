import artpart
import artdirector
import artneo

ad = artdirector.ArtDirector('mac')

np = artneo.ArtNeoPixel(pin=15,n=30,name='neo',director=ad)

np.cmd({"cmd":"clear"})
np.cmd({"cmd":"random","lights":range(0,10)})

ad.add_part(np)

ap = artpart.ArtPart(name='test')
ap.cmd({"cmd": "test"})

ad.add_part(ap)

ad.list_cmds()

ad.run()
