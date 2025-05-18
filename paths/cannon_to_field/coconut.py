
self.keyboard.press(".")
self.keyboard.slowPress("e")
sleep(0.12)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(4.2)
self.keyboard.slowPress(",")
sleep(1.5)
self.keyboard.keyUp("w")
self.keyboard.slowPress("space")
sleep(0.5)
self.keyboard.walk("d",2.5)
for _ in range(3):
    self.keyboard.keyDown("w")
    self.keyboard.slowPress('space')
    sleep(0.2)
    self.keyboard.keyUp("w")
    
self.keyboard.walk('w',2)
self.keyboard.press("space")
self.keyboard.walk('a',2.5)



    
