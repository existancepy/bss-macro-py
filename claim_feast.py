
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move

time.sleep(0.5)
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

def acchold(key, duration):
    ws = loadsettings.load()["walkspeed"]
    pag.keyDown(key)
    sleep(duration*ws/28)
    pag.keyUp(key)

sideTime = 0
frontTime = 0.45
move.press(",")
acchold('a',0.3)
for i in range(3):
    acchold("s", frontTime)
    acchold("d", sideTime)
    acchold("w", frontTime)
    acchold("d", sideTime)
for i in range(3):
    acchold("s", frontTime)
    acchold("a", sideTime)
    acchold("w", frontTime)
    acchold("a", sideTime)
   

    
