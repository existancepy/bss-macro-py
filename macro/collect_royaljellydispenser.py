
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


move.press(",")
move.press("e")
pag.keyDown("w")
time.sleep(0.1)
move.press("space")
move.press("space")
time.sleep(3.2)
pag.keyUp("w")
move.press("space")
time.sleep(0.5)
move.hold("w",1.8)
move.press(".")
move.press(".")
move.hold("w",1.8)
    
