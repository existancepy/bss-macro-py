
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
move.hold("w",14)
move.press(",")
move.press(",")
move.press(",")
move.hold("d",6)
move.hold("w",6)
move.hold("a",1.2)
move.hold("w",6)
move.hold("d",3)
move.hold("s",0.6)

