import os
import pyautogui as pag
from paddleocr import PaddleOCR
from ocrpy import imToString
import loadsettings
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
savedata = loadRes()
ww = savedata['ww']
wh = savedata['wh']
ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
ocr = PaddleOCR(lang='en', show_log = False, use_angle_cls=False)
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
cmd = """
        osascript -e  'activate application "Roblox"'
    """

os.system(cmd)
time.sleep(1)

cap = pag.screenshot(region=(ww//(3),wh//(2.8),ww//(2.3),wh//(5)))
cap.save("disconnect-test.png")
result = ocr.ocr("disconnect-test.png",cls=False)[0]
result = sorted(result, key = lambda x: x[1][1], reverse = True)
out = ''.join([x[1][0] for x in result])
print("Test output: \n{}\n\nCurrent output: \n{}".format(out,imToString("disconnect")))
cmd = """
        osascript -e  'activate application "Terminal"'
    """

os.system(cmd)
    
#pag.moveTo(X1,Y1)

