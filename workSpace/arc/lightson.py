def run():
  import ArtNeoPixel as anp
  np=anp.ArtNeoPixel(15,1)

  np.fade(cycles=10)
  np.fill((255,255,255))
  np.write()
  
if __name__ == '__main__':
  run()
