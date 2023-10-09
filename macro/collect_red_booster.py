
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



exec(open("field_rose.py").read())
move.apkey("space")
move.hold("s",1)
move.hold("a",4)
move.hold("s",3)
move.hold("w",4.3)
move.hold("d",1.6)
move.hold("w",4)
