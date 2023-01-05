
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


apd("d")
apd("s")
time.sleep(0.5)
move.press("space")
move.press("space")
time.sleep(2.7)
pag.keyUp("s")
time.sleep(1.9)  
pag.keyUp("d")
move.press("space")
    
