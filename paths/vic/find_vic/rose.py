
side = 2.1
back = 1.2

for _ in range(2):
    self.keyboard.press(".")
vicSearchWalk("a",1)
vicSearchWalk("w",0.4)
time.sleep(1)
vicSearchWalk("d",side)
vicSearchWalk("w",back)
vicSearchWalk("a",side)
vicSearchWalk("s",back)
vicSearchWalk("d",side)
vicSearchWalk("s",back)
vicSearchWalk("a",side)
vicSearchWalk("s",back)
vicSearchWalk("d",side)
vicSearchWalk("w",back*0.8)


    
