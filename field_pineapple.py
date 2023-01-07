
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

move.press("e")
apd("a")
time.sleep(1.15)
move.press("space")
move.press("space")
time.sleep(1)
apd("s")
time.sleep(1.4)
apu("s")
time.sleep(0.02)
apu("a")
move.press("space")
time.sleep(0.5)
    
