
self.keyboard.slowPress(".")
self.keyboard.slowPress(".")
self.keyboard.slowPress("e")
sleep(0.08)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(1.1)
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
sleep(0.6)
self.keyboard.keyUp("w")
self.keyboard.slowPress("space")
for _ in range(2):
    self.keyboard.press(".")
sleep(0.8)
    
