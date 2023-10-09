
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
def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

        
move.press(",")
move.press(",")
move.press("e")
sleep(0.08)
pag.keyDown("w")
move.press("space")
move.press("space")
sleep(3)
move.press(".")
move.press(".")
sleep(0.8)
pag.keyUp("w")
move.press("space")
sleep(0.6)

    
