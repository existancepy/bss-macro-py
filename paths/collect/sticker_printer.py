for _ in range(4):
    self.keyboard.press(".")
self.keyboard.slowPress("e")
sleep(0.95)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(0.55)
for _ in range(2):
    self.keyboard.slowPress(".")
sleep(2)
self.keyboard.slowPress("space")
for _ in range(2):
    self.keyboard.press(",")
sleep(0.5)

