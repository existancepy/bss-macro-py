
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
def jump():
    pag.keyDown("w")
    move.press('space')
    sleep(0.25)
    pag.keyUp("w")

exec(open("field_stump.py").read())
for _ in range(4):
    move.press(',')
acchold("w",5)
jump()
acchold("w",5)
move.press(',')
jump()
move.press('.')
move.press('.')
jump()

    
