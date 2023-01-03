import pyautogui as pag
import time
import os
import tkinter
import loadsettings

def hold(k,t):
    ws = loadsettings.load()["walkspeed"]
    pag.keyDown(k)
    time.sleep(t*ws/28)
    pag.keyUp(k)

def press(k):
    pag.keyDown(k)
    time.sleep(0.08)
    pag.keyUp(k)


        


