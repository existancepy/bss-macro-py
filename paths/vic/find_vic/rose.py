
side = 2.1
back = 1.2

for _ in range(2):
    self.keyboard.press(".")
self.keyboard.walk("a",1)
self.keyboard.walk("w",0.4)
time.sleep(1)
self.keyboard.walk("d",side)
self.keyboard.walk("w",back)
self.keyboard.walk("a",side)
self.keyboard.walk("s",back)
self.keyboard.walk("d",side)
self.keyboard.walk("s",back)
self.keyboard.walk("a",side)
self.keyboard.walk("s",back)
self.keyboard.walk("d",side)
self.keyboard.walk("w",back*0.8)


    
