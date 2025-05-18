#Note: this path has been renamed to avoid being used by the macro
# go to pine tree
pineTreeMobs = self.getRespawnedMobs("pine tree")
if pineTreeMobs:
    self.killMob(pineTreeMobs[0], "pine tree", walkPath=
    '''
self.keyboard.walk("d",1.2)
self.keyboard.multiWalk(["w","d"],6)
self.keyboard.walk("a",2.5)
attackThread.start()
self.keyboard.walk("w",8)
self.keyboard.walk("a",0.3)
    '''
    )