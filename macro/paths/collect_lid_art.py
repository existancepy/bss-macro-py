def acchold(key, duration):
    ws = loadsettings.load()["walkspeed"]
    pag.keyDown(key)
    sleep(duration*ws/28)
    pag.keyUp(key)
def jump():
    pag.keyDown("w")
    move.press('space')
    sleep(0.25)
    pag.keyUp("w")

exec(open("./paths/field_mountain top.py").read())
for _ in range(4):
    move.press(".")
acchold("w",1)
move.press(".")
acchold("w",3)
move.press(",")
move.press(",")
move.press(",")
acchold("w",6)
move.press(".")
move.press(".")
acchold("d",0.5)
acchold("w",8)
jump()
acchold("w",5)
jump()
acchold("w",3)
acchold("s",0.5)

    
