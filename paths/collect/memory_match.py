for _ in range(2):
    self.keyboard.press(",")
self.keyboard.press("e")
self.keyboard.keyDown("w")
sleep(0.8)
for _ in range(2):
    self.keyboard.press("space")
sleep(3)
for _ in range(2):
    self.keyboard.press(",")
sleep(1.8)
self.keyboard.press("space")
self.keyboard.keyUp("w")
sleep(0.2)
self.keyboard.walk("a",0.4)