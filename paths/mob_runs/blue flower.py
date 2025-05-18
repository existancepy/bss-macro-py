#go to bamboo
bamboo = self.getRespawnedMobs("bamboo")
if bamboo:
    self.killMob(bamboo[0], "bamboo", walkPath=
'''
self.keyboard.walk("w",3)
self.keyboard.walk("d",7)
self.keyboard.keyDown("w")
time.sleep(0.5)
self.keyboard.press("space")
time.sleep(1)
self.keyboard.keyUp("w")
self.keyboard.walk("w", 5.5)
for _ in range(3):
    self.keyboard.press(",")
self.keyboard.walk("w",5)
for _ in range(3):
    self.keyboard.press(".")
self.keyboard.keyDown("a")
time.sleep(1)
self.keyboard.press("space")
time.sleep(1)
self.keyboard.press("space")
attackThread.start()
time.sleep(2.5)
self.keyboard.keyUp("a")
'''
)