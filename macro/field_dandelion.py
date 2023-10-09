
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
    
move.press(",")
move.press(",")
move.press("e")
pag.keyDown("w")
move.press("space")
move.press("space")
sleep(0.45)
move.press(".")
move.press(".")
sleep(0.9)
pag.keyUp("w")
move.press("space")
sleep(0.6)


    
