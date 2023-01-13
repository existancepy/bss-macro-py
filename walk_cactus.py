
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


move.press(".")
move.press(".")
move.press(".")
move.hold("w",15)
move.press(",")
move.press(",")
move.press(",")
pag.keyDown("a")
time.sleep(12*28/ws)
pag.keyUp("a")
move.apdown("w")
time.sleep(8*28/ws)
move.press("space")
time.sleep(11*28/ws)
move.apup("w")
move.hold("d",1)
move.hold("w",4)
move.hold("d",3)
move.hold("s",0.6)

    
