import loadsettings
import pyautogui as pag
import numpy as np
from logpy import log
from PIL import Image
import os
import subprocess
import time
import mss

useOCRMac = False
useLangPref = True
try:
    from ocrmac import ocrmac #see if ocr mac is installed
    useOCRMac = True
    print("Imported macocr")
except:
    from paddleocr import PaddleOCR
    ocrP = PaddleOCR(lang='en', show_log = False, use_angle_cls=False)
    print("Imported paddleocr")
 
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

mw, mh = pag.size()
def mssScreenshot(x,y,w,h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": x, "top": y, "width": w, "height": h}
        # Grab the data and convert to pillow img
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img

def paddleBounding(b):
    #convert all values to int and unpack
    x1,y1,x2,y2 = [int(x) for x in b]
    return ([x1,y1],[x2,y1],[x2,y2],[x1,y2])
    
def ocrMac_(img):
    if useLangPref:
        result = ocrmac.OCR(img,language_preference=['en-US']).recognize(px=True)
    else:
        result = ocrmac.OCR(img).recognize(px=True)
    #convert it to the same format as paddleocr
    return [ [paddleBounding(x[2]),(x[0],x[1]) ] for x in result]

def ocrPaddle(img):
    sn = time.time()
    img.save("{}.png".format(sn))  
    result = ocrP.ocr("{}.png".format(sn),cls=False)[0]
    os.remove("{}.png".format(sn))
    return result

def screenshot(**kwargs):
    out = None
    for _ in range(4):
        try: 
            if "region" in kwargs:
                out = pag.screenshot(region=[int(x) for x in kwargs['region']])
            else:
                out = pag.screenshot()
            break
        except FileNotFoundError as e:
            log(e)
            print(e)
            time.sleep(0.5)
    return out

def imToString(m):
    setdat = loadsettings.load()
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    sn = time.time()
    ebY = wh//(20*ysm)
    honeyY = 0
    if setdat["new_ui"]:
        ebY = wh//(14*ysm)
        honeyY = 25
    if m == "bee bear":
        cap = screenshot(region=(ww//(3*xsm),ebY/1.1,ww//(3*xlm),wh//(15*ylm)))
    elif m == "egg shop":
        cap = screenshot(region=(ww//(1.2*xsm),wh//(3*ysm),ww-ww//1.2,wh//5))
    elif m == "blue":
        cap = screenshot(region=(ww*3//4, wh//3*2, ww//4,wh//3))
    elif m == "chat":
        cap = screenshot(region=(ww*3//4, 0, ww//4,wh//3))
    elif m == "ebutton":
        #cap = screenshot(region=(ww//(2.65*xsm),ebY,ww//(21*xlm),wh//(17*ylm)))
        cap = mssScreenshot(mw//2-200,20,400,125)
        result = ocrFunc(cap)
        try:
            result = sorted(result, key = lambda x: x[1][1], reverse = True)
            return result[0][1][0]
        except:
            return ""
    elif m == "honey":
        cap = mssScreenshot(mw//2-241, honeyY, 140, 36)
        if not cap: return ""
        ocrres = ocrFunc(cap)
        honey = ""
        try:
            result = ''.join([x[1][0] for x in ocrres])
            log(result)
            for i in result:
                if i == "(" or i == "+":
                    break
                elif i.isdigit():
                    honey += i
            honey = int(honey)
        except Exception as e:
            print(e)
            print(honey)
        return honey
    elif m == "disconnect":
        cap = screenshot(region=(ww//(3),wh//(2.8),ww//(2.3),wh//(5)))
    elif m == "dialog":
        cap = screenshot(region=(ww//(3*xsm),wh//(1.6*ysm),ww//(8*xlm),wh//(ylm*15)))
    if not cap: return ""
    result = ocrFunc(cap)
    try:
        result = sorted(result, key = lambda x: x[1][1], reverse = True)
        out = ''.join([x[1][0] for x in result])
    except:
        out = ""
    log("OCR for {}\n\n{}".format(m,out))
    return out

def customOCR(X1,Y1,W1,H1,applym=1):
    sn = time.time()
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    if applym:
        cap = screenshot(region=(X1/xsm,Y1/ysm,W1/xlm,H1/ylm))
    else:
        cap = screenshot(region=(X1,Y1,W1,H1))
    out = ocrFunc(cap)
    log("OCR for Custom\n{}".format(out))
    if not out is None:
        return out
    else:
        return [[[""],["",0]]]

#accept pillow img
def ocrRead(img):
    return ocr(img)
    
if useOCRMac:
    ocrFunc = ocrMac_
    try:
        ocrFunc(mssScreenshot(1,1,10,10))
    except:
        print("Language Preferences for ocrmac is disabled")
        useLangPref = False
else:
    ocrFunc = ocrPaddle
