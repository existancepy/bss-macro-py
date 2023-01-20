
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
time.sleep(0.2)
move.press("e")
pag.keyDown("w")
time.sleep(1.15)
move.press("space")
move.press("space")
time.sleep(2.5)
move.press(",")
move.press(",")
move.press(".")
move.press(".")
time.sleep(1.6)
move.press("space")
pag.keyUp("w")
move.press(".")
move.press(".")
time.sleep(0.2)
    
