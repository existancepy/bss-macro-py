import cv2
import mss
import mss.tools
import pyautogui as pag
import os
from webhook import webhook
import loadsettings
import time
import pynput
from logpy import log
from pixelcolour import getPixelColor
import move
from PIL import Image
import numpy as np

try:
    import ocrmac #see if ocr mac is installed
    from macocrpy import imToString,customOCR
    print("Imported macocr")
except:
    from ocrpy import imToString,customOCR
    print("Imported paddleocr")
    
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
redcannon = cv2.imread('./images/general/e2.png')

def pagPress(key, delay = 0.02):
    pag.keyDown(key, _pause = False)
    time.sleep(delay)
    pag.keyUp(key, _pause = False)
    
def loadRes():
    while True:
        try:
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
        except Exception as e:
            log(f"loadRes failed: {e}")
            
savedata = loadRes()     
def loadSave():
    global savedata
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
        
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
    for i in range(5):
        webhook("","Resetting character, Attempt: {}".format(i+1),"dark brown")
        mouse.position = (mw/(xsm*4.11)+40,(mh/(9*ysm))+yOffset)
        time.sleep(0.5)
        pagPress('esc')
        time.sleep(0.1)
        pagPress('r')
        time.sleep(0.2)
        pagPress('enter')
        time.sleep(8.5)
        besideE = getBesideE()
        if "make" in besideE or "honey" in besideE or "flower" in besideE or "field" in besideE:
            break
    else:
        webhook("Notice","Unable to detect that player has respawned at hive, continuing","red",1)
        return False

    for _ in range(4):
        pix = getPixelColor((ww//2)+15,wh-2)
        r = [int(x) for x in pix]
        log(r)
        log(abs(r[2]-r[1]))
        log(abs(r[2]-r[0]))
        log(abs(r[1]-r[0]))
        log("real")
        avgDiff = (abs(r[2]-r[1])+abs(r[2]-r[0])+abs(r[1]-r[0]))/3
        log(avgDiff)
        if avgDiff < 20:
            for _ in range(8):
                pagPress("o")
            time.sleep(0.8)
            return True
        
        for _ in range(4):
            pagPress(".")
            time.sleep(0.1)
    time.sleep(0.3)
    if hiveCheck:
        webhook("Notice","Hive not found.","red",1)
    else:
        webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)
    return False
    
def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(3)

def terminal():
    cmd = """
    osascript -e 'activate application "Terminal"' 
    """
    os.system(cmd)
    
def mssScreenshot(x,y,w,h,saveImg = False):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": x, "top": y, "width": w, "height": h}
        # Grab the data and convert to pillow img
        sct_img = sct.grab(monitor)
        #save it as a img
        if saveImg:
            mss.tools.to_png(sct_img.rgb, sct_img.size, output="redcannon.png")
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img
    
def ebutton(pagmode=0):
    img = mssScreenshot(mw//2-200,20,400,125)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(img_cv, redcannon, cv2.TM_CCOEFF_NORMED)
    print(cv2.minMaxLoc(res))
    return (res >= 0.9).any()

def getBesideE():
    text = imToString("bee bear").lower()
    log(text)
    return text

def canon(fast=0):
    savedata = loadRes()
    setdat = loadsettings.load()
    ww = savedata['ww']
    wh = savedata['wh']
    disconnect = False
    eb_freeze = False
    for i in range(3):
        #Move to canon:
        if not fast:
            webhook("","Moving to cannon","dark brown")
        time.sleep(1)
        move.hold("w",0.8)
        move.hold("d",0.9*4)
        pag.keyDown("d")
        time.sleep(0.5)
        move.press("space")
        time.sleep(0.2)
        r = ""
        pag.keyUp("d")
        move.hold("w",0.2)
        
        if fast:
            move.hold("d",0.95)
            time.sleep(0.1)
            return
        move.hold("d",0.35)
        move.hold("s",0.1)
        for _ in range(2):
            move.hold("d",0.15)
            time.sleep(0.05)
        time.sleep(1)
        img = mssScreenshot(mw//2-200,0,400,125,True)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(img_cv, redcannon, cv2.TM_CCOEFF_NORMED)
        print(cv2.minMaxLoc(res))
        return
            
        webhook("","Could not find cannon","dark brown",1)
        mouse.position = (mw//2,mh//5*4)
        reset()
    else:
        webhook("","Cannon failed too many times, rejoining", "red")
        disconnect = True
        
    if disconnect:
        setStatus("disconnect")
        time.sleep(1)
        return "dc"
mw, mh = pag.size()
roblox()
reset()
canon()
terminal()

