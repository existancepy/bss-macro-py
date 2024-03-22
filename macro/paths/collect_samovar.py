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

exec(open("./paths/field_stump.py").read())
for _ in range(4):
    move.press(',')
acchold("w",5)
jump()
acchold("w",5)
move.press(',')
jump()
move.press('.')
move.press('.')
jump()

    
