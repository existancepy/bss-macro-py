
import pyautogui as pag
import time
import os
import tkinter
import move
import sys
import cv2
from PIL import ImageGrab
import numpy as np
import imagesearch
import loadsettings
import subprocess
import tkinter as tk
import tty
from tkinter import ttk
import backpack
from webhook import webhook
import webbrowser
import reset
import _darwinmouse as mouse
import ast
import getHaste
import pytesseract

def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(1)
mport pyautogui as pag
import time
import os
import tkinter
import imagesearch
from webhook import webhook
import loadsettings
from delay import sleep
from pynput.mouse import Button, Controller
from pynput.keyboard import Key
import pynput.keyboard
from pixelcolour import getPixelColor
from logpy import log
keyboard = pynput.keyboard.Controller()
mouse = Controller()
savedata = {}
mw,mh = pag.size()
tar =  (127, 108, 41)
var = 20
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]

def resetGet():
    setdat = loadsettings.load()
   
    rhd = setdat["reverse_hive_direction"]
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    
    loadSave()
    for i in range(2):
        webhook("","Resetting character, Attempt: {}".format(i+1),"dark brown")
        mouse.position = (mw/(xsm*4.11),mh/(9*ysm))
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//4*3
        xt = xo*3-xo
        yt = wh-yo
        time.sleep(0.5)
        pag.press('esc')
        time.sleep(0.1)
        keyboard.press('r')
        keyboard.release('r')
        time.sleep(0.1)
        pag.press('enter')
        sleep(8.5)
        for _ in range(4):
            keyboard.press(Key.page_up)
            keyboard.release(Key.page_up)
        time.sleep(0.1)
        for _ in range(6):
            keyboard.press('o')
            time.sleep(0.08)
            keyboard.release('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')
        for _ in range(4):
            #r = imagesearch.find("hive1.png",ths, xo, yo, xt, yt)
            r = getPixelColor(ww//2,wh-2)
            log(r)
            passed = 1
            for i in range(len(r)):
                if tar[i]-var <= r[i] <= tar[i]+var:
                    pass
                else:
                    passed = 0
                    break
                
            if passed:
                time.sleep(0.1)
                if not rhd:
                    for _ in range(4):
                        keyboard.press(',')
                        keyboard.release(',')

                time.sleep(0.1)
                for _ in range(4):
                    keyboard.press(Key.page_down)
                    keyboard.release(Key.page_down)
                return
            for _ in range(4):
                keyboard.press(',')
                keyboard.release(',')
            
            time.sleep(0.5)
        time.sleep(1)
'''

times = []
start = time.time()
for _ in range(5):
    start = time.time()
    move.press(",")
    move.press("e")
    time.sleep(0.8)
    pag.keyDown("w")
    move.press("space")
    move.press("space")
    time.sleep(9)
    pag.keyUp("w")
    move.press("space")
    times.append(time.time()-start)
print(sum(times)/len(times))
'''

'''
# For both Python 2.7 and Python 3.x
from PIL import Image
img_data = b'iVBORw0KGgoAAAANSUhEUgAAAJ8AAAAWAQMAAADkatyzAAAABlBMVEUAAAAbKjWMzP1VAAAAAXRSTlMAQObYZgAAAdlJREFUeAEBzgEx/gD4AAAAAAAAAAAAAAAAAAAAAAAAAAD+BgAAAAAADAAAAAHgDAAAAEAAAAD/BgAAAAB+DAAAAAH+DAAAAEAAAACBhgAAAACCDAAAAAECDAAAAEAAAACBhgAAAAGADAAAAAEDDAAAAEAAAACBhjBAAAGADB8MDAEDDB8MAfAAJgCBBjBB8AEADAGEDAEDDAGP4fD4PAD/BjBCCAEADACECAH+DACMEEEEMAD+BjBCCAEADACGGAHgDACMEEEEIAD/BjBD+AEADB+CEAEADB+MEEH8IACBhjBH/AEADCCCEAEADCCMEEP+IACAhjBGAAGADCCDMAEADCCMEEMAIACAhhBCAAGADCCBIAEADCCMEEEAIACBhhBCAACCDCCB4AEADCCMEEEAIAD/Bg/B8AB+DB+AwAEADB+MEHD4IAD4BgAAAAAADAAAwAEADAAMEAAAIAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAADAAAAAAAAAAAAAFzEPdK0OEUMAAAAAElFTkSuQmCC'
import base64
with open("imageToSave.png", "wb") as fh:
    fh.write(base64.decodebytes(img_data))
c = Image.open("imageToSave.png")
d = c.resize((1000,700), resample=Image.BOX)
d.show()

'''


