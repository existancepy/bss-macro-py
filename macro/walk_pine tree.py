
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


move.hold("d",5)
move.hold("s",7)
move.apkey('space')
pag.keyDown("a")
time.sleep(12*28/ws)
pag.keyUp("a")
move.hold("w",8)
move.hold("d",4)
move.hold("s",1)
move.hold("w",1.2)
move.press("space")
time.sleep(0.1)
move.press("space")
time.sleep(8)
move.hold("w",13)
move.hold("s",1)
move.hold("d",5)
move.hold("w",1)
move.hold("s",0.55)

    
