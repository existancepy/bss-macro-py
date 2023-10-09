import pyautogui as pag
import time
import os
import tkinter
import imagesearch
from webhook import webhook
import loadsettings
from delay import sleep
from pynput.mouse import Button, Controller
from pynput.keyboard import Key
import pynput.keyboard
from pixelcolour import getPixelColor
from logpy import log

def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]

        
keyboard = pynput.keyboard.Controller()
mouse = Controller()
savedata = {}
mw,mh = pag.size()
tar =  (127, 108, 41)
var = 20
setdat = loadsettings.load()
rhd = setdat["reverse_hive_direction"]
ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
loadSave()
slow_colours = []
mouse.position = (mw/(xsm*4.11),mh/(9*ysm))
ww = savedata["ww"]
wh = savedata["wh"]
xo = ww//4
yo = wh//4*3
xt = xo*3-xo
yt = wh-yo
imgid = 0
time.sleep(0.5)
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
    
def reset():
    pag.press('esc')
    time.sleep(0.1)
    keyboard.press('r')
    keyboard.release('r')
    time.sleep(0.1)
    pag.press('enter')
    sleep(8.5)
def spin(fast):
    global imgid
    out = []
    if fast:
        for _ in range(4):
            keyboard.press(Key.page_up)
            keyboard.release(Key.page_up)
        time.sleep(0.1)
        for _ in range(6):
            keyboard.press('o')
            time.sleep(0.1)
            keyboard.release('o')

        for _ in range(4):
            r = getPixelColor(ww//2,wh-2)
            out.append(r)
            for _ in range(4):
                keyboard.press(',')
                time.sleep(0.05)
                keyboard.release(',')
    else:
        for _ in range(4):
            pag.press("pageup")
        for _ in range(6):
            pag.press("o")
        for _ in range(4):
            r = getPixelColor(ww//2,wh-2)
            out.append(r)
            for _ in range(4):
                pag.press(',')
            print(imgid)
            if imgid == 0 or imgid == 1:
                im = pag.screenshot(region=(ww//2, wh-2, 30, 2))
                im.save("hive - {}.png".format(imgid))
                imgid+=1
    return out
roblox()
print("trying slower reset")
reset()
im = pag.screenshot(region=(ww//2,wh//2,ww//2,wh//2))
im.save("screen.png")
vals = spin(0)
print("Color values: {}".format(vals))
if vals[0] == vals[1] == vals[2]:
    print("Slow reset failed. This can be caused by the following issues:\n1. Camera not rotating properly. This might be due to the lack of accessibility permission for terminal\n2. Screen recording permission for terminal is not enabled")
else:
    print("Slow reset passed")

print("trying normal reset")
reset()
vals = spin(1)
print("Color values: {}".format(vals))
if vals[0] == vals[1] == vals[2]:
    print("Normal reset failed. If slow reset succeeded, this is most likely due to keypresses being too fast for the OS to keep up with")
else:
    print("Success")    
    
terminal()
