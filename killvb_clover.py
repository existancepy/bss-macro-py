
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
from delay import sleep

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


side = 2
back = 1

move.hold("w",back*3)
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)
move.hold("s",back)
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)



    
