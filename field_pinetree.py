
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


move.apdown("d")
move.apdown("s")
time.sleep(0.2)
move.press("space")
move.press("space")
time.sleep(2.9)
move.apup("s")
time.sleep(1.7)  
move.apup("d")
move.press("space")
    
