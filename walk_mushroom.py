
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
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


move.hold("s",4.5)
time.sleep(0.5)
move.apkey("space")
move.hold("a",6)
move.hold("w",10)
move.hold("d",12)
move.hold("w",1.4)
move.hold("s",0.6)

    
