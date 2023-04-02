
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
from delay import sleep

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
    
move.press(".")
move.press("e")
sleep(0.12)
pag.keyDown("w")
move.press("space")
move.press("space")
sleep(4.2)
move.press(",")
sleep(1.5)
pag.keyUp("w")
move.press("space")
sleep(0.5)
move.hold("d",2.5)
for _ in range(3):
    pag.keyDown("w")
    move.press('space')
    sleep(0.2)
    pag.keyUp("w")
    
move.hold('w',2)
pag.keyDown("w")
move.press('space')
sleep(0.2)
pag.keyUp("w")
move.hold('w',4)
move.press(".")
pag.keyDown("w")
move.press('space')
sleep(0.2)
pag.keyUp("w")
move.hold('w',7)
move.press(",")
pag.keyDown("d")
move.press('space')
sleep(0.2)
pag.keyUp("d")
move.hold("d",1.9)
move.hold("s",2.9)




    
