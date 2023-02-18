try:
    import pyautogui as pag
except Exception as e:
    print(e)
    print("There is an import error here! This is most likely caused by an incorrect installation process. Ensure that you have done the 'pip3 install...' steps")
    quit()
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
import webbrowser
import multiprocessing
from webhook import webhook
import ctypes
import tty
global savedata
global setdat
import discord
import update
import updateexperiment
from tkinter import messagebox
import numpy as np
from PIL import ImageGrab
import subprocess
try:
    import cv2
except Exception as e:
    print(e)
    print("There is a import error here! Check out ImportError: dlopen in #common-fixes in the discord server or 'bugs and fixes' section in the github")
    quit()
import sv_ttk
import math
import ast
import calibrate_hive
import _darwinmouse as mouse
from datetime import datetime
from getHaste import getHaste, getHastelp


savedata = {}
ww = ""
wh = ""
ms = pag.size()
mw = ms[0]
mh = ms[1]
stop = 1
setdat = loadsettings.load()
macrov = "1.30"
planterInfo = loadsettings.planterInfo()

if __name__ == '__main__':
    planterTypes_prev = []
    planterFields_prev = []
    if not os.stat("planterdata.txt").st_size == 0:
        with open("planterdata.txt","r") as f:
            lines = f.read().split("\n")
        f.close()
        occupiedStuff = ast.literal_eval(lines[0])
        planterTypes_prev = ast.literal_eval(lines[1])
        planterFields_prev = ast.literal_eval(lines[2])
    manager = multiprocessing.Manager()
    currentfield = manager.Value(ctypes.c_wchar_p, "")
    bpc = multiprocessing.Value('i', 0)
    gather = multiprocessing.Value('i', 0)
    disconnected = multiprocessing.Value('i', 0)

def boolToInt(condition):
    if condition: return 1
    return 0
def is_running(app):
    tmp = os.popen("ps -Af").read()
    return app in tmp[:]

def discord_bot(dc):
    setdat = loadsettings.load()
    if setdat['enable_discord_bot']:
        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f'We have logged in as {client.user}')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            if message.content.startswith('!b'):
                args = message.content.split(" ")[1:]
                cmd = args[0].lower()
                if cmd == "rejoin":
                    await message.channel.send("Now attempting to rejoin")
                    dc.value = 1
                    rejoin()
                    dc.value = 0
                elif cmd == "screenshot":
                    await message.channel.send("Sending a screenshot via webhook")
                    webhook("User Requested: Screenshot","","light blue",1)
                    

        client.run(setdat['discord_bot_token'])
    
def validateSettings():
    msg = ""
    files = os.listdir("./")
    validfield = [x.split("_")[1][:-3] for x in files if x.startswith("field_")]
    validgp = [x.split("_",1)[1][:-3] for x in files if x.startswith("gather_")]
    validsize = ["s","m","l"]
    s = loadsettings.load()
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
    #if not s['gather_field'] in validfield:
        #msg += ("Invalid gather_field")
    if not s['gather_enable'] == 1 and not s['gather_enable'] == 0:
        msg += ("Invalid gather_enable. Use either 'yes' or 'no'")
    return msg

def loadSave():
    global savedata
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
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
    tempdict[m] = time.time()
    templist = []
    
    for i in tempdict:
        templist.append("\n{}:{}".format(i,tempdict[i]))
    with open('timings.txt','w') as f:
        f.writelines(templist)
    f.close()

def savePlanterTimings(p):
    
    with open('plantertimings.txt','r') as f:
        lines = f.read().split('\n')
    f.close()
    tempdict = {}
    for l in lines:
        if ":" in l:
            a,b = l.split(":")
            tempdict[a] = b
    tempdict[p] = time.time()
    templist = []
    
    for i in tempdict:
        templist.append("\n{}:{}".format(i,tempdict[i]))
    with open('plantertimings.txt','w') as f:
        f.writelines(templist)
    f.close()
    
def ebutton(pagmode=0):
    r =  []
    savedata = loadRes()
    c = loadsettings.load()['ebthreshold']
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    if setdat['ebdetect'] == "pyautogui" or pagmode:
        if setdat['display_type'] == "built-in retina display":
            r = pag.locateOnScreen("./images/retina/eb.png",confidence = 0.99,region=(0,0,ww,wh//2))
        else:
            r = pag.locateOnScreen("./images/built-in/eb.png",confidence = 0.99,region=(0,0,ww,wh//2))
    else:
        print("ebutton threshold: {}".format(c))
        r = imagesearch.find("eb.png",c,0,0,ww,wh//2)
    if r:return r
    return



def canon():
    savedata = loadRes()
    setdat = loadsettings.load()
    ww = savedata['ww']
    wh = savedata['wh']
    #Move to canon:
    webhook("","Moving to canon","dark brown")
    move.hold("w",1.5)
    move.hold("d",0.9*(setdat["hive_number"])+1)
    pag.keyDown("d")
    time.sleep(0.5)
    move.press("space")
    time.sleep(0.2)
    r = ""
    pag.keyUp("d")
    for _ in range(6):
        move.hold("d",0.15)
        r = ebutton()
        if r:
            webhook("","Canon found","dark brown")
            return
    webhook("","Cannon not found, resetting","dark brown",1)
    mouse.move_to(mw//2,mh//5*4)
    for _ in range(20):
        mouse.press()
        sleep(0.25)
        mouse.release()
    reset.reset()   
    canon()

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()
def acchold(key,duration):
    ws = loadsettings.load()["walkspeed"]
    pag.keyDown(key)
    sleep(duration*ws/28)
    pag.keyUp(key)

def mondo_buff():
    webhook("","Travelling: Mondo Buff","dark brown")
    time.sleep(2)
    move.hold("e",0)
    move.hold("space",0)
    move.hold("space",0)
    move.hold("s",0.8)
    sleep(0.82)
    move.hold("space",0)
    sleep(1.5)
    move.hold("a",2)
    move.hold("d",2.6)
    move.hold("a",0.6)
    sleep(120)

def wreath():
    savedata = loadRes()
    setdat = loadsettings.load()
    ww = savedata['ww']
    wh = savedata['wh']
    for _ in range(2):
        webhook("","Traveling: Honey Wreath","dark brown")
        move.hold("w",1.5)
        move.hold("d",0.9*(setdat["hive_number"])+1)
        pag.keyDown("d")
        time.sleep(0.5)
        move.press("space")
        time.sleep(0.2)
        r = ""
        pag.keyUp("d")
        move.hold("d",15)
        for _ in range(4):
            move.press(",")
        for _ in range(5):
            move.hold("d",0.15)
            r = ebutton()
            if r:
                webhook("","Honey Wreath found","dark brown")
                for _ in range(4):
                    move.press(".")
                move.press("e")
                move.apkey("space")
                savetimings('wreath')
                time.sleep(2)
                acchold("w",0.2)
                acchold("a",0.4)
                acchold("s",0.4)
                acchold("d",0.4)
                acchold("w",0.1)
                acchold("a",0.2)
                acchold("s",0.2)
                acchold("d",0.2)
                acchold("w",0.2)
                reset.reset()
                return
        webhook("","Honey Wreath not found, resetting","dark brown",1)
        reset.reset()
    
def convert():
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    for _ in range(2):
        r = ebutton()
        if r:
            target = r[3]-0.01
            move.press("e")
            webhook("","Starting convert","brown",1)
            st = time.perf_counter()
            while True:
                c = ebutton()
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
def walk_to_hive(gfid):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    webhook("","Going back to hive: {}".format(setdat['gather_field'][gfid]),"dark brown")
    exec(open("walk_{}.py".format(setdat['gather_field'][gfid])).read())
    for _ in range(23):
        pag.keyDown("a")
        time.sleep(0.15)
        pag.keyUp("a")
        r = ebutton()
        if r:
            convert()
            reset.reset()
            return
        
    webhook("","Cant find hive, resetting","dark brown",1)
    reset.reset()
def checkRespawn(m,t):
    timing = float(loadtimings()[m])
    respt = int(''.join([x for x in list(t) if x.isdigit()]))
    if t[-1] == 'h':
        respt = respt*60*60
    else:
        respt = respt*60
    collectList = [x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("collect_")]
    collectList.append("mondo_buff")
    if setdat['gifted_vicious_bee'] and m not in collectList:
        respt = respt/100*85
    if time.time() - timing > respt:
        return 1
    return 0

def savesettings(dictionary,filename):
    templist = []
    for i in dictionary:
        templist.append("\n{}:{}".format(i,dictionary[i]))
    with open('{}'.format(filename), "w") as f:
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
    
def resetMobTimer(cfield):
    if cfield:
        if cfield == "mushroom":
            if checkRespawn("ladybug_mushroom","5m"): savetimings("ladybug_mushroom")
        elif cfield == "strawberry":
            if checkRespawn("ladybug_strawberry","5m"): savetimings("ladybug_strawberry")
        elif cfield == "clover":
            if checkRespawn("ladybug_clover","5m"):
                savetimings("ladybug_clover")
                savetimings("rhinobeetle_clover")
        elif cfield == "pumpkin" or cfield == "cactus":
            if checkRespawn("werewolf","1h"):  savetimings("werewolf")
        elif cfield == "pinetree":
            if checkRespawn("werewolf","1h"):  savetimings("werewolf")
            if checkRespawn("mantis_pinetree","20m"):  savetimings("mantis_pinetree")
        elif cfield == "pineapple":
            if checkRespawn("mantis_pineapple","20m"):  savetimings("mantis_pineapple")
            if checkRespawn("rhinobeetle_pineapple","5m"):  savetimings("rhinobeetle_pineapple")
        elif cfield == "spider":
            if checkRespawn("spider_spider","30m"):  savetimings("spider_spider")
        elif cfield == "rose":
            if checkRespawn("scorpion_rose","20m"):  savetimings("scorpion_rose")
        elif cfield == "blueflower":
            if checkRespawn("rhinobeetle_blueflower","5m"):  savetimings("rhinobeetle_blueflower")
        elif cfield == "bamboo":
            if checkRespawn("rhinobeetle_bamboo","5m"):  savetimings("rhinobeetle_bamboo")

sat_image = cv2.imread('./images/retina/saturator.png')
method = cv2.TM_SQDIFF_NORMED
def displayPlanterName(planter):
    if planter == "redclay":
        return "Red Clay Planter"
    elif planter == "blueclay":
        return "Blue Clay Planter"
    elif planter  == "heattreated":
        return "Heat-Treated Planter"
    elif planter == "plenty":
        return "The Planter of Plenty"
    return "{} Planter".format(planter.title())

def removeComments(strng):
    res = ""
    for c in strng:
        if c == ";":
            return res
        else:
            res += c
    return res
with open ('natro_ba_config.txt','r') as f:
        readdata = f.read()
f.close()
lines = readdata.split('\n')
nectarInfo = {}
planterRanks = {}
currList = ""
for line in lines:
    if not line.startswith(";"):
        if ":=" in line:
            k,v = line.split(":=")
            if "Fields" in k:
                nectarInfo[k] = ast.literal_eval(v)
            elif "Planters" in k:
                if currList:
                    ko,vo = currList.split('=')
                    vo = ast.literal_eval(vo)
                    fields = []
                    for i in vo:
                        planterName = i[0].lower().replace("planter","")
                        if planterName == "ofplenty":
                            planterName = "plenty"
                        fields.append(planterName)
                    ko = ko.lower().replace("planters","")
                    if ko == "blueflower": ko = "blue flower"
                    elif ko == "mountaintop": ko = "mountain top"
                    elif ko == "pinetree": ko = "pine tree"
                    planterRanks[ko] = fields
                currList = "{}={}".format(k,removeComments(v))
        elif line.replace("\t","").startswith(','):
            currList+= removeComments(line).replace("\t","")

    
def getBestPlanter(field,occus,avils):
    for i in planterRanks[field]:
        if i in avils:
            validPlanter = 1
            for j in occus:
                if i == j[0]:
                    validPlanter = 0
                    break
            if validPlanter: return i
    
def placePlanter(planter):
    res = loadRes()
    plantdat = loadsettings.planterLoad()
    ww = res['ww']
    wh = res['wh']
    planterSlot = str(plantdat['{}_slot'.format(planter)])
    print(planterSlot)
    if planterSlot != "none":
        move.press(planterSlot)
    else:
        pag.moveTo(315,224)
        scroll_start = time.time()
        while True:
            pag.scroll(100000)
            if time.time() - scroll_start > 3:
                break
        if not imagesearch.find("sprinklermenu.png".format(planter),0.6,0,wh//10,ww//3,wh):
            pag.moveTo(27,102)
            pag.click()
        pag.moveTo(315,224)
        time.sleep(1)
        setdat = loadsettings.load()
        scroll_start = time.time()
        while True:
            pag.scroll(-100000)
            if time.time() - scroll_start > 3:
                break
        planter_find_start = time.time()
        while True:
            pag.scroll(2400)
            if time.time()-planter_find_start > 30:
                webhook("",'Cant Find: {}'.format(displayPlanterName(planter)),"dark brown")
                break
            if imagesearch.find("{}planter.png".format(planter),0.7,0,wh//10,ww//3,wh):
                time.sleep(0.5)
                r = imagesearch.find("{}planter.png".format(planter),0.7,0,0,ww,wh)
                webhook("",'Found: {}'.format(displayPlanterName(planter)),"dark brown")
                trows,tcols = cv2.imread('./images/retina/{}planter.png'.format(planter)).shape[:2]
                if setdat['display_type'] == "built-in retina display":
                    
                    pag.moveTo(r[1]//2+trows//4,r[2]//2+tcols//4)
                    time.sleep(0.5)
                    pag.dragTo(ww//4, wh//4,0.7, button='left')
                    time.sleep(0.5)
                    clickYes()
                       
                else:
                    pag.moveTo(r[1]+trows//2,r[2]+tcols//2)
                    pag.dragTo(ww//2, wh//2,0.8, button='left')
                    pag.moveTo(ww//4-70,wh//3.2)
                    time.sleep(0.5)
                    clickYes()

                break
        pag.moveTo(27,102)
        pag.click()
    savePlanterTimings(planter)
    webhook("","Placed Planter: {}".format(displayPlanterName(planter)),"bright green",1)
    reset.reset()

urows,ucols = cv2.imread('./images/retina/yes.png').shape[:2]
def clickYes():
    res = loadRes()
    ww = res['ww']
    wh = res['wh']
    setdat = loadsettings.load()
    a = imagesearch.find("yes.png",0.5,0,0,ww,wh)
    if setdat['display_type'] == "built-in retina display":
        if a:
            pag.moveTo(a[1]//2+urows//4,a[2]//2+ucols//4)
            pag.click()
        else:
            pag.moveTo(ww//4-70,wh//3.2)
            pag.click()
    else:
        if a:
            pag.moveTo(a[1]+urows//2,a[2]+ucols//2)
            pag.click()
        else:
            pag.moveTo(ww//2-50,wh//1.6)
            pag.click()
    
def goToPlanter(field,place=0):
    canon()
    exec(open("field_{}.py".format(field)).read())
    if field == "pine tree":
        move.hold("d",3)
        move.hold("s",4)
        if place: move.hold("w",0.07)
    elif field == "pumpkin":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        if place: move.hold("s",0.07)
    elif field  == "strawberry":
        move.hold("d",3)
        move.hold("s",4)
    elif field == "bamboo":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        if place: move.hold("s",0.07)
    elif field  == "pineapple":
        move.hold("d",3)
        move.hold("s",4)
    elif field == "mushroom":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        if place: move.hold("s",0.07)
    elif field == "coconut":
        move.hold("d",5)
        move.hold("s")
    else:
        time.sleep(1)
        
def fieldDriftCompensation():
    res = loadRes()
    ww = res["ww"]
    wh = res["wh"]
    winUp = wh/2.1
    winDown = wh/1.8
    winLeft = ww/2
    winRight = ww/1.7
    for _ in range(4):
        screen = np.array(ImageGrab.grab())
        screen = cv2.cvtColor(src=screen, code=cv2.COLOR_BGR2RGB)
        large_image = screen
        result = cv2.matchTemplate(sat_image, large_image, method)
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        x,y = mnLoc
        if mn < 0.08:
            if x >= winLeft and x <= winRight and y >= winUp and y <= winDown: break
            if x < winLeft:
                move.hold("a",0.1)
            elif x > winRight:
                move.hold("d",0.1)
            if y < winUp:
                move.hold("w",0.1)
            elif y > winDown:
                move.hold("s",0.1)
        else:
            break
        
def background(cf,bpcap,gat,dc):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    while True:
        r = imagesearch.find('disconnect.png',0.8,ww//3,wh//2.8,ww//2.3,wh//2.5)
        if r:
            dc.value = 1
            webhook("","Disconnected","red")
            rejoin()
            dc.value = 0
        
        if gat.value:
            bpcap.value = backpack.bpc()
            resetMobTimer(cf.value.lower())
            if imagesearch.find('died.png',0.8,ww//2,wh//2,ww,wh,1):
                dc.value = 1
                webhook("","Unexpected Death","red")
                dc.value = 0
                gat.value = 0
        if not is_running("Roblox") and dc.value == 0:
            dc.value = 1
            webhook("","Roblox unexpectedly closed","red")
            rejoin()
            dc.value = 0
        if setdat['haste_compensation']:
            if setdat['low_performance_haste_compensation']:
                getHastelp()
            else:
                getHaste()
        if setdat['rejoin_every_enabled']:
            with open('timings.txt', 'r') as f:
                prevTime = float([x for x in f.read().split('\n') if x.startswith('rejoin_every')][0].split(":")[1])
            if (time.time() - prevTime)/3600 > setdat['rejoin_every']:
                dc.value = 1
                rejoin()
                dc.value = 0
                savetimings('rejoin_every')

def killMob(field,mob,reset):
    webhook("","Traveling: {} ({})".format(mob.title(),field.title()),"dark brown")
    convert()
    canon()
    time.sleep(3)
    exec(open("field_{}.py".format(field)).read())
    if mob == "spider":
        for _ in range(4):
            move.press(",")
    lootMob(field,mob,reset)
    
def lootMob(field,mob,resetCheck):
    move.apkey("space")
    webhook("","Looting: {} ({})".format(mob.title(), field.title()),"bright green")
    start = time.time()
    while True:
        moblootPattern(1.1,1.4,"none",2)
        if time.time() - start > 18:
            break
    resetMobTimer(field.replace(" ","").lower())
    if resetCheck:
        reset.reset()
        convert()

def collect(name,beesmas=0):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    dispname = name.replace("_"," ").title()
    usename = name.replace(" ","")
    claimLoot = 0
    for _ in range(2):
        convert()
        canon()
        webhook("","Traveling: {}".format(dispname),"dark brown")
        exec(open("collect_{}.py".format(usename)).read())
        if usename == "wealthclock" or usename == "samovar":
            for _ in range(7):
                move.hold("w",0.1)
                if ebutton():
                    break
        elif usename == "lid_art" or usename == "feast":
            for _ in range(7):
                move.hold("s",0.1)
                if ebutton():
                    break
        time.sleep(0.5)
        if ebutton():
            webhook("","Collected: {}".format(dispname),"bright green",1)
            claimLoot =  1
            break
        webhook("","Unable To Collect: {}".format(dispname),"dark brown",1)
        reset.reset()
    savetimings(usename)
    move.press('e')
    time.sleep(0.5)
    if claimLoot and beesmas:
        sleep(4)
        move.apkey("space")
        exec(open("claim_{}.py".format(usename)).read())
    reset.reset()
def rawreset():
    pag.press('esc')
    time.sleep(0.1)
    pag.press('r')
    time.sleep(0.2)
    pag.press('enter')
    time.sleep(8) 
def updateHive(h):
    global setdat
    webhook("","Found Hive: {}".format(h),"bright green")
    loadsettings.save('hive_number',h)
    
def rejoin():
    for i in range(2):
        cmd = """
            osascript -e 'tell application "Roblox" to quit' 
            """
        os.system(cmd)
        savedata = loadRes()
        ww = savedata['ww']
        wh = savedata['wh']
        webhook("","Rejoining","dark brown")
        time.sleep(3)
        if setdat["private_server_link"]:
            webbrowser.open(setdat['private_server_link'])
        else:
            if i == 0:
                webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
                time.sleep(7)
                _,x,y,_ = imagesearch.find('playbutton.png',0.8)
                webhook("","Play Button Found","dark brown")
                if setdat['display_type'] == "built-in retina display":
                    pag.click(x//2, y//2)
                else:
                    pag.click(x, y)
            else:
                webbrowser.open('https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129')
                time.sleep(6)
                
        time.sleep(setdat['rejoin_delay']*(i+1))
        cmd = """
            osascript -e 'activate application "Roblox"' 
        """
        
        os.system(cmd)
        time.sleep(2)
        move.hold("w",5)
        move.hold("s",0.55)
        foundHive = 0
        move.apkey('space')
        webhook("","Finding Hive", "dark brown",1)
        if setdat['hive_number'] == 3:
            if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found","dark brown",1)
        elif setdat['hive_number'] == 2:
            move.hold('d',1.2)
            if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found","dark brown",1)
        elif setdat['hive_number'] == 1:
            move.hold('d',1.9)
            if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found","dark brown",1)
        elif setdat['hive_number'] == 4:
            move.hold('a',1.1)
            if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found","dark brown",1)
        elif setdat['hive_number'] == 5:
            move.hold('a',2.3)
            if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found","dark brown",1)
        else:
            move.hold('a',3.3)
            if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found","dark brown",1)
        while True:   
            if not foundHive:
                move.hold("d",12)
                webhook("","Hive already claimed, finding new hive","dark brown",1)
                move.hold('a',1)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    updateHive(1)
                    break
                move.hold('a',1.1)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    updateHive(2)
                    break
                move.hold("a",1)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    updateHive(3)
                    break
                move.hold('a',1.1)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    updateHive(4)
                    break
                move.hold('a',1.1)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    updateHive(5)
                    break
                move.hold('a',1)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    updateHive(6)
                    break
                break
            else: break
        if not foundHive:
            rawreset()
            move.hold("w",5)
            move.hold("s",0.55)
            move.hold('d',4)
            starttime = time.time()
            for _ in range(4):
                move.press(",")
            pag.keyDown("d")
            while time.time()-starttime < 10:
                move.press("e")
            pag.keyUp("d")
            updateHive(6)
        convert()
        
        if reset.resetCheck():
            webhook("","Rejoin successful","dark brown")
            break
        webhook("",'Rejoin unsuccessful, attempt 2','dark brown')
    

    
'''
root = tkinter.Tk()
root.withdraw()
ww,wh = root.winfo_screenwidth(), root.winfo_screenheight()
print("{},{}".format(ww,wh))
root.destroy()

updateSave("ww",ww)
updateSave("wh",wh)
'''
            

def placeSprinkler():
    sprinklerCount = {
        "basic":1,
        "silver":2,
        "golden":3,
        "diamond":4,
        "saturator":1

        }
    setdat = loadsettings.load()
    move.press(str(setdat['sprinkler_slot']))
    for _ in range(sprinklerCount[setdat['sprinkler_type']]):
        move.apkey("space")
        time.sleep(0.05)
        move.press(str(setdat['sprinkler_slot']))
        time.sleep(0.5)
def startLoop(cf,bpcap,gat,dc,planterTypes_prev, planterFields_prev):
        
    val = validateSettings()
    if val:
        pag.alert(text='Your settings are incorrect! Check the terminal to see what is wrong.', title='Invalid settings', button='OK')
        print(val)
        sys.exit()
    cmd = """
            osascript -e 'activate application "Roblox"' 
        """
    savetimings('rejoin_every')
    os.system(cmd)
    reset.reset()
    convert()
    savedata = loadRes()
    planterset = loadsettings.planterLoad()
    ww = savedata['ww']
    wh = savedata['wh']
    gfid = 0
    continuePlanters = 0
    if planterset['enable_planters']:
        with open("planterdata.txt","r") as f:
            lines = f.read().split("\n")
        f.close()
        occupiedStuff = ast.literal_eval(lines[0])
        planterTypes = ast.literal_eval(lines[1])
        planterFields = ast.literal_eval(lines[2])
        if planterTypes == planterTypes_prev and planterFields == planterFields_prev:
            continuePlanters = 1
        maxPlanters = planterset['planter_count']
        if len(planterTypes) < maxPlanters:
            maxPlanters = len(planterTypes)
        if len(planterFields) < maxPlanters:
            maxPlanters = len(planterFields)
    
    while True:
        cmd = """
        osascript -e 'activate application "Roblox"' 
        """
        
        os.system(cmd)
        timings = loadtimings()
        setdat = loadsettings.load()
        #Stump snail check
        if setdat['stump_snail'] and checkRespawn("stump_snail","96h"):
            canon()
            webhook("","Traveling: Stump snail (stump) ","brown")
            exec(open("field_stump.py").read())
            time.sleep(0.2)
            move.press(setdat['sprinkler_slot'])
            pag.click()
            webhook("","Starting stump snail","brown")
            while True:
                time.sleep(10)
                pag.click()
                if imagesearch.find("keepold.png",0.9):
                    savetimings("stump_snail")
                    if setdat['continue_after_stump_snail']:break
            webhook("","Stump snail killed, keeping amulet","bright green")
            pag.moveTo(mw//2-30,mh//100*60)
            pag.click()
            reset.reset()
        #Collect check
        if setdat['wealthclock']  and checkRespawn('wealthclock',"1h"):
            collect("wealth clock")
        if setdat['blueberrydispenser'] and checkRespawn('blueberrydispenser','4h'):
            collect('blueberry dispenser')
        if setdat['strawberrydispenser'] and checkRespawn('strawberrydispenser','4h'):
            collect('strawberry dispenser')
        if setdat['royaljellydispenser'] and checkRespawn('royaljellydispenser','22h'):
            collect('royal jelly dispenser')
        if setdat['treatdispenser'] and checkRespawn('treatdispenser','1h'):
            collect('treat dispenser')
        if setdat['stockings'] and checkRespawn('stockings','1h'):
            collect('stockings',1)
        if setdat['wreath'] and checkRespawn('wreath','30m'):
            wreath()
        if setdat['feast'] and checkRespawn('feast','90m'):
            collect('feast',1)
        if setdat['samovar'] and checkRespawn('samovar','6h'):
            collect('samovar',1)
        if setdat['snow_machine'] and checkRespawn('snow_machine','2h'):
            collect('snow_machine')
        if setdat['lid_art'] and checkRespawn('lid_art','8h'):
            collect('lid_art',1)
        if setdat['mondo_buff']:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            hour,minute,_ = [int(x) for x in current_time.split(":")]
            if minute < 10 and checkRespawn('mondo_buff','1h'):
                tempdict = loadtimings()
                tempdict[m] = time.time()//3600
                templist = []
                
                for i in tempdict:
                    templist.append("\n{}:{}".format(i,tempdict[i]))
                with open('timings.txt','w') as f:
                    f.writelines(templist)
                f.close()
                mondo_buff()
                webhook("","Collected: Mondo Buff","bright green")
            
        
        #Planter check
        
        if planterset['enable_planters']:
            if not continuePlanters or not occupiedStuff:
                occupiedStuff = []
                for i in range(maxPlanters):
                    bestPlanter = getBestPlanter(planterFields[i],occupiedStuff,planterTypes)
                    webhook('',"Traveling: {} ({})\nObjective: Place Planter".format(displayPlanterName(bestPlanter),planterFields[i].title()),"dark brown")
                    goToPlanter(planterFields[i],1)
    
                    placePlanter(bestPlanter)
                    occupiedStuff.append((bestPlanter,planterFields[i]))
                continuePlanters = 1
                print(occupiedStuff)
                with open("planterdata.txt","w") as f:
                    f.write("{}\n{}\n{}".format(occupiedStuff,planterTypes,planterFields))
                f.close()
            else:
                planterTimes = {}
                with open("plantertimings.txt","r") as f:
                    lines = f.read().split("\n")
                f.close()
                planterTimes = {}
                for i in lines:
                    if ":" in i:
                        p,t = i.split(":")
                        planterTimes[p] = float(t)
                cycleFields = planterFields.copy()
                collectAnyPlanters = 0
                fieldsToPlace = []
                removeFromOccupied = []
                for i in range(maxPlanters):
                    currPlanter = occupiedStuff[i][0]
                    currField = occupiedStuff[i][1]
                    if str(planterset['harvest']) == "full":
                        growTime = planterInfo[currPlanter]['grow_time']
                        if currField in planterInfo[currPlanter]['grow_fields']:
                            growTime /= planterInfo[currPlanter]['grow_time_bonus']
                    elif str(planterset['harvest']) == "auto":
                        growTime = 1
                    else:
                        growTime = planterset['harvest']
                    occupiedFields = []
                    if time.time() - planterTimes[currPlanter] > growTime*60*60:
                        collectAnyPlanters += 1
                        time.sleep(2)
                        goToPlanter(currField)
                        webhook('',"Traveling: {} ({})\nObjective: Collect Planter".format(displayPlanterName(currPlanter),currField.title()),"dark brown")
                        move.press('e')
                        clickYes()
                        if currField == "pumpkin":
                            for _ in range(4):
                                move.press(",")
                        elif currField == "pine tree" or currField == "strawberry" or currField == "pineapple":
                                move.press(".")
                                move.press(".")
                        starttime = time.time()
                        move.apkey("space")
                        while True:
                            if time.time() - starttime > 20:
                                break
                            moblootPattern(1.1,1.4,"none",2)
                        reset.reset()
                        cycleFields.remove(currField)
                        cycleFields.append(currField)
                        removeFromOccupied.append((currPlanter,currField))
                    else:
                        occupiedFields.append(currField)
                if collectAnyPlanters > 0 and planterFields == cycleFields:
                    firstelement = cycleFields[0]
                    cycleFields.pop(0)
                    cycleFields.append(firstelement)
                planterFields = cycleFields.copy()
                for i in removeFromOccupied:
                    occupiedStuff.remove(i)
                print(occupiedStuff)
                print(occupiedFields)
                print(planterFields)
                for _ in range(maxPlanters-len(occupiedStuff)):
                    for i in planterFields:
                        if i not in fieldsToPlace and i not in occupiedFields:
                            fieldsToPlace.append(i)
                            break
                    
                print(fieldsToPlace)
                for i in fieldsToPlace:
                    bestPlanter = getBestPlanter(i,occupiedStuff,planterTypes)
                    webhook('',"Traveling: {} ({})\nObjective: Place Planter".format(displayPlanterName(bestPlanter),i.title()),"dark brown")
                    goToPlanter(i,1) 
                    placePlanter(bestPlanter)
                    occupiedStuff.append((bestPlanter,i))
                    
                with open("planterdata.txt","w") as f:
                    f.write("{}\n{}\n{}".format(occupiedStuff,planterTypes,planterFields))
                f.close()             
                                                                                        
        #Mob run check
        if setdat['werewolf'] and checkRespawn("werewolf","1h"):
            killMob("pumpkin","werewolf",1)
        if setdat["ladybug"] and checkRespawn("ladybug_strawberry","5m"):
            
            if checkRespawn("ladybug_mushroom","5m"):
                killMob("strawberry","ladybug",0)
                move.hold("s",4)
                move.hold("a",3)
                move.hold("w",5.5)
                move.hold("s",3)
                lootMob("mushroom","ladybug",1)
            else:
                killMob("strawberry","ladybug",1)
        if setdat["ladybug"] and checkRespawn("ladybug_clover","5m"):
            killMob("clover","ladybug",1)
        if setdat["ladybug"] and checkRespawn("ladybug_mushroom","5m"):
            killMob("mushroom","ladybug",1)
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_clover","5m"):
            if checkRespawn("rhinobeetle_blueflower","5m"):
                webhook("","hi","red")
                killMob("clover","rhino beetle",0)
                move.hold("s",7)
                time.sleep(1)
                lootMob("blue flower","rhinobeetle",1)
            else:
                killMob("clover","rhino beetle",1)
            
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_blueflower","5m"):
            killMob("blue flower","rhino beetle",1)
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_bamboo","5m"):
            killMob("bamboo","rhino beetle",1)
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_pineapple","5m"):
            killMob("pineapple","rhino beetle",1)
        if setdat["mantis"] and checkRespawn("mantis_pinetree","20m"):
            killMob("pine tree","mantis",1)
        if setdat["mantis"] and checkRespawn("mantis_pineapple","20m"):
            killMob("pineapple","mantis",1)
        if setdat["scorpion"] and checkRespawn("scorpion_rose","20m"):
            killMob("rose","scorpion",1)
        if setdat["spider"] and checkRespawn("spider_spider","30m"):
            killMob("spider","spider",1)
        #gather check
        if setdat['gather_enable']:
            canon()
            webhook("","Traveling: {}".format(setdat['gather_field'][gfid]),"dark brown")
            exec(open("field_{}.py".format(setdat['gather_field'][gfid])).read())
            cf.value = setdat['gather_field'][gfid].replace(" ","").lower()
            time.sleep(0.2)
            if setdat["before_gather_turn"] == "left":
                for _ in range(setdat["turn_times"]):
                    move.press(",")
            elif setdat["before_gather_turn"] == "right":
                for _ in range(setdat["turn_times"]):
                    move.press(".")
            time.sleep(0.2)
            placeSprinkler()
            pag.click()
            gp = setdat["gather_pattern"].lower()
            webhook("Gathering: {}".format(setdat['gather_field'][gfid]),"Limit: {}.00 - {} - Backpack: {}%".format(setdat["gather_time"],setdat["gather_pattern"],setdat["pack"]),"light green")
            move.apkey("space")
            time.sleep(0.2)
            timestart = time.perf_counter()
            gat.value = 1
            fullTime = 0
            while True:
                time.sleep(0.05)
                mouse.press()
                time.sleep(0.05)
                exec(open("gather_{}.py".format(gp)).read())
                time.sleep(0.05)
                mouse.release()
                time.sleep(0.05)
                timespent = (time.perf_counter() - timestart)/60
                if bpcap.value >= setdat["pack"]:
                    if fullTime == 1:
                        webhook("Gathering: ended","Time: {:.2f} - Backpack - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
                        break
                    else:
                        fullTime += 1
                else:
                    fullTime = 0
                    
                if timespent > setdat["gather_time"]:
                    webhook("Gathering: ended","Time: {:.2f} - Time Limit - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
                    break
                if setdat['field_drift_compensation']:
                    fieldDriftCompensation()
            time.sleep(0.5)
            gat.value = 0
            cf.value = ""
            gfid += 1
            while True:
                if gfid >= len(setdat['gather_field']):
                    gfid = 0
                if setdat["gather_field"][gfid].lower() == "none":
                    gfid += 1
                else: break
            if setdat["before_gather_turn"] == "left":
                for _ in range(setdat["turn_times"]):
                    move.press(".")
            elif setdat["before_gather_turn"] == "right":
                for _ in range(setdat["turn_times"]):
                    move.press(",")
                    
            if setdat['return_to_hive'] == "walk":
                walk_to_hive(gfid)
            elif setdat['return_to_hive'] == "reset":
                reset.reset()
                convert()
            elif setdat['return_to_hive'] == "rejoin":
                rejoin()
                reset.reset()
            elif setdat['return_to_hive'] == "whirligig":
                reject = 0
                webhook("","Activating whirligig","dark brown")
                if setdat['whirligig_slot'] == "none":
                    webhook("Notice","Whirligig option selected but no whirligig slot given, walking back","red")
                    walk_to_hive(gfid)
                else:
                    move.press(str(setdat['whirligig_slot']))
                    time.sleep(1)
                    r = ebutton()
                    if not r or reject:
                        webhook("Notice","Whirligig failed to activate, walking back","red")
                        walk_to_hive()
                    else:
                        convert()
                        reset.reset()
                    
def setResolution():
    wwd = int(pag.size()[0])
    whd = int(pag.size()[1])
    if subprocess.call("system_profiler SPDisplaysDataType | grep -i 'retina'", shell=True) == 0:
        loadsettings.save('display_type', 'built-in retina display')
        print("display type: retina")
        wwd *=2
        whd *=2
    else:
        loadsettings.save('display_type',"built-in display")
        print("display type: built-in")
    print("Screen coordinates: {}x{}".format(wwd,whd))
    with open('save.txt', 'w') as f:
        f.write('wh:{}\nww:{}'.format(whd,wwd))
            
if __name__ == "__main__":
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = bool(subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True).communicate()[0])
    print("\n\nTo launch the macro manually, enter the following 2 commands in terminal:\ncd path/to/macro-folder\npython3 e_macro.py\n\nTo stop the macro, \ntab out of roblox, make sure terminal is in focus and press ctrl c\nor,\nright click the macro app in the dock and force quit")
    print("\n\nYour python version is {}".format(sys.version_info[0]))
    print("Your macro version is {}\n\n".format(macrov))
    setResolution()
    loadSave()
    plantdat = loadsettings.planterLoad()
    ww = savedata["ww"]
    wh = savedata["wh"]
    root = tk.Tk(className='exih_macro')
    root.geometry('780x400')
    s = ttk.Style()
    if p:
        sv_ttk.set_theme("dark")
        wbgc = "#323232"
    else:
        sv_ttk.set_theme("light")
        wbgc = '#E4E4E4'
    wfgc = '#000000'
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, pady = 5)
    img = tk.Image("photo", file="./images/icon.png")
    root.tk.call('wm','iconphoto', root._w, img)

    s.configure('my.TMenubutton', font=('Helvetica', 12))
    s.configure('smaller.TMenubutton', font=('Helvetica', 10))
    
    # create frames
    frame1 = ttk.Frame(notebook, width=780, height=400)
    frame2 = ttk.Frame(notebook, width=780, height=400)
    frame3 = ttk.Frame(notebook, width=780, height=400)
    frame4 = ttk.Frame(notebook, width=780, height=400)
    frame5 = ttk.Frame(notebook, width=780, height=400)
    frame6 = ttk.Frame(notebook, width=780, height=400)

    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    frame3.pack(fill='both', expand=True)
    frame4.pack(fill='both', expand=True)
    frame5.pack(fill='both', expand=True)
    frame6.pack(fill='both', expand=True)

    notebook.add(frame1, text='Gather')
    notebook.add(frame2, text='Bug run')
    notebook.add(frame4, text='Collect')
    notebook.add(frame6, text='Planters')
    notebook.add(frame3, text='Settings')
    notebook.add(frame5, text='Calibration')

    #get variables
    gather_enable = tk.IntVar(value=setdat["gather_enable"])
    gather_field_one = tk.StringVar(root)
    gather_field_one.set(setdat["gather_field"][0].title())
    gather_field_two = tk.StringVar(root)
    gather_field_two.set(setdat["gather_field"][1].title())
    gather_field_three = tk.StringVar(root)
    gather_field_three.set(setdat["gather_field"][2].title())
    return_to_hive = tk.StringVar(root)
    return_to_hive.set(setdat["return_to_hive"].title())
    gather_pattern = tk.StringVar(root)
    gather_pattern.set(setdat["gather_pattern"])
    gather_size = tk.StringVar(root)
    gather_size.set(setdat["gather_size"].title())
    gather_width = tk.IntVar(value=setdat["gather_width"])
    gather_time = setdat["gather_time"]
    pack =setdat["pack"]
    before_gather_turn = tk.StringVar(root)
    before_gather_turn.set(setdat["before_gather_turn"])
    turn_times = tk.IntVar(value=setdat["turn_times"])
    whirligig_slot = tk.StringVar(root)
    whirligig_slot.set(setdat["whirligig_slot"])
    stump_snail = tk.IntVar(value=setdat["stump_snail"])
    continue_after_stump_snail = tk.IntVar(value=setdat["continue_after_stump_snail"])
    ladybug = tk.IntVar(value=setdat["ladybug"])
    rhinobeetle = tk.IntVar(value=setdat["rhinobeetle"])
    werewolf = tk.IntVar(value=setdat["werewolf"])
    scorpion = tk.IntVar(value=setdat["scorpion"])
    spider = tk.IntVar(value=setdat["spider"])
    mantis = tk.IntVar(value=setdat["mantis"])
    gifted_vicious_bee = tk.IntVar(value=setdat["gifted_vicious_bee"])
    enable_discord_webhook = tk.IntVar(value=setdat["enable_discord_webhook"])
    discord_webhook_url= setdat["discord_webhook_url"]
    send_screenshot  = tk.IntVar(value=setdat["send_screenshot"])
    walkspeed = setdat["walkspeed"]
    hive_number = tk.IntVar(value=setdat["hive_number"])
    display_type = tk.StringVar(root)
    display_type.set(setdat["display_type"].capitalize())
    private_server_link = setdat["private_server_link"]
    enable_discord_bot = tk.IntVar(value=setdat["enable_discord_bot"])
    sprinkler_slot = tk.StringVar(root)
    sprinkler_slot.set(setdat["sprinkler_slot"])
    sprinkler_type = tk.StringVar(root)
    sprinkler_type.set(setdat["sprinkler_type"].title())
    discord_bot_token = setdat['discord_bot_token']
    field_drift_compensation = tk.IntVar(value=setdat["field_drift_compensation"])
    haste_compensation = tk.IntVar(value=setdat["haste_compensation"])
    low_performance_haste_compensation = tk.IntVar(value=setdat["low_performance_haste_compensation"])
    rejoin_every_enabled = tk.IntVar(value=setdat["rejoin_every_enabled"])
    rejoin_every = setdat['rejoin_every']
    rejoin_delay = setdat['rejoin_delay']
    
    wealthclock = tk.IntVar(value=setdat["wealthclock"])
    blueberrydispenser = tk.IntVar(value=setdat["blueberrydispenser"])
    strawberrydispenser = tk.IntVar(value=setdat["strawberrydispenser"])
    royaljellydispenser  = tk.IntVar(value=setdat["royaljellydispenser"])
    treatdispenser = tk.IntVar(value=setdat["treatdispenser"])
    stockings = tk.IntVar(value=setdat["stockings"])
    feast = tk.IntVar(value=setdat["feast"])
    samovar = tk.IntVar(value=setdat["samovar"])
    wreath = tk.IntVar(value=setdat["wreath"])
    snow_machine = tk.IntVar(value=setdat["snow_machine"])
    mondo_buff = tk.IntVar(value=setdat["mondo_buff"])
    lid_art = tk.IntVar(value=setdat["lid_art"])
    
    ebthreshold = setdat['ebthreshold']
    ebdetect = tk.StringVar(root)
    ebdetect.set(setdat["ebdetect"])
    canon_time = setdat['canon_time']
    reverse_hive_direction = tk.IntVar(value=setdat['reverse_hive_direction'])

    enable_planters = tk.IntVar(value=plantdat['enable_planters'])
    paper_planter = tk.IntVar(value=plantdat['paper_planter'])
    ticket_planter = tk.IntVar(value=plantdat['ticket_planter'])
    plastic_planter = tk.IntVar(value=plantdat['plastic_planter'])
    candy_planter = tk.IntVar(value=plantdat['candy_planter'])
    blueclay_planter = tk.IntVar(value=plantdat['blueclay_planter'])
    redclay_planter = tk.IntVar(value=plantdat['redclay_planter'])
    tacky_planter = tk.IntVar(value=plantdat['tacky_planter'])
    pesticide_planter = tk.IntVar(value=plantdat['pesticide_planter'])
    heattreated_planter = tk.IntVar(value=plantdat['heattreated_planter'])
    hydroponic_planter = tk.IntVar(value=plantdat['hydroponic_planter'])
    petal_planter = tk.IntVar(value=plantdat['petal_planter'])
    plenty_planter = tk.IntVar(value=plantdat['plenty_planter'])
    festive_planter = tk.IntVar(value=plantdat['festive_planter'])
    paper_slot = tk.StringVar(root)
    paper_slot.set(plantdat['paper_slot'])
    ticket_slot = tk.StringVar(root)
    ticket_slot.set(plantdat['ticket_slot'])
    plastic_slot = tk.StringVar(root)
    plastic_slot.set(plantdat['plastic_slot'])
    candy_slot = tk.StringVar(root)
    candy_slot.set(plantdat['candy_slot'])
    blueclay_slot = tk.StringVar(root)
    blueclay_slot.set(plantdat['blueclay_slot'])
    redclay_slot = tk.StringVar(root)
    redclay_slot.set(plantdat['redclay_slot'])
    tacky_slot = tk.StringVar(root)
    tacky_slot.set(plantdat['tacky_slot'])
    pesticide_slot = tk.StringVar(root)
    pesticide_slot.set(plantdat['pesticide_slot'])
    heattreated_slot = tk.StringVar(root)
    heattreated_slot.set(plantdat['heattreated_slot'])
    hydroponic_slot = tk.StringVar(root)
    hydroponic_slot.set(plantdat['hydroponic_slot'])
    petal_slot = tk.StringVar(root)
    petal_slot.set(plantdat['plenty_slot'])
    plenty_slot = tk.StringVar(root)
    plenty_slot.set(plantdat['plenty_slot'])
    festive_slot = tk.StringVar(root)
    festive_slot.set(plantdat['festive_slot'])
    harvest = plantdat['harvest']
    planter_count = tk.StringVar(root)
    planter_count.set(plantdat['planter_count'])
    harvest_full = tk.IntVar(value=boolToInt(str(harvest)=="full"))
    harvest_auto = tk.IntVar(value=boolToInt(str(harvest)=="auto"))
    harvest_int = plantdat['harvest']
    slot_options = ["none"]+[x+1 for x in range(7)]
    gather_fields = [x.split("_")[1][:-3].title() for x in os.listdir("./") if x.startswith("field_")]
    gather_fields.insert(0,"None")
    field_options = tk.Variable(value=[x.split("_")[1][:-3].title() for x in os.listdir("./") if x.startswith("field_")])
    planter_fields =  plantdat['planter_fields']



    
    wwa  = savedata['ww']
    wha = savedata['wh']

    def screenshothive():
        cmd = """
                    osascript -e  'activate application "Roblox"'
                """
        os.system(cmd)
        setdat = loadsettings.load()
        maxvals = []
        savedata = loadSave()
        pag.moveTo(350,100)
        savedata = loadRes()
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//4*3
        xt = xo*3-xo
        yt = wh-yo
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
        for _ in range(2):
            r = imagesearch.find("hive0.png",0, xo, yo, xt, yt)
            maxvals.append(r[3])
            for _ in range(4):
                pag.press(",")
                
        if maxvals[0] < maxvals[1]:
            for _ in range(4):
                pag.press(",")
        xo = ww//4
        yo = wh-2
        xt = ww//8
        yt = 2
        webhook("","Screenshotting: hive1.png","dark brown",1)
        im = pag.screenshot(region = (xo,yo,xt,yt))
        if setdat['display_type'] ==  "built-in retina display":
            im.save('./images/retina/hive1.png')
        else:
            im.save('./images/built-in/hive1.png')
            
        
    def calibratehive(term=1):
        if subprocess.call("system_profiler SPDisplaysDataType | grep -i 'retina'", shell=True) == 0:
            loadsettings.save('display_type', 'built-in retina display')
        else:
            loadsettings.save('display_type',"built-in display")
        if not calibrate_hive.calibrate():
            cmd = """
                    osascript -e  'activate application "Terminal"'
                """
            os.system(cmd)
            window = tk.Toplevel()
            label = tk.Label(window, text="ERROR calibrating, ensure that:\n\n -Roblox is in fullscreen\n -Terminal has screen recording permissions (System prefences -> security and privacy -> privacy -> screen recording)\n\nIf the issue still persists, go to calibration tab -> calibrate hive.",bg=wbgc)
            button_no = ttk.Button(window, text="Ok", command=window.destroy)
            label.grid(row=0, column=0, columnspan=2)
            button_no.grid(row=1, column=1)
            return False
        elif term:
            cmd = """
                    osascript -e  'activate application "Terminal"'
                """
            os.system(cmd)

        return True
        
            
    def calibratebp():
        webhook("","Calibrating: Backpack","dark brown")
        savedata = loadRes()
        reset.reset()
        webhook("","Filling up backpack","dark brown")
        canon()
        time.sleep(2)
        exec(open("{}.py".format(setdat['gather_field'])).read())
        time.sleep(1)
        webhook("Gathering: {}".format(setdat['gather_field']),"Limit: {}.00 - {} - Backpack: {}%".format(setdat["gather_time"],setdat["gather_pattern"],setdat["pack"]),"light green")
        move.apkey("space")
        placeSprinkler()
        time.sleep(0.2)
        if setdat["before_gather_turn"] == "left":
            for _ in range(setdat["turn_times"]):
                move.press(",")
        elif setdat["before_gather_turn"] == "right":
            for _ in range(setdat["turn_times"]):
                move.press(".")
        timestart = time.perf_counter()
        while True:
            time.sleep(0.05)
            pag.mouseDown()
            time.sleep(0.05)
            exec(open("gather_{}.py".format(setdat['gather_pattern'])).read())
            time.sleep(0.05)
            pag.mouseUp()
            time.sleep(0.05)
            timespent = (time.perf_counter() - timestart)/60
            if timespent > 20:
                webhook("Gathering: ended","Time: {:.2f}".format(timespent),"light green")
                break
            if setdat['field_drift_compensation']:
                fieldDriftCompensation()
        time.sleep(0.5)
        webhook("","Finding coordinates of backpack","dark brown")
        for x in range(ww//2+50,ww//2+200):
            for y in range(6,18):
                pix = pag.pixel(x,y)
                if pix[0] > 230:
                    #savesettings("bploc",[x,y])
                    webhook("","Success! Backpack coordinates found at: {},{}".format(x,y),"light blue")
                    break
            else:
                continue
            break
    def screenshotebutton():
        setdat = loadsettings.load()
        webhook("","Screenshotting: eb.png","dark brown")
        xo = ww//2.6
        yo = wh//19
        xt = ww//25
        yt = wh//30
        im = pag.screenshot(region = (xo,yo,xt,yt))
        if setdat['display_type'] ==  "built-in retina display":
            im.save('./images/retina/eb.png')
        else:
            im.save('./images/built-in/eb.png')

    def calibrateebutton():
        setdat = loadsettings.load()
        savedata = loadRes()
        ww = savedata['ww']
        wh = savedata['wh']
        webhook("","Calibrating: e_button","dark brown",1)        
        vals = []
        reset.reset()
        move.hold("w",2)
        move.hold("d",0.9*(setdat["hive_number"])+1)
        pag.keyDown("d")
        time.sleep(0.5)
        move.press("space")
        time.sleep(0.2)
        r = ""
        pag.keyUp("d")
        for _ in range(7):
            move.hold("d",0.15)
            vals.append(imagesearch.find("eb.png",0,0,0,ww,wh//2)[3])
            
        webhook("","Done obtaining vals","dark brown")
            
        vals = sorted(vals,reverse=True)
        print(vals)
        gap = vals[0] - 0.05
        truemin = 0
        for i in range(len(vals)):
            if vals[i] > gap:
                truemin = vals[i]
            else:
                break
        thresh = math.floor(truemin*100)/100
        webhook("","Calculated: E Button Threshold\nValue: {}".format(thresh),"dark brown")
        webhook("","Determining e button detect type","dark brown")
        loadsettings.save("ebthreshold",thresh)
        loadsettings.save("ebdetect","cv2")
        reset.reset()
        canon()
        #screenshotebutton()
        #r=imagesearch.find("eb.png",0,0,0,ww,wh//2)[3]
        #thresh = math.ceil((r*100)/100)
        #loadsettings.save("ebthreshold",thresh)
        if ebutton(1):
            loadsettings.save("ebdetect","pyautogui")
            webhook("","E button detect type: pyautogui".format(thresh),"light blue")
        else:
            webhook("","E button detect type: cv2".format(thresh),"light blue")

    def calibrate():
        if calibratehive(0):
            calibrateebutton()
            webhook("","Calibration Complete","light green")
            cmd = """
                    osascript -e  'activate application "Terminal"'
                """
            os.system(cmd)
            window = tk.Toplevel()
            label = tk.Label(window, text="Calibration complete")
            button_no = ttk.Button(window, text="Ok", command=window.destroy)
            label.grid(row=0, column=0, columnspan=2)
            button_no.grid(row=1, column=1)
            
            
    def updateGo():
        update.update()
        exit()
    def updateExp():
        updateexperiment.update()
        exit()

    def expu():
        window = tk.Toplevel() #creates a window to confirm if the user wants to start deleting files
        #window.config(bg=wbgc)
        label = tk.Label(window, text="Are you sure you want to update the macro to experimental version?\n(your settings and images will be replaced)\nYou can click the update button to go back to the main macro",bg=wbgc)
        button_yes = ttk.Button(window, text="Yes",command=updateExp)
        button_no = ttk.Button(window, text="No", command=window.destroy)
        label.grid(row=0, column=0, columnspan=2)
        button_yes.grid(row=1, column=0)
        button_no.grid(row=1, column=1)
    
        
    def updateFiles():
        window = tk.Toplevel() #creates a window to confirm if the user wants to start deleting files
        window.config(bg=wbgc)
        label = tk.Label(window, text="Are you sure you want to update the macro?\n(your settings and images will be replaced)")
        button_yes = ttk.Button(window, text="Yes",command=updateGo)
        button_no = ttk.Button(window, text="No", command=window.destroy)
        label.grid(row=0, column=0, columnspan=2)
        button_yes.grid(row=1, column=0)
        button_no.grid(row=1, column=1)
         
    def startGo():
        global setdat, stop, planterTypes_prev, planterFields_prev
        setdat = loadsettings.load()
        planterFields_set = []
        for i in listbox.curselection():
            planterFields_set.append(listbox.get(i).lower())
        setdict = {
            "hive_number": hive_number.get(),
            "walkspeed": speedtextbox.get(1.0,"end").replace("\n",""),
            "gifted_vicious_bee": gifted_vicious_bee.get(),
            "enable_discord_webhook": enable_discord_webhook.get(),
            "discord_webhook_url": urltextbox.get(1.0,"end").replace("\n",""),
            "send_screenshot": send_screenshot.get(),
            "sprinkler_slot": sprinkler_slot.get(),
            "sprinkler_type": sprinkler_type.get(),
            "display_type": display_type.get().lower(),
            "private_server_link":linktextbox.get(1.0,"end").replace("\n",""),
            "enable_discord_bot":enable_discord_bot.get(),
            "discord_bot_token":tokentextbox.get(1.0,"end").replace("\n",""),
            "field_drift_compensation": field_drift_compensation.get(),
            "haste_compensation": haste_compensation.get(),
            "low_performance_haste_compensation": low_performance_haste_compensation.get(),
            "rejoin_every_enabled": rejoin_every_enabled.get(),
            "rejoin_every": rejoinetextbox.get(1.0,"end").replace("\n",""),
            "rejoin_delay": rejoindelaytextbox.get(1.0,"end").replace("\n",""),
            
            "gather_enable": gather_enable.get(),
            "gather_field": [gather_field_one.get(),gather_field_two.get(),gather_field_three.get()],
            "gather_pattern": gather_pattern.get(),
            "gather_size": gather_size.get(),
            "gather_width": gather_width.get(),
            "gather_time": timetextbox.get(1.0,"end").replace("\n",""),
            "pack": packtextbox.get(1.0,"end").replace("\n",""),
            "before_gather_turn": before_gather_turn.get(),
            "turn_times": turn_times.get(),
            "return_to_hive": return_to_hive.get(),
            "whirligig_slot": whirligig_slot.get(),
                
            "stump_snail": stump_snail.get(),
            "continue_after_stump_snail": continue_after_stump_snail.get(),
            "ladybug": ladybug.get(),
            "rhinobeetle": rhinobeetle.get(),
            "spider": spider.get(),
            "scorpion": scorpion.get(),
            "werewolf": werewolf.get(),
            "mantis": mantis.get(),

            "wealthclock": wealthclock.get(),
            "blueberrydispenser": blueberrydispenser.get(),
            "strawberrydispenser": strawberrydispenser.get(),
            "royaljellydispenser":royaljellydispenser.get(),
            "treatdispenser":treatdispenser.get(),
            "stockings":stockings.get(),
            "feast": feast.get(),
            "samovar": samovar.get(),
            "wreath": wreath.get(),
            "snow_machine": snow_machine.get(),
            "mondo_buff": mondo_buff.get(),
            "lid_art":lid_art.get(),

            "hivethreshold":setdat['hivethreshold'],
            "ebthreshold":ebtextbox.get(1.0,"end").replace("\n",""),
            "ebdetect":ebdetect.get(),
            "bploc":setdat['bploc'],
            "canon_time":cttextbox.get(1.0,"end").replace("\n",""),
            "reverse_hive_direction": reverse_hive_direction.get()


        }

        planterdict = {

            "enable_planters": enable_planters.get(),
            "paper_planter": paper_planter.get(),
            "ticket_planter": ticket_planter.get(),
            "plastic_planter": plastic_planter.get(),
            "candy_planter": candy_planter.get(),
            "blueclay_planter": blueclay_planter.get(),
            "redclay_planter":redclay_planter.get(),
            "tacky_planter":tacky_planter.get(),
            "pesticide_planter":pesticide_planter.get(),
            'heattreated_planter': heattreated_planter.get(),
            'hydroponic_planter': hydroponic_planter.get(),
            "petal_planter": petal_planter.get(),
            "plenty_planter": plenty_planter.get(),
            "festive_planter": festive_planter.get(),
            "paper_slot": paper_slot.get(),
            "ticket_slot": ticket_slot.get(),
            "plastic_slot": plastic_slot.get(),
            "candy_slot": candy_slot.get(),
            "blueclay_slot": blueclay_slot.get(),
            "redclay_slot": redclay_slot.get(),
            "tacky_slot": tacky_slot.get(),
            "pesticide_slot": pesticide_slot.get(),
            "heattreated_slot": heattreated_slot.get(),
            "hydroponic_slot": hydroponic_slot.get(),
            "petal_slot": petal_slot.get(),
            "plenty_slot":plenty_slot.get(),
            "festive_slot":festive_slot.get(),
            'planter_fields':planterFields_set,
            "planter_count": planter_count.get(),
            "harvest": harvesttextbox.get(1.0,"end").replace("\n","")
        
            }
                

        
        #ww = int(wwatextbox.get(1.0,"end").replace("\n",""))
        #wh = int(whatextbox.get(1.0,"end").replace("\n",""))
        #if setdict["display_type"] == "built-in retina display":
            #if ww<2000:
                #pag.alert(text='The resolution is invalid for a built-in retina display. Check it by going to about this mac -> displays', title='Setting error', button='OK')
                #return
        '''
            "dandelion_field": dandelion_field.get(),
            "sunflower_field": sunflower_field.get(),
            "mushroom_field": mushroom_field.get(),
            "blue_flower_field": blue_flower_field.get(),
            "clover_field": clover_field.get(),
            "spider_field": spider_field.get(),
            "strawberry_field": strawberry_field.get(),
            "bamboo_field":bamboo_field.get(),
            "pineapple_field":pineapple_field.get(),
            "stump_field":stump_field.get(),
            "cactus_field":cactus_field.get(),
            "pumpkin_field":pumpkin_field.get(),
            "pine_tree_field":pine_tree_field.get(),
            "rose_field":rose_field.get(),
            "mountain_top_field":mountain_top_field.get(),
            "coconut_field":coconut_field.get(),
            "pepper_field":pepper_field.get(),
        '''
        try:
            a = float(setdict["walkspeed"])
        except:
            pag.alert(text="The walkspeed of {} is not a valid number/decimal".format(setdict['walkspeed']),title="Invalid setting",button="OK")
            return
        with open('save.txt', 'w') as f:
            f.write('wh:{}\nww:{}'.format(wh,ww))
        f.close()
        
        savesettings(setdict,"settings.txt")
        savesettings(planterdict,"plantersettings.txt")
        
        with open("haste.txt","w") as a:
            a.write(setdict["walkspeed"])
        a.close()
        if str(planterdict['enable_planters']) == "1":
            planterTypes_set = []
            for s in planterdict:
                if str(planterdict[s]) == "1" and "_" in s:
                    info,suffix = s.rsplit("_",1)
                    #planterTypes, planterFields
                    if suffix == "planter":
                        planterTypes_set.append(info)

            if sorted(planterFields_set) != sorted(planterFields_prev) or sorted(planterTypes_prev) != sorted(planterTypes_set):
                with open("planterdata.txt","w") as f:
                    f.write("[]\n{}\n{}".format(planterTypes_set,planterFields_set))
                f.close()
                with open("plantertimings.txt","r") as f:
                    lines = f.read().split("\n")
                f.close()
                with open("plantertimings.txt","w") as f:
                    writeStuff = []
                    for i in lines:
                        if ":" in i:
                            k,_ = i.split(':')
                            writeStuff.append("{}:0".format(k))
                    print(writeStuff)
                    f.write('\n'.join(writeStuff))
                f.close()
                
                            
            
        if int(setdict['hivethreshold']) == 1:
            window = tk.Toplevel() 
            label = tk.Label(window,text="You have not calibrated your macro yet. Do you want to calibrate it automatically?")
            button_yes = ttk.Button(window, text="Yes",command=lambda: [calibrate(), window.destroy()]) 
            button_no = ttk.Button(window, text="No",command=lambda: [macro(),window.destroy()]) 
            label.grid(row=0, column=0, columnspan=2)
            button_yes.grid(row=1, column=0)
            button_no.grid(row=1, column=1)
        else:
            macro()
            pass

    def macro():
        webhook("Macro started","exih_macro {}".format(macrov),"dark brown")
        setdat = loadsettings.load()
        if not is_running("roblox"):
            rejoin()
        startLoop_proc = multiprocessing.Process(target=startLoop,args=(currentfield,bpc,gather,disconnected,planterTypes_prev, planterFields_prev))
        startLoop_proc.start()
        background_proc = multiprocessing.Process(target=background,args=(currentfield,bpc,gather,disconnected))
        background_proc.start()
        discord_bot_proc = multiprocessing.Process(target=discord_bot,args=(disconnected,))
        discord_bot_proc.start()
        try:
            while True:
                if disconnected.value:
                    startLoop_proc.terminate()
                    while disconnected.value:
                        pass
                    startLoop_proc = multiprocessing.Process(target=startLoop,args=(currentfield,bpc,gather,disconnected,planterTypes_prev, planterFields_prev))
                    startLoop_proc.start()
                    
        except KeyboardInterrupt:
            startLoop_proc.terminate()
            background_proc.terminate()
            discord_bot_proc.terminate()
            webhook("Macro Stopped","","dark brown")
    
    def savedisplaytype(event):
        loadsettings.save("display_type",display_type.get().lower())
        setResolution()
        
    def disablews(event):
        if return_to_hive.get().lower() == "whirligig":
            wslotmenu.configure(state="normal")
        else:
            wslotmenu.configure(state="disable")
    def disableeb(event):
        if ebdetect.get().lower() == "pyautogui":
            ebtextbox.configure(state="disable")
        else:
            ebtextbox.configure(state="normal")

    def disabledw():
        if str(enable_discord_webhook.get()) == "1":
            sendss.configure(state="normal")
            urltextbox.configure(state="normal")
        else:
            sendss.configure(state="disable")
            urltextbox.configure(state="disable")

    def changeHarvest(selected):
        global harvest_full, harvest_auto, harvest_int
        htt = harvesttextbox.get(1.0,"end").replace("\n","")
        harvesttextbox.configure(state="normal")
        if htt.isdigit():
            harvest_int = htt
        if harvest_full.get() and selected == "full":
            harvesttextbox.delete("1.0", "end")
            harvesttextbox.insert("end","Full")
            harvesttextbox.configure(state="disable")
            harvest_auto.set(0)
        elif harvest_auto.get() and selected == "auto":
            harvesttextbox.delete("1.0", "end")
            harvesttextbox.insert("end","Auto")
            harvest_full.set(0)
            harvesttextbox.configure(state="disable")
        else:
            harvesttextbox.delete("1.0", "end")
            harvesttextbox.insert("end",harvest_int)
            
    #Tab 1
    tkinter.Checkbutton(frame1, text="Enable Gathering", variable=gather_enable).place(x=0, y = 15)
    dropField = ttk.OptionMenu(frame1, gather_field_one,setdat['gather_field'][0].title(), *gather_fields[1:],style='my.TMenubutton' )
    dropField.place(x = 120, y = 50,height=24,width=120)
    dropField = ttk.OptionMenu(frame1, gather_field_two,setdat['gather_field'][1].title(), *gather_fields,style='my.TMenubutton' )
    dropField.place(x = 260, y = 50,height=24,width=120)
    dropField = ttk.OptionMenu(frame1, gather_field_three,setdat['gather_field'][2].title(), *gather_fields,style='my.TMenubutton' )
    dropField.place(x = 400, y = 50,height=24,width=120)
    tkinter.Label(frame1, text = "Gathering Fields").place(x = 0, y = 50)

    tkinter.Label(frame1, text = "Gathering Pattern").place(x = 0, y = 85)
    dropField = ttk.OptionMenu(frame1, gather_pattern,setdat['gather_pattern'], *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")],style='my.TMenubutton')
    dropField.place(width=110,x = 120, y = 85,height=24)
    tkinter.Label(frame1, text = "Size").place(x = 250, y = 85)
    dropField = ttk.OptionMenu(frame1, gather_size,setdat['gather_size'].title(), *["S","M","L"],style='my.TMenubutton' )
    dropField.place(width=50,x = 290, y = 85,height = 24)
    tkinter.Label(frame1, text = "Width").place(x = 360, y = 85)
    dropField = ttk.OptionMenu(frame1, gather_width,setdat['gather_width'], *[(x+1) for x in range(10)],style='my.TMenubutton' )
    dropField.place(width=50,x = 410, y = 85,height=24)

    tkinter.Label(frame1, text = "Before Gathering, Rotate Camera").place(x = 0, y = 120)
    dropField = ttk.OptionMenu(frame1, before_gather_turn,setdat['before_gather_turn'].title(), *["None","Left","Right"],style='my.TMenubutton' )
    dropField.place(width=70,x = 215, y = 120,height=24)
    dropField = ttk.OptionMenu(frame1, turn_times,setdat['turn_times'], *[(x+1) for x in range(4)],style='my.TMenubutton' )
    dropField.place(width=50,x = 295, y = 120,height=24)

    tkinter.Label(frame1, text = "Gather Until:").place(x = 0, y = 155)
    tkinter.Label(frame1, text = "Mins").place(x = 90, y = 155)
    timetextbox = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    timetextbox.insert("end",gather_time)
    timetextbox.place(x = 130, y=158)
    tkinter.Label(frame1, text = "Backpack%").place(x = 175, y = 155)
    packtextbox = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    packtextbox.insert("end",pack)
    packtextbox.place(x = 260, y=158)
    tkinter.Label(frame1, text = "To Hive By").place(x = 305, y = 155)
    dropConvert = ttk.OptionMenu(frame1 , return_to_hive,setdat['return_to_hive'].title(), command = disablews, *["Walk","Reset","Rejoin","Whirligig"],style='my.TMenubutton')
    dropConvert.place(width=85,x = 380, y = 155,height=24)
    tkinter.Label(frame1, text = "Whirligig Slot").place(x = 480, y = 155)
    wslotmenu = ttk.OptionMenu(frame1 , whirligig_slot,setdat['whirligig_slot'], *[1,2,3,4,5,6,7,"none"],style='my.TMenubutton')
    wslotmenu.place(width=70,x = 570, y = 155,height=24)

    tkinter.Checkbutton(frame1, text="Field Drift Compensation", variable=field_drift_compensation).place(x=0, y = 190)
    

    #Tab 2 
    tkinter.Checkbutton(frame2, text="Apply gifted vicious bee hive bonus", variable=gifted_vicious_bee).place(x=0, y = 15)
    tkinter.Checkbutton(frame2, text="Stump Snail", variable=stump_snail).place(x=0, y = 50)
    tkinter.Checkbutton(frame2, text="Continue macro after stump snail is killed", variable=continue_after_stump_snail).place(x=120, y = 50)
    tkinter.Checkbutton(frame2, text="Ladybug", variable=ladybug).place(x=0, y = 85)
    tkinter.Checkbutton(frame2, text="Rhino Beetle", variable=rhinobeetle).place(x=80, y = 85)
    tkinter.Checkbutton(frame2, text="Scorpion", variable=scorpion).place(x=190, y = 85)
    tkinter.Checkbutton(frame2, text="Mantis", variable=mantis).place(x=275, y = 85)
    tkinter.Checkbutton(frame2, text="Spider", variable=spider).place(x=345, y = 85)
    tkinter.Checkbutton(frame2, text="Werewolf", variable=werewolf).place(x=415, y = 85)

    #Tab 3
    tkinter.Checkbutton(frame4, text="Wealth Clock", variable=wealthclock).place(x=0, y = 15)
    tkinter.Checkbutton(frame4, text="Mondo Buff", variable=mondo_buff).place(x=120, y = 15)
    tkinter.Checkbutton(frame4, text="Blueberry Dispenser", variable=blueberrydispenser).place(x=0, y = 50)
    tkinter.Checkbutton(frame4, text="Strawberry Dispenser", variable=strawberrydispenser).place(x=160, y = 50)
    tkinter.Checkbutton(frame4, text="(Free) Royal Jelly Dispenser", variable=royaljellydispenser).place(x=320, y = 50)
    tkinter.Checkbutton(frame4, text="Treat Dispenser", variable=treatdispenser).place(x=520, y = 50)
    tkinter.Checkbutton(frame4, text="Stockings", variable=stockings).place(x=0, y = 85)
    tkinter.Checkbutton(frame4, text="Feast", variable=feast).place(x=100, y = 85)
    tkinter.Checkbutton(frame4, text="Samovar", variable=samovar).place(x=175, y = 85)
    tkinter.Checkbutton(frame4, text="Snow Machine", variable=snow_machine).place(x=265, y = 85)
    tkinter.Checkbutton(frame4, text="Lid Art", variable=lid_art).place(x=390, y = 85)
    tkinter.Checkbutton(frame4, text="Honey Wreath", variable=wreath).place(x=470, y = 85)
    #Tab 4
    tkinter.Checkbutton(frame6, text="Enable Planters", variable=enable_planters).place(x=545, y = 20)
    tkinter.Label(frame6, text = "Allowed Planters").place(x = 120, y = 15)
    tkinter.Label(frame6, text = "slot").place(x = 105, y = 40)
    tkinter.Checkbutton(frame6, text="Paper", variable=paper_planter).place(x=0, y = 65)
    tkinter.Checkbutton(frame6, text="Ticket", variable=ticket_planter).place(x=0, y = 100)
    tkinter.Checkbutton(frame6, text="Plastic", variable=plastic_planter).place(x=0, y = 135)
    tkinter.Checkbutton(frame6, text="Candy", variable=candy_planter).place(x=0, y = 170)
    tkinter.Checkbutton(frame6, text="Blue Clay", variable=blueclay_planter).place(x=0, y = 205)
    tkinter.Checkbutton(frame6, text="Red Clay", variable=redclay_planter).place(x=0, y = 240)
    tkinter.Checkbutton(frame6, text="Tacky", variable=tacky_planter).place(x=0, y = 275)

    tkinter.Checkbutton(frame6, text="Pesticide", variable=pesticide_planter).place(x=175, y = 65)
    tkinter.Checkbutton(frame6, text="Heat-Treated", variable=heattreated_planter).place(x=175, y = 100)
    tkinter.Checkbutton(frame6, text="Hydroponic", variable=hydroponic_planter).place(x=175, y = 135)
    tkinter.Checkbutton(frame6, text="Petal", variable=petal_planter).place(x=175, y = 170)
    tkinter.Checkbutton(frame6, text="Planter of Plenty", variable=plenty_planter).place(x=175, y = 205)
    tkinter.Checkbutton(frame6, text="Festive", variable=festive_planter).place(x=175, y = 240)
    
    dropField = ttk.OptionMenu(frame6, paper_slot,plantdat['paper_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 90, y = 69,height=20)
    dropField = ttk.OptionMenu(frame6, ticket_slot,plantdat['ticket_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 90, y = 69+35,height=20)
    dropField = ttk.OptionMenu(frame6, plastic_slot,plantdat['plastic_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 90, y = 69+35*2,height=20)
    dropField = ttk.OptionMenu(frame6, candy_slot,plantdat['candy_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 90, y = 69+35*3,height=20)
    dropField = ttk.OptionMenu(frame6, blueclay_slot,plantdat['blueclay_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 90, y = 69+35*4,height=20)
    dropField = ttk.OptionMenu(frame6, redclay_slot,plantdat['redclay_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 90, y = 69+35*5,height=20)
    dropField = ttk.OptionMenu(frame6, tacky_slot,plantdat['tacky_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 90, y = 69+35*6,height=20)

    dropField = ttk.OptionMenu(frame6, pesticide_slot,plantdat['pesticide_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 290, y = 69,height=20)
    dropField = ttk.OptionMenu(frame6, heattreated_slot,plantdat['heattreated_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 290, y = 69+35,height=20)
    dropField = ttk.OptionMenu(frame6, hydroponic_slot,plantdat['hydroponic_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 290, y = 69+35*2,height=20)
    dropField = ttk.OptionMenu(frame6, petal_slot,plantdat['petal_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 290, y = 69+35*3,height=20)
    dropField = ttk.OptionMenu(frame6, plenty_slot,plantdat['plenty_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 290, y = 69+35*4,height=20)
    dropField = ttk.OptionMenu(frame6, festive_slot,plantdat['festive_slot'], *slot_options,style='smaller.TMenubutton')
    dropField.place(width=65,x = 290, y = 69+35*5,height=20)


    tkinter.Label(frame6, text = "Allowed Fields").place(x = 400, y = 15)
    ttk.Separator(frame6,orient="vertical").place(x=370, y=30, width=2, height=260)    
    listbox = tk.Listbox(frame6,listvariable=field_options,height=7,selectmode=tk.MULTIPLE)
    scrollbar = ttk.Scrollbar(frame6,orient=tk.VERTICAL,command=listbox.yview)
    listbox['yscrollcommand'] = scrollbar.set
    listbox.configure(font=('Helvetica 14'),width=14)
    listbox.place(x=400,y=70)
    scrollbar.place(x=513,y=75,height=110)
    for i in planter_fields:
        listbox.select_set(field_options.get().index(i.title()))

    
    dropField = ttk.OptionMenu(frame6, planter_count,plantdat['planter_count'], *[1,2,3],style='my.TMenubutton' )
    dropField.place(x = 630, y = 70,height=24,width=60)
    tkinter.Label(frame6, text = "Max planters").place(x=545,y=70)
    tkinter.Label(frame6, text = "Harvest Every").place(x=545,y=105)
    harvesttextbox = tkinter.Text(frame6, width = 4, height = 1, bg= wbgc)
    harvesttextbox.insert("end",harvest)
    harvesttextbox.place(x = 637, y=107)
    tkinter.Label(frame6, text = "Hours").place(x=674,y=105)
    tkinter.Checkbutton(frame6, text="Full Grown", variable=harvest_full,command=lambda: changeHarvest("full")).place(x=545, y = 140)
   #tkinter.Checkbutton(frame6, text="Auto", variable=harvest_auto,command=lambda: changeHarvest("auto")).place(x=640, y = 140)

    

    #Tab 5
    tkinter.Label(frame3, text = "Hive Slot (6-5-4-3-2-1)").place(x = 0, y = 15)
    dropField = ttk.OptionMenu(frame3, hive_number, setdat['hive_number'], *[x+1 for x in range(6)],style='my.TMenubutton' )
    dropField.place(width=60,x = 160, y = 15,height=24)
    tkinter.Label(frame3, text = "Move Speed (without haste)").place(x = 0, y = 50)
    speedtextbox = tkinter.Text(frame3, width = 4, height = 1, bg= wbgc)
    speedtextbox.insert("end",walkspeed)
    speedtextbox.place(x = 185, y=52)
    tkinter.Checkbutton(frame3, text="Enable Discord Webhook", command = disabledw,variable=enable_discord_webhook).place(x=0, y = 85)
    tkinter.Label(frame3, text = "Discord Webhook Link").place(x = 350, y = 85)
    urltextbox = tkinter.Text(frame3, width = 24, height = 1, yscrollcommand = True, bg= wbgc)
    urltextbox.insert("end",discord_webhook_url)
    sendss = tkinter.Checkbutton(frame3, text="Send screenshots", variable=send_screenshot)
    sendss.place(x=200, y = 85)
    urltextbox.place(x = 500, y=87)

    tkinter.Label(frame3, text = "Sprinkler Type").place(x = 0, y = 120)
    dropField = ttk.OptionMenu(frame3, sprinkler_type, setdat['sprinkler_type'], *["Basic","Silver","Golden","Diamond","Saturator"],style='my.TMenubutton' )
    dropField.place(width=90,x = 100, y = 120,height=24)

    tkinter.Label(frame3, text = "Slot").place(x = 205, y = 120)
    dropField = ttk.OptionMenu(frame3, sprinkler_slot, setdat['sprinkler_slot'], *[x+1 for x in range(6)],style='my.TMenubutton' )
    dropField.place(width=60,x = 245, y = 120,height=24)
    

    #tkinter.Label(frame3, text = "Width", bg = wbgc).place(x = 150, y = 120)
    #wwatextbox = tkinter.Text(frame3, width = 5, height = 1)
    #wwatextbox.insert("end",wwa)
    #wwatextbox.place(x=200,y=122)
    #tkinter.Label(frame3, text = "Height", bg = wbgc).place(x = 260, y = 120)
    #whatextbox = tkinter.Text(frame3, width = 5, height = 1)
    #whatextbox.insert("end",wha)
    #whatextbox.place(x=310,y=122)
    tkinter.Checkbutton(frame3, text="Enable Haste Compensation", variable=haste_compensation).place(x=0, y = 155)
    tkinter.Checkbutton(frame3, text="Low Performance Haste Compensation", variable=low_performance_haste_compensation).place(x=210, y = 155)
    #dropField = ttk.OptionMenu(frame3, display_type, setdat['display_type'], command = savedisplaytype, *["Built-in retina display","Built-in display"],style='my.TMenubutton' )
    #dropField.place(width=160,x = 100, y = 155,height=24)
    tkinter.Label(frame3, text = "Private Server Link (optional)").place(x = 0, y = 190)
    linktextbox = tkinter.Text(frame3, width = 24, height = 1, bg= wbgc)
    linktextbox.insert("end",private_server_link)
    linktextbox.place(x=190,y=192)
    
    tkinter.Checkbutton(frame3, text="Enable Discord Bot", variable=enable_discord_bot).place(x=0, y = 225)
    tkinter.Label(frame3, text = "Discord Bot Token").place(x = 170, y = 226)
    tokentextbox = tkinter.Text(frame3, width = 24, height = 1, bg= wbgc)
    tokentextbox.insert("end",discord_bot_token)
    tokentextbox.place(x = 300, y=228)
    
    tkinter.Label(frame3, text = "Slot").place(x = 205, y = 120)
    dropField = ttk.OptionMenu(frame3, sprinkler_slot, setdat['sprinkler_slot'], *[x+1 for x in range(6)],style='my.TMenubutton' )
    dropField.place(width=60,x = 245, y = 120,height=24)

    tkinter.Checkbutton(frame3, text="Rejoin every", variable=rejoin_every_enabled).place(x=0, y = 260)
    rejoinetextbox = tkinter.Text(frame3, width = 4, height = 1, bg= wbgc)
    rejoinetextbox.insert("end",rejoin_every)
    rejoinetextbox.place(x=104,y=263)
    tkinter.Label(frame3, text = "hours").place(x = 140, y = 260)

    tkinter.Label(frame3, text = "Wait for").place(x = 0, y = 290)
    rejoindelaytextbox = tkinter.Text(frame3, width = 4, height = 1, bg= wbgc)
    rejoindelaytextbox.insert("end",rejoin_delay)
    rejoindelaytextbox.place(x=55,y=293)
    tkinter.Label(frame3, text = "secs when rejoining").place(x = 90, y = 290)
    
    #Tab 6
    ttk.Button(frame5, text = "Calibrate Hive", command = calibratehive, width = 10).place(x=0,y=13)
    tkinter.Checkbutton(frame5, text="Reverse Hive Direction", variable=reverse_hive_direction).place(x=140, y = 15)
    tkinter.Label(frame5, text = "E Button Detection Type").place(x = 0, y = 50)
    dropField = ttk.OptionMenu(frame5, ebdetect,setdat['ebdetect'], command = disableeb, *["cv2","pyautogui"],style='my.TMenubutton' )
    dropField.place(width=130,x = 158, y = 51,height=24)
    tkinter.Label(frame5, text = " Threshold").place(x = 300, y = 50)
    ebtextbox = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    ebtextbox.insert("end",ebthreshold)
    ebtextbox.place(x=380,y=53)
    tkinter.Label(frame5, text = "Flight Multiplier").place(x = 0, y = 85)
    cttextbox = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    cttextbox.insert("end",canon_time)
    cttextbox.place(x=110,y=88)
    #Root
    ttk.Button(root, text = "Start", command = startGo, width = 7 ).place(x=10,y=360)
    ttk.Button(root, text = "Update",command = updateFiles, width = 9,).place(x=150,y=360)
    ttk.Button(root, text = "Experimental update",command = expu, width = 16,).place(x=300,y=360)
    ttk.Label(root, text = "version {}".format(macrov)).place(x = 630, y = 370)

    disablews("1")
    disabledw()
    disableeb("1")
    root.mainloop()
    


        




