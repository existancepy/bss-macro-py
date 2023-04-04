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
import numpy as np
import subprocess

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

def setResolution():
    wwd = int(pag.size()[0])
    whd = int(pag.size()[1])
    info  = str(subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)).lower()
    if "retina" in info or "m1" in info:
        try:
            retout = subprocess.check_output("system_profiler SPDisplaysDataType | grep -i 'retina'",shell=True)
            retout = retout.decode().split("\n")[1].strip().split("x")
            nww = ''.join([x for x in retout[0] if x.isdigit()])
            nwh = ''.join([x for x in retout[1] if x.isdigit()])
        except:
            nww = 0
            nwh = 0
        loadsettings.save('display_type', 'built-in retina display')
        print("display type: retina")
        log("display type: retina")
        wwd *=2
        whd *=2
    else:
        loadsettings.save('display_type',"built-in display")
        print("display type: built-in")
        log("display type: built-in")
        nww = wwd
        nwh = whd
    print("Screen coordinates: {}x{}".format(wwd,whd))
    log("Screen coordinates: {}x{}".format(wwd,whd))
    with open('save.txt', 'w') as f:
        f.write('wh:{}\nww:{}\nnww:{}\nnwh:{}'.format(whd,wwd,nww,nwh))
    ndisplay = "{}x{}".format(wwd,whd)

    multiInfo = {
        #ysm, xsm, ylm,  xlm
        "2880x1800": [1,1,1,1],
        "2940x1912": [1.1,0.98,1,1.2],
        "1920x1080": [1.2,0.92,1.3,1.5],
        "1440x900": [1,1,1,1],
        "4096x2304": [1.45,0.91,1.32,1.5],
        "3024x1964": [1,0.98, 1.2, 1.2],
        "3360x2100": [1.2,0.95,1.2,1.3],
        "4480x2520": [1.4,0.89,1.4,1.9]
        }
    if ndisplay in multiInfo:
        loadsettings.save("y_screenshot_multiplier",multiInfo[ndisplay][0],"multipliers.txt")
        loadsettings.save("x_screenshot_multiplier",multiInfo[ndisplay][1],"multipliers.txt")
        loadsettings.save("y_length_multiplier",multiInfo[ndisplay][2],"multipliers.txt")
        loadsettings.save("x_length_multiplier",multiInfo[ndisplay][3],"multipliers.txt")
    else:
        print("\033[0;31mScreen Coordinates not found in supported list. Contact Existance to get it supported\033[00m")

    print("Retina detected")
