sideTime = 0.1
frontTime = 0.8
time.sleep(3)
self.keyboard.slowPress(".")
self.keyboard.slowPress(".")
self.keyboard.walk('a',0.2)
self.keyboard.walk('w',0.4)
for i in range(4):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("d", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("d", sideTime)

    