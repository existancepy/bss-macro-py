
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
move.hold("s",9)
move.hold("a",9)
move.hold("s",7)
move.press(",")
move.hold("w",3)
move.press(".")
move.hold("a",8)
move.hold("w",3)
move.hold("s",0.3)
move.hold("d",3)
move.hold("w",1)
move.hold("s",0.6)







    
