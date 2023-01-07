
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
ws = loadsettings.load()["walkspeed"]

def apd(k):
    cmd = """
        osascript -e  'tell application "System Events" to key down "{}"'
    """.format(k)
    os.system(cmd)
def apu(k):
    cmd = """
        osascript -e  'tell application "System Events" to key up "{}"'
    """.format(k)
    os.system(cmd)


move.hold("s",8)
move.hold("d",6)
move.hold("w",9)
move.hold("d",2)
pag.keyDown("d")
time.sleep(0.1)
move.press("space")
time.sleep(0.15*28/ws)
pag.keyUp("d")
move.hold("w",7)
move.hold("d",4)
move.hold("s",0.5)
move.hold("a",0.1)
pag.keyDown("s")
time.sleep(0.1)
move.press("space")
time.sleep(0.15*28/ws)
pag.keyUp("s")
while True:
    pag.keyDown("s")
    time.sleep(0.15)
    pag.keyUp("s")
    r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
    if r:
        break
time.sleep(2)
move.press("e")
move.hold("w",4)
move.hold("d",3)
move.hold("s",0.6)


    
