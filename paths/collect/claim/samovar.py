sideTime = 0.13
frontTime = 0.7
time.sleep(2)
self.keyboard.walk('w',0.8)
self.keyboard.walk('d',0.4)
for i in range(3):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("a", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("a", sideTime)
for i in range(3):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("d", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("d", sideTime)
   

    
