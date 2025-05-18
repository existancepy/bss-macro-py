for _ in range(3):
    self.keyboard.press(".")
self.keyboard.slowPress("e")
sleep(0.08)
self.keyboard.keyDown("w")
sleep(0.5)
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(2.7)
self.keyboard.slowPress(",")
sleep(3.5)
self.keyboard.keyUp("w")
self.keyboard.walk("d",4, False)
self.keyboard.walk("w",2)
self.keyboard.press(".")
for i in range (8):
    self.keyboard.walk("s",0.3)
    if self.isBesideE(["honey"]):
        break
    time.sleep(0.15)