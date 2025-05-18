
self.keyboard.press(".")
self.keyboard.press(".")
self.keyboard.slowPress("e")
sleep(0.11)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(2.9)
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.keyUp("w")
self.keyboard.slowPress("space")
for _ in range(2):
    self.keyboard.press(".")
sleep(0.6)

    
