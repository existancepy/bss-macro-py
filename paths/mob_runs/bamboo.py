#go to blue flower
blueFlower = self.getRespawnedMobs("blue flower")
if blueFlower:
    self.killMob(blueFlower[0], "blue flower",
    '''
self.keyboard.walk("d",7)
self.keyboard.walk("w",5)
attackThread.start()
self.keyboard.walk("s",6.5)
self.keyboard.walk("a",3)
    '''                       
    )