#go to strawberry
strawberry = self.getRespawnedMobs("strawberry")
if strawberry:
    self.killMob(strawberry[0], "strawberry",
    '''
self.keyboard.walk("d",5)
self.keyboard.walk("s",9)
self.keyboard.walk("a",1)
attackThread.start()
self.keyboard.walk("s",3)
    '''                       
    )