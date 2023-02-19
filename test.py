
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

roblox()
savedata = loadRes()
ww = savedata['ww']
wh = savedata['wh']
im = pag.screenshot(region=(ww//3,0,ww//3,wh//3))
im.save('test.png')


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


