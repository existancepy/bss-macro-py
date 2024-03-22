
ct = loadsettings.load()["canon_time"]

move.press(",")
move.press(",")
move.press("e")
time.sleep(0.8)
pag.keyDown("w")
move.press("space")
move.press("space")
sleep(2.6*ct)
move.press(".")
move.press(".")
sleep(3.55*ct)
pag.keyUp("w")
move.press("space")

    
