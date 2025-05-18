for _ in range(4):
    self.keyboard.press(".")
time.sleep(2)
self.keyboard.walk("w",0.2)
for _ in range(3):
    self.keyboard.walk("s",0.4)
    self.keyboard.walk("a",0.3)
    self.keyboard.walk("w",0.55)
    self.keyboard.walk("d",0.4)