#go to mushroom
mushroomMobs = self.getRespawnedMobs("mushroom")
if mushroomMobs:
    self.killMob(mushroomMobs[0], "mushroom", walkPath=
    '''
self.keyboard.walk("w",3)
self.keyboard.walk("d",5)
attackThread.start()
self.keyboard.walk("s",5)
self.keyboard.walk("d",1.5)
    '''
    )
else:
    #go to spider
    spider = self.getRespawnedMobs("spider")
    if spider:
        self.killMob(spider[0], "spider", walkPath=
        '''
self.keyboard.walk("a",5)
self.keyboard.walk("s",4)
self.keyboard.walk("d",7)
attackThread.start()
self.keyboard.walk("w",2.5)
        '''
        )