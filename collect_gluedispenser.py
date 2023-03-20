
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
from delay import sleep
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

move.press("e")
sleep(0.5)
pag.keyDown("w")
move.press("space")
move.press("space")
sleep(5)
pag.keyUp("w")
time.sleep(2)
move.hold("w",2.85)
move.hold("a",1.2)
