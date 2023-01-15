
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



exec(open("field_blue flower.py").read())
move.apkey("space")
move.hold("s",3)
move.hold("a",4)
move.hold("w",1.5)
move.hold('d',0.1)
move.press(",")
move.hold("w",7)
