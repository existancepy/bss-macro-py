
side = 3
back = 0.6
vicSearchWalk("s",1.4)
vicSearchWalk("d",1)
for _ in range(2):
    self.keyboard.press(".")
vicSearchWalk("a",side)
vicSearchWalk("s",back)
vicSearchWalk("d",side)
vicSearchWalk("s",back)
vicSearchWalk("a",side)
vicSearchWalk("s",back)
vicSearchWalk("d",side)

    
