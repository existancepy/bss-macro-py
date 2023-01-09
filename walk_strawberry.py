
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


move.hold("s",5)
move.hold("a",6)
move.hold("w",8)
move.hold("a",0.8)
move.hold("w",5.5)
move.hold("d",3)
move.hold("s",0.6)

    
