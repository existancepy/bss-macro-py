
if sizeword.lower() == "xs":
    size = 0.5
elif sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "l":
    size = 2
elif sizeword.lower() == "xl":
    size = 2.5
else:
    size = 1.5
    
wm = 0.2*size
sm = 0.65*size
move.hold("a",width*wm*2)
move.hold("s",sm)
for _ in range(width):
    move.hold("d",wm)
    move.hold("w",sm)
    move.hold("d",wm)
    move.hold("s",sm)
    
move.hold("a",width*wm*2)
move.hold("w",sm)
for _ in range(width):
    move.hold("d",wm)
    move.hold("s",sm)
    move.hold("d",wm)
    move.hold("w",sm)


        
