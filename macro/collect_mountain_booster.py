
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
from delay import sleep
ws = loadsettings.load()["walkspeed"]

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



move.press('e')
sleep(3)
move.hold("d",6)

