
import pyautogui as pag
import time
import os
import tkinter
import move
import sys
import cv2
from PIL import ImageGrab
from delay import sleep
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
    sleep(3)
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
    print("Screen Coordinates: {}x{}".format(ww,wh))
    # Path of tesseract executable
    #pytesseract.pytesseract.tesseract_cmd ='**Path to tesseract executable**'
    # ImageGrab-To capture the screen image in a loop. 
    # Bbox used to capture a specific area.
    if m == "bee bear":
        cap = pag.screenshot(region=(ww//3,wh//20,ww//3,wh//7))
    elif m == "egg shop":
        cap = pag.screenshot(region=(ww//1.2,wh//3,ww-ww//1.2,wh//5))
    elif m == "ebutton":
        cap = pag.screenshot(region=(ww//2.65,wh//20,ww//21,wh//17))
        img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, None, fx=2, fy=2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        config = '--oem 3 --psm %d' % 10
        tesstr = pytesseract.image_to_string(img, config = config, lang ='eng')
        print(tesstr)
        return tesstr

    # Converted the image to monochrome for it to be easily 
    # read by the OCR and obtained the output String.
    tesstr = pytesseract.image_to_string(cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY), lang ='eng')
    return tesstr
mx = float(input("input x screenshot multiplier: "))
my = float(input("input y screenshot multiplier: "))
lx = float(input("input x length multiplier: "))
ly = float(input("input y length multiplier: "))
roblox()
ima = pag.screenshot(region=(0,0,ww,wh))
ima.save('screentest.png')
im = pag.screenshot(region=(ww//(2.65*mx),wh//(20*my),ww//(21*lx),wh//(17*ly)))
im.save('test.png')
loadsettings.save("y_screenshot_multiplier",my,"multipliers.txt")
loadsettings.save("x_screenshot_multiplier",mx,"multipliers.txt")
loadsettings.save("y_length_multiplier",ly,"multipliers.txt")
loadsettings.save("x_length_multiplier",lx,"multipliers.txt")
cmd = """
    osascript -e 'activate application "Terminal"' 
    """
os.system(cmd)

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


