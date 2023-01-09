import pyautogui as pag
import time
import os
import tkinter
import tkinter as tk
from tkinter import ttk
import move
import loadsettings
import reset
import backpack
import sys
import imagesearch
from webhook import webhook
import threading
print("Your python version is {}".format(sys.version_info[0]))
savedata = {}
started = 0
currentfield = ""
def validateSettings():
    msg = ""
    files = os.listdir("./")
    validfield = [x.split("_")[1][:-3] for x in files if x.startswith("field_")]
    print(validfield)
    validgp = ["e_lol","squares"]
    validsize = ["s","m","l"]
    s = loadsettings.load()
    print(s)
    if s['hive_number'] > 6 or s['hive_number'] < 0:
        msg += "\nInvalid hive number, it must be between 1-6 (inclusive)"
    if not s['gather_pattern'].lower() in validgp:
        msg += "\nInvalid gathering pattern, it has to be either {}".format(validgp)
    if not s['gather_size'].lower() in validsize:
        msg += "\nInvalid gather size, it has to be either {}".format(validsize)
    if not isinstance(s['gather_time'], int):
        msg += "\nInvalid gather time"
    if s['pack'] < 0 or s['pack'] > 100:
        msg += "\nInvalid pack, it must be between 1-100 (inclusive)"
    if not s['gather_field'] in validfield:
        msg += ("Invalid gather_field")
    if not s['gather_enable'] == 1 and not s['gather_enable'] == 0:
        msg += ("Invalid gather_enable. Use either 'yes' or 'no'")
    return msg


def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]

def loadtimings():
    tempdict = {}
    with open('timings.txt') as f:
        lines = f.read().split("\n")
    f.close()
    lines = [x for x in lines if x]
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        tempdict[l[0]] = l[1]
    return tempdict

def savetimings(m):
    tempdict = loadtimings()
    print(tempdict)
    tempdict[m] = time.time()
    templist = []
    
    for i in tempdict:
        templist.append("\n{}:{}".format(i,tempdict[i]))
    print(templist)
    with open('timings.txt','w') as f:
        f.writelines(templist)
    f.close()
    
loadSave()
ww = savedata["ww"]
wh = savedata["wh"]
setdat = loadsettings.load()
ms = pag.size()
mw = ms[0]
mh = ms[1]
def canon():
    #Move to canon:
    webhook("","Moving to canon","dark brown")
    move.hold("w",2)
    move.hold("d",0.9*(setdat["hive_number"])+1)
    pag.keyDown("d")
    time.sleep(0.5)
    move.press("space")
    time.sleep(0.2)
    st = time.perf_counter()
    r = ""
    pag.keyUp("d")
    while True:
        pag.keyDown("d")
        time.sleep(0.15)
        pag.keyUp("d")
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            webhook("","Canon found","dark brown")
            return
        if time.perf_counter()  - st > 10/28*setdat["walkspeed"]:
            webhook("","Cannon not found, resetting","dark brown")
            break
        
    reset.reset()   
    canon()
def convert():
    for _ in range(2):
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            webhook("","Starting convert","brown")
            move.press("e")
            st = time.perf_counter()
            while True:
                c = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
            
                if not c:
                    webhook("","Convert done","brown")
                    time.sleep(3)
                    break
                if time.perf_counter()  - st > 600:
                    webhook("","Converting took too long, moving on","brown")
                    break
            
            break
        else:
            time.sleep(0.25)
    return
def walk_to_hive(filename):
    webhook("","Going back to hive","dark brown")
    exec(open("walk_{}.py".format(filename)).read())
    st = time.perf_counter()
    while True:
        pag.keyDown("a")
        time.sleep(0.15)
        pag.keyUp("a")
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            convert()
            break
        if time.perf_counter()  - st > 30/28*setdat["walkspeed"]:
            webhook("","Cant find hive, resetting","dark brown")
            reset.reset()
            break
    reset.reset()
def checkRespawn(m,t):
    timing = loadtimings()[m]
    respt = int(''.join([x for x in list(t) if x.isdigit()]))
    if t[-1] == 'h':
        respt = respt*60*60
    else:
        respt = respt*60
        
    if setdat['gifted_vicious_bee']:
        respt = respt/100*85
    if time.time() - timing > respt:
        return 1
    return 0

def savesettings(dictionary):
    global currentfield
    if not currentfield: return
    templist = []
    
    for i in dictionary:
        templist.append("\n{}:{}".format(i,dictionary[i]))
    with open('settings.txt', "w") as f:
        f.writelines(templist)
    f.close()
def moblootPattern(f,s,r,t):
    if r == "l":
        for _ in range(t):
            move.press(",")
    elif r == "r":
        for _ in range(t):
            move.press(",")
    for i in range(2):
        move.hold("w", 0.72*f)
        move.hold("a", 0.1*s)
        move.hold("s", 0.72*f)
        move.hold("a", 0.1*s)
    for i in range(2):
        move.hold("w", 0.72*f)
        move.hold("d", 0.1*s)
        move.hold("s", 0.72*f)
        move.hold("d", 0.1*s)
    
    
def killMob(field,mob):
    global currentfield
    currentfield = field.replace(" ","").lower()
    webhook("","Traveling: {} ({})".format(mob.title(),field.title()),"dark brown")
    convert()
    canon()
    exec(open("field_{}.py".format(field)).read())
    xo = ww//2
    yo = wh//2
    while True:
        if pag.locateOnScreen("./images/{}.png".format(mob.replace(" ","").lower()),confidence = 0.8, region = (xo,yo,xo,yo)): break
    webhook("","Looting: {} ({})".format(mob,field),"dark brown")
    
    moblootPattern(1.5,1.5,"none",2)
    
    
    
'''
root = tkinter.Tk()
root.withdraw()
ww,wh = root.winfo_screenwidth(), root.winfo_screenheight()
print("{},{}".format(ww,wh))
root.destroy()

updateSave("ww",ww)
updateSave("wh",wh)
'''
cmd = """
        osascript -e 'activate application "Roblox"' 
        """
os.system(cmd)
bpc = 0
def background():
    global bpc
    global currentfield
    while True:
        bpc = backpack.bpc()
        
def startLoop():
    global bpc
    global currentfield
    while True:
        
        webhook("Gathering: no canon","Limit: 30.00 - no canon - Backpack: 95%","light green")
        move.apkey("space")
        time.sleep(0.2)
        timestart = time.perf_counter()

        while True:
            currentfield = "pinetree"
            pag.mouseDown()
            exec(open("gather_e_lol.py").read())
            pag.mouseUp()
            timespent = (time.perf_counter() - timestart)/60
            if bpc > 95:
                webhook("Gathering: ended","Time: {:.2f} - Backpack - Return: no canon".format(timespent, ),"light green")
                break
            if timespent > 30:
                webhook("Gathering: ended","Time: {:.2f} - Time Limit - Return: no canon".format(timespent),"light green")
                break
        currentfield = ""
        for _ in range(2):
            move.press(".")
        walk_to_hive(currentfield)
        break


mainloop = threading.Thread(target=startLoop, args=())
background = threading.Thread(target=background, args=())
mainloop.start()
background.start()       




