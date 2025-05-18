#go to strawberry
strawberry = self.getRespawnedMobs("strawberry")
if strawberry:
    self.killMob(strawberry[0], "strawberry",
    '''
self.keyboard.walk("w",5)
self.keyboard.keyDown("a")
time.sleep(4)
self.keyboard.press("space")
attackThread.start()
time.sleep(2.5)
self.keyboard.keyUp("a")
self.keyboard.walk("s",2)
    '''
    )
else:
    #go to mushroom
    mushroom = self.getRespawnedMobs("mushroom")
    if mushroom:
        self.killMob(mushroom[0], "mushroom", walkPath=
        '''
self.keyboard.walk("w",5)
self.keyboard.walk("a",4)
attackThread.start()
self.keyboard.walk("s",8)
        '''
        )
    else:
        #go to bamboo
        bamboo = self.getRespawnedMobs("bamboo")
        if bamboo:
            self.killMob(bamboo[0], "bamboo", walkPath=
        '''
self.keyboard.walk("w",5)
self.keyboard.walk("d",4)
self.keyboard.walk("s",1.5)
attackThread.start()
self.keyboard.walk("d",4.5)
        '''
        )