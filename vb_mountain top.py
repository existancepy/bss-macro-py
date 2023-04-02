
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


side = 2.5
back = 1
time.sleep(1)
for _ in range(2):
    keyboard.press(",")
    time.sleep(0.03)
    keyboard.release(",")
move.hold("d",0.75)
move.hold("d",side/2)
move.hold("w",back)
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)
move.hold("s",back)
move.hold("a",side)

    
