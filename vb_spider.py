
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


side = 2.8
back = 0.9

for _ in range(4):
    keyboard.press(",")
    time.sleep(0.03)
    keyboard.release(",")
move.hold("w",3)
move.hold("a",3)
move.hold("d",0.6)
move.hold("s",0.7)
move.hold("d",side)
move.hold("s",back)
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)
move.hold("s",back)
move.hold("a",side)



    
