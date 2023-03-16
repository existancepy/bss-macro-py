
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

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

move.press(",")
move.press(",")
move.press("e")
pag.keyDown("w")
sleep(0.4)
move.press("space")
move.press("space")
sleep(3.93)
move.press(".")
move.press(".")
sleep(0.5)
pag.keyUp("w")


    
