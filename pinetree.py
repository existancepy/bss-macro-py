
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move

def go():
    pag.keyDown("d")
    pag.keyDown("s")
    time.sleep(0.5)
    move.press("space")
    move.press("space")
    time.sleep(2.7)
    pag.keyUp("s")
    time.sleep(1.9)  
    pag.keyUp("d")
    move.press("space")
    
