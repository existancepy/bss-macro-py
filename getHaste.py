
import move
import cv2 as cv
from PIL import ImageGrab
import os
import pyautogui as pag
import time
import numpy as np
import threading
import queue
import loadsettings

q = queue.Queue()
method = cv.TM_CCOEFF_NORMED #cv.TM_SQDIFF_NORMED
hasteimgs = []
vals = []
ww = 0
wh = 0
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

REGION = (0,0,0,0)
for i in range(10):
    imgread = cv.imread('./images/general/haste{}.png'.format(i+1))
    hasteimgs.append(imgread)
def fastimgsearch():
    global vals,ww,wh, REGION
    while True:
        i = q.get()
        img = pag.screenshot(region=REGION)
        img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        res = cv.matchTemplate(img_cv, hasteimgs[i], method)
        
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        vals.append((max_val,1+(i*0.1)))
        q.task_done()

def getHaste():
    global vals, ww,wh, REGION
    ws = loadsettings.load()["walkspeed"]
    savedat = loadRes()
    ww = savedat['ww']
    wh = savedat['wh']
    hasteFound = 0
    REGION = (0,wh//30,ww//2,wh//8)
    vals = []
    i = -1
    for _ in range(2):
        threading.Thread(target=fastimgsearch, daemon=True).start()
        for _ in range(5):
            i+=1
            q.put(i)
        q.join()
    vals = sorted(vals,reverse=True)
    haste = vals[0][1]
    with open("haste.txt","w") as f:
        f.write(str(ws*haste))
    f.close()

def getHastelp():
    global vals, ww,wh, REGION
    ws = loadsettings.load()["walkspeed"]
    savedat = loadRes()
    ww = savedat['ww']
    wh = savedat['wh']
    hasteFound = 0
    REGION = (0,wh//30,ww//2,wh//8)
    vals = []
    i = -1
    for x in range(5):
        threading.Thread(target=fastimgsearch, daemon=True).start()
        for y in range(2):
            i += 1
            q.put(i)
        q.join()
    vals = sorted(vals,reverse=True)
    haste = vals[0][1]
    with open("haste.txt","w") as f:
        f.write(str(ws*haste))
    f.close()
    
