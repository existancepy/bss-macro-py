
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
    
move.press(",")
move.press(",")
move.press(",")
move.press("e")
time.sleep(0.3)
pag.keyDown("w")
move.press("space")
move.press("space")
move.press(",")
pag.keyUp("w")
move.press("space")
move.press(".")
move.press(".")
move.press(".")
move.press(".")

time.sleep(0.6)

    
