exec(open("./paths/field_blue flower.py").read())
move.apkey("space")
pag.keyDown("a")
sleep(8)
move.press("space")
sleep(0.2)
pag.keyUp("a")
move.hold("w",4)
move.hold("d",5)
move.hold("a",0.25)
move.hold("s",7)
