
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
def imToString(m):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    # Path of tesseract executable
    #pytesseract.pytesseract.tesseract_cmd ='**Path to tesseract executable**'
    # ImageGrab-To capture the screen image in a loop. 
    # Bbox used to capture a specific area.
    if m == "bee bear":
        cap = pag.screenshot(region=(ww//(3*xsm),wh//(20*ysm),ww//3,wh//7))
        cap.save("bear.png")
        img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, None, fx=2, fy=2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        config = '--oem 3 --psm %d' % 12
        tesstr = pytesseract.image_to_string(img, config = config, lang ='eng')
        return tesstr
    elif m == "egg shop":
        cap = pag.screenshot(region=(ww//(1.2*xsm),wh//(3*ysm),ww-ww//1.2,wh//5))
    elif m == "ebutton":
        cap = pag.screenshot(region=(ww//(2.65*xsm),wh//(20*ysm),ww//21,wh//17))
        img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, None, fx=2, fy=2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        config = '--oem 3 --psm %d' % 10
        tesstr = pytesseract.image_to_string(img, config = config, lang ='eng')
        return tesstr
    elif m == "honey":
        cap = pag.screenshot(region=(ww//(3*xsm),0,ww//6.5,wh//25))
        img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (h, w) = gry.shape[:2]
        gry = cv2.resize(gry, (w * 2, h * 2))
        (T, threshInv) = cv2.threshold(gry, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        tesstr = pytesseract.image_to_string(threshInv, config = "digits")
        tessout = ""
        for i in tesstr:
            if i.isdigit():
                tessout += i
            elif i == "(" or i == "[" or i == "{":
                break
        print(millify(int(tessout)))
        return tessout
    elif m == "disconnect":
        cap = pag.screenshot(region=(ww//3,wh//2.8,ww//2.3,wh//2.5))
        cap.save("disconnect.png")
        img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, None, fx=1.5, fy=1.5)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        config = '--oem 3 --psm %d' % 12
        tesstr = pytesseract.image_to_string(img, config = config, lang ='eng')
        return tesstr
        
    # Converted the image to monochrome for it to be easily 
    # read by the OCR and obtained the output String.
    tesstr = pytesseract.image_to_string(cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY), lang ='eng')
    return tesstr
roblox()
text = imToString("disconnect").lower()
print(text)
if "disconnected" in text:
    print("disconnect checked")

