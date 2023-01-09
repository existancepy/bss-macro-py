
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

move.hold("w",6)
move.hold("d",8)
move.hold("s",7)
move.hold("d",14)
move.hold("w",5)
move.press(",")
move.hold("w",12)
move.press(".")
move.hold("s",0.2)
move.hold("d",4)
move.hold("w",1.4)
move.hold("s",0.6)
