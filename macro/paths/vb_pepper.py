
side = 3
back = 0.6
move.hold("s",1.4)
move.hold("d",1)
for _ in range(6):
    keyboard.press(",")
    time.sleep(0.03)
    keyboard.release(",")
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)
move.hold("s",back)
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)

    
