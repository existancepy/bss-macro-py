
import pyautogui as pag
import time
import os
import tkinter
import move
import sys
import cv2
from PIL import ImageGrab, Image
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
from datetime import datetime
import matplotlib.pyplot as plt
import random
from matplotlib.colors import from_levels_and_colors
from matplotlib.collections import LineCollection
import math
from pynput.keyboard import Key, Controller
import pynput
from pynput.mouse import Button
import Quartz.CoreGraphics as CG
import struct
import reset
from ocrpy import customOCR
keyboard = Controller()
mouse = pynput.mouse.Controller()
#import easyocr
def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(1)
def loadRes():
    outdict =  {}
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        outdict[l[0]] = l[1]
    return outdict


savedata = loadRes()
ww = savedata['ww']
wh = savedata['wh']


def openSettings():
    savedat = loadRes()
    mw, mh = pag.size()
    ww = savedat['ww']
    wh = savedat['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    
    promoCode = ''.join([x[1] for x in customOCR(0,wh/7,ww/3,wh/8)]).lower()
    if not "code" in promoCode:
        mouse.position = (mw/5.5*xsm, mh/8.4*ysm)
        mouse.click(Button.left, 1)
        promoCode = ''.join([x[1] for x in customOCR(0,wh/7,ww/3,wh/8)]).lower()
        if not "code" in promoCode:
            mouse.click(Button.left, 1)
    mouse.position = (mw/5, mh/3)
    time.sleep(1)
    for _ in range(5):
        pag.scroll(-10000)
    time.sleep(0.5)
    for _ in range(2):
        pag.scroll(200)
    pag.scroll(100)
    for _ in range(10):
        statData = customOCR(0,wh/7,ww/7,wh/2)
        statNames = ''.join([x[1] for x in statData]).lower()
        if 'speed'in statNames:
            break
        pag.scroll(200)
    else:
        return
    time.sleep(1)
    check = customOCR(0,0,ww/7,wh)
    for i, e in enumerate(check):
        if 'speed' in e[1]:
            movespeedInfo = e
    print(movespeedInfo)
    coords = movespeedInfo[0]
    start,_,end,_ = coords
    x,y, = start[0],start[1]-20
    h = end[1] - y+40
    
    im = pag.screenshot(region=(ww/8,y,ww/10,h))
    im.save('test.png')
    loadsettings.save("msh",h,"multipliers.txt")
    loadsettings.save("msy",y,"multipliers.txt")

def getHaste():
    msh = loadsettings.load('multipliers.txt')['msh']
    msy = loadsettings.load('multipliers.txt')['msy']
    text = customOCR(ww/8,msy,ww/10,msh)
    print(text)
    
roblox()
#im = pag.screenshot(region=(0,wh/7,ww/7,wh/1.3))
#im.save('test.png')
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


