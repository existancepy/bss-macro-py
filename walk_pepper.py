
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
move.hold("s",8)
move.hold("a",9)
move.hold("s",7)
move.press(",")
move.hold("w",2.5)
move.press(".")
move.hold("a",6)







    
