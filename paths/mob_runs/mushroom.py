#go to strawberry
strawberry = self.getRespawnedMobs("strawberry")
if strawberry:
    self.killMob(strawberry[0], "strawberry",
    '''
self.keyboard.walk("w",4)
self.keyboard.walk("a",7)
self.keyboard.walk("d",1)
self.keyboard.keyDown("w")
time.sleep(0.5)
self.keyboard.press("space")
time.sleep(2)
self.keyboard.keyUp("w")
attackThread.start()
self.keyboard.walk("a",1)
    '''                       
    )
else:
    #go to spider
    spider = self.getRespawnedMobs("spider")
    if spider:
        self.killMob(spider[0], "spider",
        '''
self.keyboard.walk("w",4)
self.keyboard.keyDown("d")
time.sleep(8)
self.keyboard.press("space")
time.sleep(0.4)
self.keyboard.keyUp("d")
attackThread.start()
self.keyboard.walk("w",4)
        '''                          
        )