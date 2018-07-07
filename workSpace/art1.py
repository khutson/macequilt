import artpart
import artdirector
import artneo

ad = artdirector.ArtDirector('mac')

np = artneo.ArtNeoPixel(pin=15,n=30,name='neo',director=ad)

np.cmd({"cmd":"clear"})
np.cmd({"cmd":"random","lights":range(0, 7), "duration":4000})
np.cmd({"cmd":"fade", "lights":range(7, 14), "duration":4000})
np.cmd({"cmd":"bounce","lights":range(14, 21), "duration":4000})
np.cmd({"cmd":"chase","lights":range(21, 28), "duration":4000})
np.cmd({"cmd":"clear","start":5000})

np.run(1)

ad.add_part(np)

ap = artpart.ArtPart(name='test')
ap.cmd({"cmd": "test"})

ad.add_part(ap)

ad.list_cmds()

ad.run()
