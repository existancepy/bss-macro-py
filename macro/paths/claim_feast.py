def acchold(key, duration):
    ws = loadsettings.load()["walkspeed"]
    pag.keyDown(key)
    sleep(duration*ws/28)
    pag.keyUp(key)

sideTime = 0
frontTime = 0.45
move.press(",")
acchold('a',0.3)
for i in range(3):
    acchold("s", frontTime)
    acchold("d", sideTime)
    acchold("w", frontTime)
    acchold("d", sideTime)
for i in range(3):
    acchold("s", frontTime)
    acchold("a", sideTime)
    acchold("w", frontTime)
    acchold("a", sideTime)
   

    
