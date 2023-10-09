import pyautogui as pag
import time
import os
import tkinter
import loadsettings

def hold(k,t):
    ws = loadsettings.load()["walkspeed"]
    pyautogui.keyDown(k)
    time.sleep(t*ws/28)
    pyautogui.keyUp(k)


        


