
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
back = 0.6
move.hold("s",1.4)
move.hold("d",1)
for _ in range(6):
    keyboard.press(",")
    time.sleep(0.03)
    keyboard.release(",")
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)
move.hold("s",back)
move.hold("a",side)
move.hold("s",back)
move.hold("d",side)

    
