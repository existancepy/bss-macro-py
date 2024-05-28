
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
import ast
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
from pixelcolour import getPixelColor
import pygetwindow as gw
from logpy import log
from ocrpy import customOCR, imToString
import backpack
keyboard = Controller()
mouse = pynput.mouse.Controller()
ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
mw,mh = pag.size()
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

def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(1)

def terminal():
    cmd = """
    osascript -e 'activate application "Terminal"' 
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

savedat = loadRes()
ww = savedat['ww']
wh = savedat['wh']
ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']

def getBesideE():
    text = imToString("bee bear").lower()
    log(text)
    return text

def pagPress(key, delay = 0.02):
    pag.keyDown(key, _pause = False)
    time.sleep(delay)
    pag.keyUp(key, _pause = False)
    
def reset(hiveCheck=False):
    setdat = loadsettings.load()
    yOffset = 0
    if setdat["new_ui"]: yOffset = 20
    loadSave()
    rhd = setdat["reverse_hive_direction"]
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ww = savedata["ww"]
    wh = savedata["wh"]
    xo = ww//4
    yo = wh//4*3
    xt = xo*3-xo
    yt = wh-yo
    i = 1
    while True:
        webhook("","Resetting character, Attempt: {}".format(i),"dark brown")
        mouse.position = (mw/(xsm*4.11)+40,(mh/(9*ysm))+yOffset)
        time.sleep(0.5)
        pagPress('esc')
        time.sleep(0.1)
        pagPress('r')
        time.sleep(0.2)
        pagPress('enter')
        time.sleep(8.5)
        besideE = getBesideE()
        if "make" in besideE or "honey" in besideE:
            break
        i += 1
    for _ in range(4):
        pix = getPixelColor(ww//2,wh-2)
        r = [int(x) for x in pix]
        log(r)
        log(abs(r[2]-r[1]))
        log(abs(r[2]-r[0]))
        log(abs(r[1]-r[0]))
        log("real")
        avgDiff = (abs(r[2]-r[1])+abs(r[2]-r[0])+abs(r[1]-r[0]))/3
        log(avgDiff)
        if avgDiff < 10:
            for _ in range(6):
                pagPress("o")
            time.sleep(0.3)
            return True
        for _ in range(4):
            pagPress(".")
    time.sleep(0.3)
    return False
    if hiveCheck:
        webhook("Notice","Hive not found.","red",1)
    else:
        webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)


from difflib import SequenceMatcher
giver = "bucko"
ocr = [[[[[298.0, 41.0], [343.0, 41.0], [343.0, 69.0], [298.0, 69.0]], ('1/6', 0.9993550777435303)], [[[193.0, 110.0], [445.0, 110.0], [445.0, 135.0], [193.0, 135.0]], ('Defeat 2 Werewolves', 0.994888186454773)], [[[297.0, 142.0], [343.0, 142.0], [343.0, 172.0], [297.0, 172.0]], ('1/2', 0.9992332458496094)], [[[180.0, 230.0], [459.0, 232.0], [459.0, 265.0], [180.0, 262.0]], ('Bucko Bee: Tour', 0.9981157779693604)], [[[71.0, 311.0], [570.0, 313.0], [570.0, 333.0], [71.0, 330.0]], ('Collect 205.000.000 Pollen from the Blue', 0.9870282411575317)], [[[80.0, 343.0], [561.0, 341.0], [561.0, 366.0], [80.0, 368.0]], ('Flower Field. 21,982,406/205,000,000', 0.9833346605300903)], [[[44.0, 410.0], [597.0, 411.0], [597.0, 435.0], [44.0, 434.0]], ('Collect 205.000,000 Pollen from the Bamboo', 0.9799546599388123)], [[[132.0, 443.0], [508.0, 443.0], [508.0, 466.0], [132.0, 466.0]], ('Field. 1.523.550/205.000.000', 0.9795450568199158)], [[[38.0, 511.0], [604.0, 511.0], [604.0, 534.0], [38.0, 534.0]], ('Collect 205.000.000 Pollen from the Pine Tree', 0.9388981461524963)], [[[217.0, 544.0], [424.0, 544.0], [424.0, 568.0], [217.0, 568.0]], ('Forest. Complete!', 0.9923646450042725)], [[[181.0, 609.0], [454.0, 609.0], [454.0, 633.0], [181.0, 633.0]], ('Defeat 5 Rhino Beetles', 0.9967955946922302)], [[[295.0, 641.0], [345.0, 641.0], [345.0, 669.0], [295.0, 669.0]], ('4/5', 0.9998016357421875)], [[[213.0, 711.0], [425.0, 711.0], [425.0, 735.0], [213.0, 735.0]], ('Defeat 3 Mantises', 0.9662429690361023)], [[[261.0, 742.0], [382.0, 742.0], [382.0, 771.0], [261.0, 771.0]], ('Complete!', 0.9975935816764832)], [[[95.0, 830.0], [544.0, 833.0], [543.0, 870.0], [95.0, 866.0]], ('Black Bear: Pepper Patrol', 0.981100857257843)], [[[51.0, 908.0], [587.0, 913.0], [586.0, 938.0], [51.0, 933.0]], ('Collect 400.000,000 Pollen from the Pepper', 0.9787130951881409)], [[[122.0, 943.0], [516.0, 943.0], [516.0, 967.0], [122.0, 967.0]], ('Patch. 43,116,694/400,000,000', 0.9797178506851196)], [[[151.0, 1031.0], [488.0, 1034.0], [488.0, 1070.0], [151.0, 1067.0]], ('Riley Bee: Clean-up', 0.9984012246131897)]]]
ocr = ocr[0]
questData = {}
questBear = ""
questTitle = ""
questInfo = []
with open("./dataFiles/quest_data.txt", "r") as f:
    qdata = [x for x in f.read().split("\n") if x]
f.close()
print("a")
for i in qdata:
    if i.startswith("="):
        i = i.replace("=","")
        questBear = i
        questData[questBear] = {}
    elif i.startswith("-"):
        if questTitle:
            questData[questBear][questTitle] = questInfo
        questTitle = i[1:]
        questInfo = []
    elif i.startswith("#"):
        questData[questBear][questTitle] = questInfo
    elif not i.isspace():
        questInfo.append(i)
        
q_title = ""
lines = []  
for j in range(10):
    lines = [x[1][0].lower() for x in ocr]
    #log(lines)
    #search for quest title in only the first 6 lines
    lineCount = min(len(lines),6)
    #check all lines on the last iteration, detect quest at bottom of page
    if j == 9:
        lineCount = len(lines)
    for i in range(lineCount):
        x = lines[i]
        if giver in x and ":" in x:
            q_title_raw = x.split(":")[1]
            q_title = q_title_raw.replace(giver,"").replace("bear","").replace("bee","")
            lines.remove(x)
            break
    if q_title:
        break
    for _ in range(2):
        keyboard.press(Key.page_down)
        time.sleep(0.02)
        keyboard.release(Key.page_down)
print(q_title)

highest_match = [0,"",[]]
for k,v in questData[giver].items():
    match = SequenceMatcher(None, k, q_title).ratio()
    print(k,match)
    if match > highest_match[0]:
        highest_match[0] = match
        highest_match[1] = k
        highest_match[2] = v
print(highest_match)
            
'''
screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
small_image = cv2.imread('./images/general/nightsky.png')
large_image = screen
res = cv2.matchTemplate(small_image, large_image, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
x,y = max_loc
print("Trying to find night sky. max_val is {} ".format(max_val))
MPx,MPy = min_loc

print(MPx,MPy)
pag.moveTo(MPx//2,MPy//2)
# Step 2: Get the size of the template. This is the same size as the match.
trows,tcols = small_image.shape[:2]
# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
# Display the original image with the rectangle around the match.
cv2.imshow('output',large_image)
# The image is only displayed if we call this
cv2.waitKey(0)

if max_val >= 0.5:
    return [1,x,y,max_val]
return
'''

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


