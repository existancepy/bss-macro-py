
side = 2.8
back = 0.9

for _ in range(4):
    self.keyboard.press(",")
self.keyboard.walk("w",3)
self.keyboard.walk("a",3)
self.keyboard.walk("d",0.6)
self.keyboard.walk("s",0.7)
self.keyboard.walk("d",side)
self.keyboard.walk("s",back)
self.keyboard.walk("a",side)
self.keyboard.walk("s",back)
self.keyboard.walk("d",side)
self.keyboard.walk("s",back)
self.keyboard.walk("a",side)



    
