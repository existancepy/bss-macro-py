
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
    
move.press(".")
move.press(".")
move.press(".")
move.press("e")
time.sleep(0.08)
pag.keyDown("w")
time.sleep(0.5)
move.press("space")
move.press("space")
time.sleep(1.4)
move.press(",")
time.sleep(0.35)
move.press("space")
pag.keyUp("w")
move.press(",")
move.press(",")
time.sleep(0.5)




    
