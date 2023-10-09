
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
sleep(2.7)
move.press(",")
sleep(1.6)
pag.keyUp("w")
move.press("space")
move.press(",")
move.press(",")
sleep(0.6)
    
