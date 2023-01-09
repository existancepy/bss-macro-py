
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move


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
    
move.hold("d",4)
move.hold("s",3)
pag.keyDown("s")
move.press('space')
time.sleep(0.2)
pag.keyUp("s")
move.hold("s",5)
move.hold("a",5)
move.hold("w",4)
move.hold("s",0.2)
move.hold("d",7)
move.hold("w",1)
move.hold("s",0.6)





    
