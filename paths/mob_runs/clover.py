#go to blue flower
blueFlower = self.getRespawnedMobs("blue flower")
if blueFlower:
    self.killMob(blueFlower[0], "blue flower",
    '''
self.keyboard.walk("w",6)
attackThread.start()
    '''                       
    )