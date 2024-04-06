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
#pg.PAUSE = 0.02
tar = (170, 125, 41)
var = 25
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
def pagPress(key, delay = 0.02):
    pag.keyDown(key, _pause = False)
    time.sleep(delay)
    pag.keyUp(key, _pause = False)
    
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
    for i in range(2):
        webhook("","Resetting character, Attempt: {}".format(i+1),"dark brown")
        mouse.position = (mw/(xsm*4.11)+40,(mh/(9*ysm))+yOffset)
        time.sleep(0.5)
        pagPress('esc')
        time.sleep(0.1)
        pagPress('r')
        time.sleep(0.2)
        pagPress('enter')
        sleep(8.5)
        for _ in range(4):
            pix = getPixelColor(ww//2,wh-2)
            r = [int(x) for x in pix]
            log(r)
            log(abs(r[2]-r[1]))
            log(abs(r[2]-r[0]))
            log(abs(r[1]-r[0]))
            log("real")
            avgDiff = (abs(r[2]-r[1])+abs(r[2]-r[0])+abs(r[1]-r[0]))/3
            log(avgDiff)
            if avgDiff > 10:
                passed = True
                print(r)
                for i in range(len(tar)):
                    if not( tar[i]-var <= r[i] <= tar[i]+var):        
                        passed = False
                        break
                    
                if passed or r[2] == 0:
                    time.sleep(0.1)
                    for _ in range(4):
                        pagPress(".")
                    time.sleep(0.1)
                    for _ in range(6):
                        pagPress("o")
                    time.sleep(0.4)
                    return True
            for _ in range(4):
                pagPress(".")
        time.sleep(0.2)
    return False
    if hiveCheck:
        webhook("Notice","Hive not found.","red",1)
    else:
        webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)

'''
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
    for i in range(2):
        webhook("","Resetting character, Attempt: {}".format(i+1),"dark brown")
        mouse.position = (mw/(xsm*4.11)+40,(mh/(9*ysm))+yOffset)
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
                return True
            for _ in range(4):
                keyboard.press(',')
                time.sleep(0.05)
                keyboard.release(',')
            
            time.sleep(0.5)
        time.sleep(1)
    return False
    if hiveCheck:
        webhook("Notice","Hive not found.","red",1)
    else:
        webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)

'''
