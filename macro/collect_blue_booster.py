
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



exec(open("field_blue flower.py").read())
move.apkey("space")
pag.keyDown("a")
sleep(8)
move.press("space")
sleep(0.2)
pag.keyUp("a")
move.hold("w",4)
move.hold("d",5)
move.hold("a",0.25)
move.hold("s",7)
