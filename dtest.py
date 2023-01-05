import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
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
cmd = """
        osascript -e  'activate application "Roblox"'
    """
os.system(cmd)
time.sleep(0.2)
pag.moveTo(350,100)
ww = savedata["ww"]
wh = savedata["wh"]
xo = ww//4
yo = wh//4*3
xt = xo*3
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
for _ in range(4):
    pag.press(".")
im = pag.screenshot(region = (xo,yo,xt,yt))
im.save('hivedebug.png')

time.sleep(0.4)
