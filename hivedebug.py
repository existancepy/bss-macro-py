import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
import cv2
from PIL import ImageGrab
import numpy as np
savedata = {}
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
ww = savedata["ww"]
wh = savedata["wh"]
vals = []
def find(img,confi, x1 = 0, y1 = 0, x2 = ww, y2 = wh):
    method = cv2.TM_CCOEFF_NORMED
    screen = pag.screenshot(region=(x1,y1,x2,y2))
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    small_image = cv2.imread('./images/{}'.format(img))
    large_image = screen
    result = cv2.matchTemplate(small_image, large_image, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    x,y = max_loc
    print("Trying to find {}. max_val is {} ".format(img,max_val))
    vals.append(max_val)
    if max_val >= confi:
        return [1,x,y]
    return

cmd = """
        osascript -e  'activate application "Roblox"'
    """

os.system(cmd)
time.sleep(1)

pag.moveTo(350,100)
xo = ww//4
yo = wh//4*3
xt = xo*2
yt = wh
time.sleep(2)
pag.press('esc')
time.sleep(0.1)
pag.press('r')
time.sleep(0.2)
pag.press('enter')
time.sleep(8)
for _ in range(4):
    pag.press('pgup')
time.sleep(0.1)
for _ in range(6):
    pag.press('o')

r = find("hive1.png",0.8, xo, yo, xt, yt)
for _ in range(4):
    pag.press('.')
r = find("hive1.png",0.8, xo, yo, xt, yt)
print(vals)
if vals[0] > vals[1]:
    time.sleep(1)
    print('hi')
    for _ in range(4):
        pag.press('.')


im = pag.screenshot(region = (ww//2,wh-50,30,10))
im.save('./images/hive1.png')
time.sleep(0.4)
    
    
