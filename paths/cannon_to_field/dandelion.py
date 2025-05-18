
self.keyboard.press(",")
self.keyboard.press(",")
self.keyboard.slowPress("e")
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(0.45)
self.keyboard.press(".")
self.keyboard.press(".")
sleep(1)
self.keyboard.keyUp("w")
self.keyboard.slowPress("space")
for _ in range(2):
    self.keyboard.press(",")
sleep(0.6)


    
