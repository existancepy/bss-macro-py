import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
import cv2
import imagesearch
from PIL import ImageGrab
import numpy as np
savedata = {}
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
loadSave()
ww = savedata["ww"]
wh = savedata["wh"]

cmd = """
        osascript -e  'activate application "Roblox"'
    """

os.system(cmd)
time.sleep(1)

if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
    print("eb works")
else:
    r = imagesearch.find("eb.png",0,0,0,ww,wh//2)
    print(r[3])
im = pag.screenshot(region = (0,0,ww,wh//2))
im.save('ebuttondebug.png')
time.sleep(0.4)
    
    
