
side = 2.5
back = 1
time.sleep(1)
for _ in range(2):
    self.keyboard.press(",")
self.keyboard.walk("d",0.75)
self.keyboard.walk("d",side/2)
self.keyboard.walk("w",back)
self.keyboard.walk("a",side)
self.keyboard.walk("s",back)
self.keyboard.walk("d",side)
self.keyboard.walk("s",back)
self.keyboard.walk("a",side)

    
