import pyautogui as pag
import loadsettings
import os
import time
import pyscreeze
from webhook import webhook
from pyscreeze import _locateAll_python
pyscreeze.locateAll = _locateAll_python
cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)
time.sleep(2)

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
ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']

while True:
    dayCount = 0
    nightCount = 0
    for _ in range(3):
        im = pyscreeze.screenshot(region=(0,wh/2,ww,wh/2))
        if pyscreeze.locate("./images/general/grassD.png",im, limit=1):
            dayCount += 1
        if pyscreeze.locate("./images/general/grassN.png",im, limit=1):
            nightCount += 1

    result = "night"
    if dayCount > nightCount:
        result = "day"
    webhook("Result",result,"brown",1)
    pag.click()

cmd = """
osascript -e 'activate application "Terminal"' 
"""
os.system(cmd)
