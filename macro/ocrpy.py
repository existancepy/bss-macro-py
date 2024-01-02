from paddleocr import PaddleOCR
import loadsettings
import pyautogui as pag
import numpy as np
from logpy import log
import os
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

def millify(n):
    if not n: return 0
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

def imToString(m):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    sn = time.time()
    # Path of tesseract executable
    #pytesseract.pytesseract.tesseract_cmd ='**Path to tesseract executable**'
    # ImageGrab-To capture the screen image in a loop. 
    # Bbox used to capture a specific area.
    if m == "bee bear":
        cap = pag.screenshot(region=(ww//(3*xsm),wh//(20*ysm),ww//(3*xlm),wh//(7*ylm)))
    elif m == "egg shop":
        cap = pag.screenshot(region=(ww//(1.2*xsm),wh//(3*ysm),ww-ww//1.2,wh//5))
    elif m == "blue":
        cap = pag.screenshot(region=(ww*3//4, wh//3*2, ww//4,wh//3))
    elif m == "chat":
        cap = pag.screenshot(region=(ww*3//4, 0, ww//4,wh//3))
    elif m == "ebutton":
        cap = pag.screenshot(region=(ww//(2.65*xsm),wh//(20*ysm),ww//(21*xlm),wh//(17*ylm)))
        cap.save("{}.png".format(sn))
        result = ocr.ocr("{}.png".format(sn),cls=False)[0]
        os.remove("{}.png".format(sn))
        try:
            result = sorted(result, key = lambda x: x[1][1], reverse = True)
            return result[0][1][0]
        except:
            return ""
    elif m == "honey":
        cap = pag.screenshot(region=(ww//(3*xsm),0,ww//(6.5*xlm),wh//(ylm*25)))
        cap.save("{}.png".format(sn))  
        ocrres = ocr.ocr("{}.png".format(sn),cls=False)[0]
        #print(ocrres)
        result = [x[1][0] for x in ocrres]
        honey = 0
        for i in result:
            if i[0].isdigit():
                honey = i
                break
        try:
            honey = int(''.join([x for x in honey if x.isdigit()]))
            log(millify(honey))
        except Exception as e:
            print(honey)
        os.remove("{}.png".format(sn))
        return honey
    elif m == "disconnect":
        cap = pag.screenshot(region=(ww//(3),wh//(2.8),ww//(2.3),wh//(5)))
    elif m == "dialog":
        cap = pag.screenshot(region=(ww//(3*xsm),wh//(1.6*ysm),ww//(8*xlm),wh//(ylm*15)))
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
        cap = pag.screenshot(region=(X1/xsm,Y1/ysm,W1/xlm,H1/ylm))
    else:
        cap = pag.screenshot(region=(X1,Y1,W1,H1))
    cap.save("{}.png".format(sn)) 
    out = ocr.ocr("{}.png".format(sn),cls=False)
    log("OCR for Custom\n{}".format(out))
    os.remove("{}.png".format(sn))
    return out[0]
