
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
from pixelcolour import getPixelColor
import pygetwindow as gw
from logpy import log
#from paddleocr import PaddleOCR,draw_ocr
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

def millify(n):
    if not n: return 0
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))



def hourlyReport(hourly=1):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    try:
        with open('honey_history.txt','r') as f:
            honeyHist = ast.literal_eval(f.read())
        f.close()
        
        setdat = loadsettings.load()
        log(honeyHist)
        if hourly == 0:
            setdat['prev_honey'] = honeyHist[-1]
        digitCounts = []
        for i, e in enumerate(honeyHist[:]):
            if len(str(e)) <= 4:
                honeyHist.pop(i)
        if honeyHist.count(honeyHist[0]) != len(honeyHist):
            for i, e in reversed(list(enumerate(honeyHist[:]))):
                if e != setdat['prev_honey']:
                    break
                else:
                    honeyHist.pop(i)
        log('prev honey: {}'.format(setdat['prev_honey']))
        log(honeyHist)
        
        while True:
            compList = [x for x in honeyHist if x]
            sortedHoney = sorted(compList)
            if sortedHoney == compList:
                break
            else:
                removeELE = sortedHoney[-1]
                honeyHist.remove(removeELE)
        log(honeyHist)
        currHoney = honeyHist[-1]
        session_honey = currHoney - setdat['start_honey']
        hourly_honey = currHoney - setdat['prev_honey']
        if hourly:
            loadsettings.save('prev_honey',currHoney)
            timehour = int(datetime.now().hour) - 1
        else:
            timehour = int(datetime.now().hour)
            
        stime = time.time() - setdat['start_time']
        day = stime // (24 * 3600)
        stime = stime % (24 * 3600)
        hour = stime // 3600
        stime %= 3600
        minutes = stime // 60
        stime %= 60
        seconds = round(stime)
        session_time = "{}d {}h {}m".format(round(day),round(hour),round(minutes))
        yvals = []
        for i in range(len(honeyHist)):
            if i != 0:
                hf, hb = honeyHist[i], honeyHist[i-1]
                yvals.append(int(hf) - int(hb))
        #yvals = [1,2,3,4,5,6,7,8]
        xvals = [x+1 for x in range(len(yvals))]


        fig = plt.figure(figsize=(12,12), dpi=300,constrained_layout=True)
        gs = fig.add_gridspec(12,12)
        fig.patch.set_facecolor('#121212')

        axText = fig.add_subplot(gs[0:12, 8:12])
        axText.get_xaxis().set_visible(False)
        axText.get_yaxis().set_visible(False)
        axText.patch.set_facecolor('#121212')
        axText.spines['bottom'].set_color('#121212')
        axText.spines['top'].set_color('#121212')
        axText.spines['left'].set_color('#121212')
        axText.spines['right'].set_color('#121212')

        plt.text(0.3,1,"Report", fontsize=20,color="white")
        plt.text(0,0.95,"Session Time: {}".format(session_time), fontsize=15,color="white")
        plt.text(0,0.9,"Current Honey: {}".format(millify(currHoney)), fontsize=15,color="white")
        plt.text(0,0.85,"Session Honey: {}".format(millify(session_honey)), fontsize=15,color="white")
        plt.text(0,0.8,"Honey/Hr: {}".format(millify(hourly_honey)), fontsize=15,color="white")

        ax1 = fig.add_subplot(gs[0:3, 0:7])
        if not yvals:
            yvals = honeyHist.copy()
        if max(yvals) == 0:
            yticks = [0]
        else:
            yticks = np.arange(0, max(yvals)+1, max(yvals)/4)
        yticksDisplay = [millify(x) if x else x for x in yticks]

        xticks = np.arange(0,max(xvals)+1, 10)
        xticksDisplay = ["{}:{}".format(timehour,x) if x else "{}:00".format(timehour) for x in xticks]

        ax1.set_yticks(yticks,yticksDisplay,fontsize=16)
        ax1.set_xticks(xticks,xticksDisplay,fontsize=16)
        ax1.set_title('Honey/min',color='white',fontsize=19)
        ax1.patch.set_facecolor('#121212')
        ax1.spines['bottom'].set_color('white')
        ax1.spines['top'].set_color('white')
        ax1.spines['left'].set_color('white')
        ax1.spines['right'].set_color('white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.plot(xvals, yvals,color="#BB86FC")
        
        
        buffim = pag.screenshot(region = (0,wh/(30*ysm),ww/2,wh/(16*ylm)))
        buffim.save("buffs.png")
        buffim = plt.imread('buffs.png')
        ax2 = fig.add_subplot(gs[4:6, 0:7])
        ax2.set_title('Buffs',color='white',fontsize=19)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        ax2.patch.set_facecolor('#121212')
        ax2.imshow(buffim)
        
        plt.grid(alpha=0.08)
        plt.savefig("hourlyReport-resized.png", bbox_inches='tight')    
        #c = Image.open("hourlyReport.png")
        #d = c.resize((1452,1452),resample = Image.NEAREST)
        #d.save("hourlyReport-resized.png")
        webhook("**Hourly Report**","","light blue",0,1)
    except Exception as e:
        log(e)
        print(e)
        webhook("","Hourly Report has an error that has been caught. The error can be found in macroLogs.log","red")
hourlyReport(0)
                    
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


