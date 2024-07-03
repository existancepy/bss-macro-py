from paddleocr import PaddleOCR
import loadsettings
import pyautogui as pag
import numpy as np
from logpy import log
import os
import subprocess
import time
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

ocr = PaddleOCR(lang='en', show_log = False, use_angle_cls=False)

def screenshot(**kwargs):
    out = None
    for _ in range(4):
        try: 
            if "region" in kwargs:
                out = pag.screenshot(region=kwargs['region'])
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
        honeyY = 31
        if setdat['display_type'] == "built-in retina display": honeyY*=2
    if m == "bee bear":
        cap = screenshot(region=(ww//(3*xsm),ebY/1.1,ww//(3*xlm),wh//(15*ylm)))
    elif m == "egg shop":
        cap = screenshot(region=(ww//(1.2*xsm),wh//(3*ysm),ww-ww//1.2,wh//5))
    elif m == "blue":
        cap = screenshot(region=(ww*3//4, wh//3*2, ww//4,wh//3))
    elif m == "chat":
        cap = screenshot(region=(ww*3//4, 0, ww//4,wh//3))
    elif m == "ebutton":
        cap = screenshot(region=(ww//(2.65*xsm),ebY,ww//(21*xlm),wh//(17*ylm)))
        if not cap: return ""
        cap.save("{}.png".format(sn))
        result = ocr.ocr("{}.png".format(sn),cls=False)[0]
        os.remove("{}.png".format(sn))
        try:
            result = sorted(result, key = lambda x: x[1][1], reverse = True)
            return result[0][1][0]
        except:
            return ""
    elif m == "honey":
        xm = 3
        wm = 6.5
        if ww == 2560 and wh == 1600:
            xm = 5.5
            wm = 5
        cap = pag.screenshot(region=(ww//(xm*xsm),honeyY,ww//(wm*xlm),wh//(ylm*25)))
        if not cap: return ""
        cap.save("{}.png".format(sn))  
        ocrres = ocr.ocr("{}.png".format(sn),cls=False)[0]
        honey = 0
        #print(ocrres)
        try:
            result = [x[1][0] for x in ocrres]
            log(result)
            for i in result:
                if i[0].isdigit():
                    honey = i
                    break
            honey = int(''.join([x for x in honey if x.isdigit()]))
        except Exception as e:
            print(e)
            print(honey)
        os.remove("{}.png".format(sn))
        return honey
    elif m == "disconnect":
        cap = screenshot(region=(ww//(3),wh//(2.8),ww//(2.3),wh//(5)))
    elif m == "dialog":
        cap = screenshot(region=(ww//(3*xsm),wh//(1.6*ysm),ww//(8*xlm),wh//(ylm*15)))
    if not cap: return ""
    cap.save("{}.png".format(sn))  
    result = ocr.ocr("{}.png".format(sn),cls=False)[0]
    try:
        result = sorted(result, key = lambda x: x[1][1], reverse = True)
        out = ''.join([x[1][0] for x in result])
    except:
        out = ""
    os.remove("{}.png".format(sn))
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
    cap.save("{}.png".format(sn)) 
    out = ocr.ocr("{}.png".format(sn),cls=False)
    log("OCR for Custom\n{}".format(out))
    os.remove("{}.png".format(sn))
    if not out is None:
        return out[0]
    else:
        return [[[""],["",0]]]
