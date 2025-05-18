def jump(self):
    self.keyboard.keyDown("w")
    self.keyboard.slowPress('space')
    sleep(0.25)
    self.keyboard.keyUp("w")

self.runPath("cannon_to_field/mountain top")
for _ in range(4):
    self.keyboard.press(",")
self.keyboard.walk("w",3)
self.keyboard.walk("a",5.5)
self.keyboard.walk("d",0.76)
self.keyboard.walk("w",8)
jump(self)
self.keyboard.walk("w",5)
jump(self)
self.keyboard.walk("w",3)
self.keyboard.walk("a",0.05)
self.keyboard.walk("s",0.5)

    