
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
    
move.press(".")
move.press(".")
move.press(".")
move.press("e")
sleep(0.08)
pag.keyDown("w")
sleep(0.5)
move.press("space")
move.press("space")
sleep(1.9)
move.press(",")
move.press(".")
sleep(0.08)
move.press(".")
pag.keyUp("w")
move.press("space")
sleep(0.5)
move.press(",")
move.press(",")
move.press(",")
move.press(",")




    
