
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


side = 3
back = 1.4
move.hold("d",1.33)
move.hold("w",0.4)

time.sleep(1)
move.hold("d",side/2)
move.hold("w",back/2)
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)



    
