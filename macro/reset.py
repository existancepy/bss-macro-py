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
keyboard = pynput.keyboard.Controller()
mouse = Controller()
savedata = {}
mw,mh = pag.size()
tar =  (127, 108, 41)
var = 40
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]

def reset():
    setdat = loadsettings.load()
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
    for i in range(2):
        webhook("","Resetting character, Attempt: {}".format(i+1),"dark brown")
        mouse.position = (mw/(xsm*4.11)+40,mh/(9*ysm))
        time.sleep(0.5)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        sleep(8.5)
        for _ in range(4):
            keyboard.press(Key.page_up)
            keyboard.release(Key.page_up)
        time.sleep(0.1)
        for _ in range(6):
            keyboard.press('o')
            time.sleep(0.1)
            keyboard.release('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')
        for _ in range(4):
            #r = imagesearch.find("hive1.png",ths, xo, yo, xt, yt)
            r = getPixelColor(ww//2,wh-2)
            log(r)
            passed = 1
            for i in range(len(tar)):
                if tar[i]-var <= r[i] <= tar[i]+var:
                    pass
                elif i == 2 and r[2] < 15:
                    pass
                else:           
                    passed = 0
                    break
                
            if passed:
                time.sleep(0.1)
                if not rhd:
                    for _ in range(4):
                        keyboard.press(',')
                        time.sleep(0.05)
                        keyboard.release(',')

                time.sleep(0.1)
                for _ in range(4):
                    keyboard.press(Key.page_down)
                    keyboard.release(Key.page_down)
                return
            for _ in range(4):
                keyboard.press(',')
                time.sleep(0.05)
                keyboard.release(',')
            
            time.sleep(0.5)
        time.sleep(1)
    return False
    webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)

def resetCheck():
    
    loadSave()
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    for _ in range(2):
        webhook("","Resetting character","dark brown")
        pag.moveTo(mw/(4.11*xsm),mh/(9*ysm))
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//100*90
        xt = xo*2
        yt = wh//100*20
        time.sleep(2)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        sleep(8.5)
        for _ in range(4):
            pag.press('pgup')
        time.sleep(0.1)
        for _ in range(6):
            pag.press('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')

        time.sleep(0.4)
        for _ in range(4):
            r = getPixelColor(ww//2,wh-2)
            passed = 1
            for i in range(len(tar)):
                if tar[i]-var <= r[i] <= tar[i]+var:
                    pass
                elif i == 2 and r[2] < 15:
                    pass
                else:           
                    passed = 0
                    break
                
                
            if passed:
                time.sleep(0.1)
                for _ in range(4):
                    pag.press(".")

                time.sleep(0.1)
                for _ in range(4):
                    pag.press('pgdn')
                return True
            for _ in range(4):
                pag.press(",")
            
            time.sleep(0.5)
        time.sleep(1)
    for _ in range(4):
        pag.press(",")
    webhook("Notice","Hive not found.","red",1)
    return False


