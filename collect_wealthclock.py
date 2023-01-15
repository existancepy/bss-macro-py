
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
time.sleep(0.8)
pag.keyDown("w")
move.press("space")
move.press("space")
time.sleep(4.9)
move.press(",")
time.sleep(0.45)
pag.keyUp("w")
move.press("space")
time.sleep(1)
    
