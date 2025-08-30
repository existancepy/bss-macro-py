
side = 2.5
back = 1
time.sleep(1)
for _ in range(2):
    self.keyboard.press(",")
vicSearchWalk("d",0.75)
vicSearchWalk("d",side/2)
vicSearchWalk("w",back)
vicSearchWalk("a",side)
vicSearchWalk("s",back)
vicSearchWalk("d",side)
vicSearchWalk("s",back)
vicSearchWalk("a",side)

    
