
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
move.press("e")
sleep(0.12)
pag.keyDown("w")
move.press("space")
move.press("space")
sleep(3.7)
move.press(".")
sleep(0.2)
pag.keyUp("w")
move.press("space")
time.sleep(0.5)
move.hold("w",0.8)
