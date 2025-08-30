
side = 2.8
back = 0.9

for _ in range(4):
    self.keyboard.press(",")
vicSearchWalk("w",3)
vicSearchWalk("a",3)
vicSearchWalk("d",0.6)
vicSearchWalk("s",0.7)
vicSearchWalk("d",side)
vicSearchWalk("s",back)
vicSearchWalk("a",side)
vicSearchWalk("s",back)
vicSearchWalk("d",side)
vicSearchWalk("s",back)
vicSearchWalk("a",side)



    
