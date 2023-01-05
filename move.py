import pyautogui as pag
import time
import os
import tkinter
import loadsettings
def apdown(k):
    cmd = """
        osascript -e  'tell application "System Events" to key down "{}"'
    """.format(k)
    os.system(cmd)
def apup(k):
    cmd = """
        osascript -e  'tell application "System Events" to key up "{}"'
    """.format(k)
    os.system(cmd)
    
def hold(k,t):
    ws = loadsettings.load()["walkspeed"]
    pag.keyDown(k)
    time.sleep(t*ws/28)
    pag.keyUp(k)

def press(k):
    pag.keyDown(k)
    time.sleep(0.08)
    pag.keyUp(k)


        


