
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

move.hold("w",0.4)
move.hold("a",6)
move.hold("s",2)
move.press(".")
move.hold("w",12)
move.press(",")
move.hold("s",5)
move.hold("d",8)
move.hold("w",11)
move.hold("s",0.1)
move.hold("d",0.35)
move.hold("w",4)
move.hold("d",3)
move.hold("s",0.6)

    
