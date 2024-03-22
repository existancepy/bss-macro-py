def acchold(key, duration):
    ws = loadsettings.load()["walkspeed"]
    pag.keyDown(key)
    sleep(duration*ws/28)
    pag.keyUp(key)

sideTime = 0
frontTime = 0.45
acchold('w',0.8)
acchold('d',0.2)
for i in range(3):
    acchold("s", frontTime)
    acchold("a", sideTime)
    acchold("w", frontTime)
    acchold("a", sideTime)
for i in range(3):
    acchold("s", frontTime)
    acchold("d", sideTime)
    acchold("w", frontTime)
    acchold("d", sideTime)
   

    
