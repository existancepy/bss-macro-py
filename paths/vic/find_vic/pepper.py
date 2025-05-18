
side = 3
back = 0.6
self.keyboard.walk("s",1.4)
self.keyboard.walk("d",1)
for _ in range(2):
    self.keyboard.press(".")
self.keyboard.walk("a",side)
self.keyboard.walk("s",back)
self.keyboard.walk("d",side)
self.keyboard.walk("s",back)
self.keyboard.walk("a",side)
self.keyboard.walk("s",back)
self.keyboard.walk("d",side)

    
