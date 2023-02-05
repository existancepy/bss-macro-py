
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
move.apkey("space")
pag.keyDown("a")
time.sleep(12*28/ws)
pag.keyUp("a")
move.hold("w",8)
move.press("space")
time.sleep(0.1)
move.press("space")
pag.keyDown("w")
time.sleep(4)
move.press(".")
time.sleep(0.5)
move.press('space')
pag.keyUp("w")
move.hold("w",8)
move.press(",")
move.hold("s",0.6)

    
