
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
move.press(",")
move.press("e")
pag.keyDown("w")
time.sleep(0.35)
move.press("space")
move.press("space")
time.sleep(2.81)
move.press(",")
move.press(",")
time.sleep(1.35)
pag.keyUp("w")
move.press("space")
time.sleep(0.7)
    
