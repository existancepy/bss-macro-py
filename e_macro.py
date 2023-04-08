try:
    import pyautogui as pag
except Exception as e:
    print(e)
    print("\033[0;31mThere is an import error here! This is most likely caused by an incorrect installation process. Ensure that you have done the 'pip3 install...steps'\033[00m")
    quit()
import time, os, ctypes, tty
import tkinter
import tkinter as tk
from tkinter import ttk
import backpack, reset, loadsettings, move,update,updateexperiment
import multiprocessing, webbrowser, imagesearch, sys, discord, subprocess
from webhook import webhook
global savedata
global setdat
from tkinter import messagebox
import numpy as np
import asyncio
from logpy import log
import logging
import pynput
from pynput.keyboard import Key
from pynput.mouse import Button

try:
    import matplotlib.pyplot as plt
except Exception as e:
    print("\033[0;31mThere is an import error here! Enter `pip3 install matplotlib` in terminal'\033[00m")
from PIL import ImageGrab, Image

try:
    import cv2
except Exception as e:
    print(e)
    print("\033[0;31mThere is a import error here! Check out ImportError: dlopen in #common-fixes in the discord server or 'bugs and fixes' section in the github\033[00m")
    quit()

from ocrpy import imToString,customOCR
import sv_ttk
import math
import ast
import calibrate_hive
from datetime import datetime

savedata = {}
ww = ""
wh = ""
ms = pag.size()
mw = ms[0]
mh = ms[1]
stop = 1
setdat = loadsettings.load()
macrov = "1.40.1"
sv_i = sys.version_info
python_ver = '.'.join([str(sv_i[i]) for i in range(0,3)])
planterInfo = loadsettings.planterInfo()
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

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
    rejoinval = multiprocessing.Value('i', 0)
    gather = multiprocessing.Value('i', 0)
    disconnected = multiprocessing.Value('i', 0)
    timeupdate = multiprocessing.Value('i', 0)
    night = manager.Value(ctypes.c_wchar_p, "")

def boolToInt(condition):
    if condition: return 1
    return 0
def is_running(app):
    tmp = os.popen("ps -Af").read()
    return app in tmp[:]
def pagmove(k,t):
    pag.keyDown(k)
    time.sleep(t)
    pag.keyUp(k)
def fullscreen():
    keyboard.press(Key.cmd)
    time.sleep(0.05)
    keyboard.press(Key.ctrl)
    time.sleep(0.05)
    keyboard.press("f")
    time.sleep(0.1)
    keyboard.release(Key.cmd)
    keyboard.release(Key.ctrl)
    keyboard.release("f")
def discord_bot():
    setdat = loadsettings.load()
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('!b'):
            args = message.content.split(" ")[1:]
            cmd = args[0].lower()
            if cmd == "rejoin":
                await message.channel.send("Now attempting to rejoin")
                await asyncRejoin()
            elif cmd == "screenshot":
                await message.channel.send("Sending a screenshot via webhook")
                webhook("User Requested: Screenshot","","light blue",1)
            elif cmd == "report":
                await message.channel.send("Sending Hourly Report")
                hourlyReport(0)
                
                #honeyHist = []
                #savehoney_history(honeyHist)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    client.run(setdat['discord_bot_token'], log_handler=handler)
def setStatus(msg="none"):
    with open("status.txt","w") as f:
        f.write(msg)
    f.close()

def getStatus():
    with open("status.txt","r") as f:
        out = f.read()
    f.close()
    return out
def validateSettings():
    return False
    '''
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
    '''

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



def checkwithOCR(m):
    text = imToString(m).lower()
    if m == "bee bear":
        if "bear" in text:
            return True
    elif m == "egg shop":
        if "bee egg" in text or "basic bee" in text or "small bag" in text or ("blue" in text and "bubble" in text):
            return True
    elif m == "disconnect":
        if "disconnected" in text or "join error" in text:
            setStatus("disconnect")
            webhook("","disconnected","red")
            return True
    elif m == "dialog":
        if "bear" in text:
            return True
    return False
    
def ebutton(pagmode=0):
    ocrval = ''.join([x for x in list(imToString('ebutton').strip()) if x.isalpha()])
    log(ocrval)
    return "E" in ocrval and len(ocrval) <= 3

def detectNight(bypasstime=0):
    savedat = loadRes()
    ww = savedat['ww']
    wh = savedat['wh']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    screen = np.array(pag.screenshot(region=(0,0,round((ww/3.4)*xlm),round((wh/25)*ylm))))
    w,h = screen.shape[:2]
    rgb = screen[0,0][:3]
    if not setdat['stinger']: return False
    if not checkRespawn("night","10m") and not bypasstime:
        return False
    for x in range(w):
        for y in range(h):
            if list(screen[x,y]) == [0,0,0,255]:
                success = True
                for x1 in range(9):
                    for y1 in range(9):
                        if x+x1+1 < w and y1+y+1 < h:
                            if list(screen[x+x1+1,y+y1+1]) != [0,0,0,255]:
                                success = False
                if success:
                    print(x,y)
                    webhook("","Night Detected","dark brown")
                    savetimings("night")
                    return True
    return False

def millify(n):
    if not n: return 0
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def hourlyReport(hourly=1):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    try:
        with open('honey_history.txt','r') as f:
            honeyHist = ast.literal_eval(f.read())
        f.close()
        
        setdat = loadsettings.load()
        log(honeyHist)
        if hourly == 0:
            setdat['prev_honey'] = honeyHist[-1]
        digitCounts = []
        for i, e in enumerate(honeyHist[:]):
            if len(str(e)) <= 4:
                honeyHist.pop(i)
        if honeyHist.count(honeyHist[0]) != len(honeyHist):
            for i, e in reversed(list(enumerate(honeyHist[:]))):
                if e != setdat['prev_honey']:
                    break
                else:
                    honeyHist.pop(i)
        log('prev honey: {}'.format(setdat['prev_honey']))
        log(honeyHist)
        
        while True:
            compList = [x for x in honeyHist if x]
            sortedHoney = sorted(compList)
            if sortedHoney == compList:
                break
            else:
                removeELE = sortedHoney[-1]
                honeyHist.remove(removeELE)
        log(honeyHist)
        currHoney = honeyHist[-1]
        session_honey = currHoney - setdat['start_honey']
        hourly_honey = currHoney - setdat['prev_honey']
        if hourly:
            loadsettings.save('prev_honey',currHoney)
            timehour = int(datetime.now().hour) - 1
        else:
            timehour = int(datetime.now().hour)
            
        stime = time.time() - setdat['start_time']
        day = stime // (24 * 3600)
        stime = stime % (24 * 3600)
        hour = stime // 3600
        stime %= 3600
        minutes = stime // 60
        stime %= 60
        seconds = round(stime)
        session_time = "{}d {}h {}m".format(round(day),round(hour),round(minutes))
        yvals = []
        for i in range(len(honeyHist)):
            if i != 0:
                hf, hb = honeyHist[i], honeyHist[i-1]
                yvals.append(int(hf) - int(hb))
        #yvals = [1,2,3,4,5,6,7,8]
        xvals = [x+1 for x in range(len(yvals))]


        fig = plt.figure(figsize=(12,12), dpi=300,constrained_layout=True)
        gs = fig.add_gridspec(12,12)
        fig.patch.set_facecolor('#121212')

        axText = fig.add_subplot(gs[0:12, 8:12])
        axText.get_xaxis().set_visible(False)
        axText.get_yaxis().set_visible(False)
        axText.patch.set_facecolor('#121212')
        axText.spines['bottom'].set_color('#121212')
        axText.spines['top'].set_color('#121212')
        axText.spines['left'].set_color('#121212')
        axText.spines['right'].set_color('#121212')

        plt.text(0.3,1,"Report", fontsize=20,color="white")
        plt.text(0,0.95,"Session Time: {}".format(session_time), fontsize=15,color="white")
        plt.text(0,0.9,"Current Honey: {}".format(millify(currHoney)), fontsize=15,color="white")
        plt.text(0,0.85,"Session Honey: {}".format(millify(session_honey)), fontsize=15,color="white")
        plt.text(0,0.8,"Honey/Hr: {}".format(millify(hourly_honey)), fontsize=15,color="white")

        ax1 = fig.add_subplot(gs[0:3, 0:7])
        if not yvals:
            yvals = honeyHist.copy()
        if max(yvals) == 0:
            yticks = [0]
        else:
            yticks = np.arange(0, max(yvals)+1, max(yvals)/4)
        yticksDisplay = [millify(x) if x else x for x in yticks]

        xticks = np.arange(0,max(xvals)+1, 10)
        xticksDisplay = ["{}:{}".format(timehour,x) if x else "{}:00".format(timehour) for x in xticks]

        ax1.set_yticks(yticks,yticksDisplay,fontsize=16)
        ax1.set_xticks(xticks,xticksDisplay,fontsize=16)
        ax1.set_title('Honey/min',color='white',fontsize=19)
        ax1.patch.set_facecolor('#121212')
        ax1.spines['bottom'].set_color('white')
        ax1.spines['top'].set_color('white')
        ax1.spines['left'].set_color('white')
        ax1.spines['right'].set_color('white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.plot(xvals, yvals,color="#BB86FC")
        
        
        buffim = pag.screenshot(region = (0,wh/(30*ysm),ww/2,wh/(16*ylm)))
        buffim.save("buffs.png")
        buffim = plt.imread('buffs.png')
        ax2 = fig.add_subplot(gs[4:6, 0:7])
        ax2.set_title('Buffs',color='white',fontsize=19)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        ax2.patch.set_facecolor('#121212')
        ax2.imshow(buffim)
        
        plt.grid(alpha=0.08)
        plt.savefig("hourlyReport-resized.png", bbox_inches='tight')    
        webhook("**Hourly Report**","","light blue",0,1)
    except Exception as e:
        log(e)
        print(e)
        webhook("","Hourly Report has an error that has been caught. The error can be found in macroLogs.log","red")


        



def canon(fast=0):
    savedata = loadRes()
    setdat = loadsettings.load()
    ww = savedata['ww']
    wh = savedata['wh']
    for i in range(4):
        if checkwithOCR("disconnect"):
            return "dc"
        #Move to canon:
        if not fast: webhook("","Moving to canon","dark brown")
        move.apkey("space")
        time.sleep(1)
        move.hold("w",0.8)
        move.hold("d",0.9*(setdat["hive_number"])+1)
        pag.keyDown("d")
        time.sleep(0.5)
        move.press("space")
        time.sleep(0.2)
        r = ""
        pag.keyUp("d")
        if fast:
            move.hold("d",0.9)
            time.sleep(0.1)
            return
        move.hold("d",0.3)
        for _ in range(4):
            move.hold("d",0.2)
            time.sleep(0.05)
            r = ebutton()
            if r:
                if checkwithOCR('bee bear'):
                    webhook("","Bee Bear detected","dark brown")
                    break
                else:
                    webhook("","Canon found","dark brown")
                    with open('canonfails.txt', 'w') as f:
                        f.write('0')
                    f.close()
                    return
        mouse.position = (mw//2,mh//5*4)
        reset.reset()
    else:
        webhook("","Canon failed too many times, rejoining", "red")
        setStatus("disconnect")
        time.sleep(1)
        return "dc"
    '''
        for _ in range(20):
            mouse.press()
            sleep(0.25)
            mouse.release()
    '''
        

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
    setdat = loadsettings.load()
    r = False
    for _ in range(2):
        r = ebutton()
        if r: break
        time.sleep(0.25)
    if not r: return
    move.press("e")
    if setdat['stinger']:
        move.press(",")
    webhook("","Starting convert","brown",1)
    st = time.perf_counter()
    while True:
        sh = stingerHunt(1,1)
        if sh == "dc" or sh == "success":
            break
        c = ebutton()
        if not c:
            webhook("","Convert done","brown")
            time.sleep(2)
            break
        if time.perf_counter()  - st > 600:
            webhook("","Converting took too long, moving on","brown")
            break
        
def walk_to_hive(gfid):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    webhook("","Going back to hive: {}".format(setdat['gather_field'][gfid]),"dark brown")
    exec(open("walk_{}.py".format(setdat['gather_field'][gfid])).read())
    for _ in range(30):
        pag.keyDown("a")
        time.sleep(0.15)
        pag.keyUp("a")
        r = ebutton()
        if r:
            if checkwithOCR('bee bear'):
                break
            else:
                convert()
                reset.reset()
                return
        
    webhook("","Cant find hive, resetting","dark brown",1)
    reset.reset()
    convert()
def checkRespawn(m,t):
    timing = float(loadtimings()[m])
    respt = int(''.join([x for x in list(t) if x.isdigit()]))
    if t[-1] == 'h':
        respt = respt*60*60
    else:
        respt = respt*60
    collectList = [x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("collect_")]
    collectList+=["mondo_buff","night"]
    if setdat['gifted_vicious_bee'] and m not in collectList:
        respt = respt/100*85
    if time.time() - timing > respt:
        return True
    return False

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
        pagmove("w", 0.72*f)
        pagmove("a", 0.1*s)
        pagmove("s", 0.72*f)
        pagmove("a", 0.1*s)
    for i in range(2):
        pagmove("w", 0.72*f)
        pagmove("d", 0.1*s)
        pagmove("s", 0.72*f)
        pagmove("d", 0.1*s)
    
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
def stingerHunt(convert=0,gathering=0):
    setdat = loadsettings.load()
    fields = ['pepper','mountain top','rose','cactus','spider','clover']
    if checkwithOCR("disconnect"):
        time.sleep(1)
        return "dc"
    if setdat['rejoin_every_enabled']:
        with open('timings.txt', 'r') as f:
            prevTime = float([x for x in f.read().split('\n') if x.startswith('rejoin_every')][0].split(":")[1])
        log("{}, {}".format((time.time() - prevTime)/3600, setdat['rejoin_every']))
        if (time.time() - prevTime)/3600 > setdat['rejoin_every']:
            setStatus("disconnect")
            time.sleep(1)
            return "dc"
    status = getStatus()         
    if status != "night": return False
    if convert:
        move.press(".")
    if gathering: reset.reset()
    for field in fields:
        status = getStatus()
        fieldGoTo = field
        killvb = 0
        if not "vb_found" in status: #Status might update after resetting
            if canon(1) == "dc": return "dc"
            exec(open("field_{}.py".format(field)).read())
            webhook("","Finding Vicious Bee ({})".format(field),"dark brown")
            setStatus("finding_vb_{}".format(field))
            exec(open("vb_{}.py".format(field)).read())
            status = getStatus()
        else:
            fi = fields.index(field)
            if fi > 0:
                prev_field = fields[fi-1]
            else:
                prev_field = fields[fi]
            status = "vb_found_wrong_field_{}".format(prev_field)
        print(status)
        if "vb_found_right_field" in status:
            killvb = 1
        elif "vb_found_wrong_field" in status:
            reset.reset()
            if canon(1) == "dc": return "dc"
            fieldGoTo = status.split("_")[-1]
            exec(open("field_{}.py".format(fieldGoTo)).read())
            exec(open("vb_{}.py".format(fieldGoTo)).read())
            killvb = 1
        if killvb:
            setStatus("killing_vb")
            st = time.time()
            while True:
                exec(open("killvb_{}.py".format(fieldGoTo)).read())
                status = getStatus()
                if status == "vb_killed":
                    webhook("","Vicious Bee Killed","bright green")
                    break
                if time.time()-st > 300:
                    webhook("","Took too long to kill vicious bee, leaving","red")
                    break
                if status == "killing_vb_died":
                    reset.reset()
                    if canon(1) == "dc": return "dc"
                    fieldGoTo = status.split("_")[4]
                    exec(open("field_{}.py".format(fieldGoTo)).read())
                    setStatus("killing_vb")
            reset.reset()
            break
        reset.reset()
    setStatus("none")
    return "success"
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
    log(planterSlot)
    if checkwithOCR("disconnect"):
        return
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
        mouse.click(27,102)
        mouse.click(Button.left, 2)
    savePlanterTimings(planter)
    webhook("","Placed Planter: {}".format(displayPlanterName(planter)),"bright green",1)
    reset.reset()


urows,ucols = cv2.imread('./images/retina/yes.png').shape[:2]
def clickYes():
    res = loadRes()
    ww = res['ww']
    wh = res['wh']
    setdat = loadsettings.load()
    a = imagesearch.find("yes.png",0.2,0,0,ww,wh)
    if setdat['display_type'] == "built-in retina display":
        if a:
            mouse.position = (a[1]//2+urows//4,a[2]//2+ucols//4)
            mouse.click(Button.left, 1)
        else:
            mouse.position = (ww//4-70,wh//3.2)
            mouse.click(Button.left, 1)
    else:
        if a:
            mouse.position = (a[1]+urows//2,a[2]+ucols//2)
            mouse.click(Button.left, 1)
        else:
            mouse.position= (ww//2-50,wh//1.6)
            mouse.click(Button.left, 1)
            
    
def goToPlanter(field,place=0):
    if canon() == "dc": return
    exec(open("field_{}.py".format(field)).read())
    if field == "pine tree":
        move.hold("d",3)
        move.hold("s",4)
        move.hold("w",0.25)
    elif field == "pumpkin":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        move.hold("s",0.25)
    elif field  == "strawberry":
        move.hold("d",3)
        move.hold("s",4)
    elif field == "bamboo":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        move.hold("s",0.25)
    elif field  == "pineapple":
        move.hold("d",3)
        move.hold("s",4)
    elif field == "mushroom":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        move.hold("s",0.25)
    elif field == "coconut":
        move.hold("d",5)
        move.hold("s")
    else:
        time.sleep(0.8)
    time.sleep(0.2)
        
def fieldDriftCompensation():
    res = loadRes()
    ww = res["ww"]
    wh = res["wh"]
    winUp = wh/2.1
    winDown = wh/1.8
    winLeft = ww/2.05
    winRight = ww/1.8
    for _ in range(4):
        screen = np.array(ImageGrab.grab())
        screen = cv2.cvtColor(src=screen, code=cv2.COLOR_BGR2RGB)
        large_image = screen
        result = cv2.matchTemplate(sat_image, large_image, method)
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        x,y = mnLoc
        if mn < 0.075:
            if x >= winLeft and x <= winRight and y >= winUp and y <= winDown: break
            if x < winLeft:
                move.hold("a",0.32)
            elif x > winRight:
                move.hold("d",0.32)
            if y < winUp:
                move.hold("w",0.32)
            elif y > winDown:
                move.hold("s",0.32)
        else:
            break

def savehoney_history(saveinfo):
    with open("honey_history.txt","w") as f:
        f.write(str(saveinfo))
    f.close()
    
def hastecompbg():
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    print("hastecomp activated")
    while True:
        getHaste()

def vic():
    fields = ['pepper','mountain','rose','cactus','spider','clover']
    prevHour = datetime.now().hour
    prevMin = datetime.now().minute
    invalid_prev_honey = 1
    honeyHist = [0]*60
    while True:
        status = getStatus()
        
        #r = imagesearch.find('disconnect.png',0.7,ww//3,wh//2.8,ww//2.3,wh//2.5)
        
        if "vb" in status:
            bluetexts = imToString("blue").lower()
            print(bluetexts)
            if "finding_vb" in status and "vicious" in bluetexts and "attack" in bluetexts:
                currField = status.split("_")[2]
                targetField = "none"
                for fd in fields:
                    if fd in bluetexts:
                        if fd == "mountain":
                            targetField = "mountain top"
                        else:
                            targetField = fd
                        break
                webhook("","Found Vicious Bee In {} Field".format(fd.title()),"light green")
                if currField.lower() == targetField.lower():
                    setStatus("vb_found_right_field")
                else:
                    setStatus("vb_found_wrong_field_{}".format(targetField))
            elif "killing_vb" in status:
                if "vicious" in bluetexts and "defeated" in bluetexts:
                    setStatus("vb_killed")
                elif "died" in bluetexts:
                    setStatus("killing_vb_died")
        else:
            if setdat['stinger']:
                if detectNight():
                    setStatus("night")
            if setdat['enable_discord_webhook'] and setdat['send_screenshot']:
                sysTime = datetime.now()
                sysHour = sysTime.hour
                sysMin = sysTime.minute
                if sysMin != prevMin:
                    prevMin = sysMin
                    ch = imToString('honey')
                    if invalid_prev_honey and ch:
                        invalid_prev_honey = 0
                        honeyHist = [ch]*60
                        loadsettings.save("prev_honey",ch)
                        webhook("","First Honey detected: {}".format(millify(ch)),"light blue")
                    else:
                        if ch:
                            honeyHist[sysMin] = int(ch)
                        else:
                            honeyHist[sysMin] = honeyHist[sysMin-1]
                            print("failed to detect honey")
                    log(ch)
                    savehoney_history(honeyHist)
                if sysMin == 0 and sysHour != prevHour:
                    
                    hourlyReport()
                    prev_honey = loadsettings.load()['prev_honey']
                    honeyHist = [prev_honey]*60
                    prevHour = sysHour
        
def killMob(field,mob,reset):
    webhook("","Traveling: {} ({})".format(mob.title(),field.title()),"dark brown")
    convert()
    if canon() == "dc": return
    time.sleep(1)
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
        if canon() == "dc": return
        webhook("","Traveling: {}".format(dispname),"dark brown")
        exec(open("collect_{}.py".format(usename)).read())
        if usename == "wealthclock" or usename == "samovar":
            for _ in range(6):
                move.hold("w",0.2)
                if ebutton():
                    break
        elif usename == "candles":
            for _ in range(7):
                    move.hold("w",0.2)
                    if ebutton():
                        break
        elif usename == "lid_art" or usename == "feast":
            for _ in range(7):
                move.hold("s",0.2)
                if ebutton():
                    break
        elif usename == "gluedispenser":
            time.sleep(1)
            move.press(str(setdat['gumdrop_slot']))
            time.sleep(2)
            move.hold("w",2.5)
        time.sleep(0.5)
        if usename == "feast":
            if checkwithOCR("bee bear"):
                pag.keyDown("w")
                time.sleep(1)
                move.apkey("space")
                time.sleep(1.5)
                pag.keyUp("w")
        for _ in range(2):
            if ebutton():
                webhook("","Collected: {}".format(dispname),"bright green",1)
                claimLoot =  1
                break
        if claimLoot: break
        webhook("","Unable To Collect: {}".format(dispname),"dark brown",1)
        reset.reset()
    savetimings(usename)
    move.press('e')
    time.sleep(0.5)
    if claimLoot and beesmas:
        if name != "stockings":
            sleep(4)
        move.apkey("space")
        exec(open("claim_{}.py".format(usename)).read())
    reset.reset()
def rawreset(nowait=0):
    pag.press('esc')
    time.sleep(0.1)
    pag.press('r')
    time.sleep(0.2)
    pag.press('enter')
    if nowait: return
    time.sleep(8) 
def updateHive(h):
    global setdat
    webhook("","Found Hive: {}".format(h),"bright green")
    loadsettings.save('hive_number',h)

def openSettings():
    savedat = loadRes()
    mw, mh = pag.size()
    ww = savedat['ww']
    wh = savedat['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    webhook('','Opening Stats',"brown")
    promoCode = ''.join([x[1][0] for x in customOCR(0,wh/7,ww/3,wh/8)]).lower()
    pag.typewrite("\\")
    if not "code" in promoCode:
        for _ in range(5):
            keyboard.press(Key.up)
            time.sleep(0.05)
            keyboard.release(Key.up)
            time.sleep(0.1)
        keyboard.press(Key.down)
        time.sleep(0.05)
        keyboard.release(Key.down)
        for _ in range(9):
            keyboard.press(Key.left)
            time.sleep(0.05)
            keyboard.release(Key.left)
        for _ in range(4):
            keyboard.press(Key.right)
            time.sleep(0.05)
            keyboard.release(Key.right)
        move.press('enter')
        promoCode = ''.join([x[1][0] for x in customOCR(0,wh/7,ww/3,wh/8)]).lower()
        if not "code" in promoCode:
            move.press('enter')
    keyboard.press(Key.down)
    time.sleep(0.05)
    keyboard.release(Key.down)
    for _ in range(24):
        keyboard.press(Key.page_down)
        time.sleep(0.02)
        keyboard.release(Key.page_down)
    time.sleep(0.5)
    for _ in range(3):
        keyboard.press(Key.page_up)
        time.sleep(0.02)
        keyboard.release(Key.page_up)
    pag.scroll(100)
    for _ in range(5):
        statData = customOCR(0,wh/7,ww/7,wh/2)
        statNames = ''.join([x[1][0] for x in statData]).lower()
        print(statNames)
        if 'speed'in statNames:
            pag.typewrite("\\")
            break
        keyboard.press(Key.page_up)
        time.sleep(0.02)
        keyboard.release(Key.page_up)
    else:
        pag.typewrite("\\")
        webhook("","Unable to locate the walkspeed stat, haste compensation is disabled","red")
        loadsettings.save("msh",-1,"multipliers.txt")
        loadsettings.save("msy",-1,"multipliers.txt")
        return
    time.sleep(0.3)
    check = customOCR(0,0,ww/7,wh)
    for i, e in enumerate(check):
        if 'speed' in e[1][0]:
            movespeedInfo = e
    print(movespeedInfo)
    coords = movespeedInfo[0]
    start,_,end,_ = coords
    x,y, = start[0],start[1]-20
    h = end[1] - y+20
    
    im = pag.screenshot(region=(ww/8,y,ww/10,h))
    im.save('test.png')
    loadsettings.save("msh",h,"multipliers.txt")
    loadsettings.save("msy",y,"multipliers.txt")


def getHaste():
    setdat = loadsettings.load()
    ws = float(setdat['walkspeed'])
    mp  = loadsettings.load('multipliers.txt')
    #print(mp)
    msh = mp['msh']
    msy = mp['msy']
    ww = loadRes()['ww']
    if str(msh) == "-1": return
    if tesseract:
        st = time.time()
        image = np.array(pag.screenshot(region=(ww/8,msy,ww/10,msh)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #gray = cv2.medianBlur(gray, 3)
        ocr = pytesseract.image_to_string(gray)
        print(time.time()-st)
        print(ocr)
    else:
        ocr = customOCR(ww/8,msy,ww/10,msh,0)
    if not ocr:return
    filtered = [x for x in ocr if "." in x[1][0] or x[1][0].replace("_","").replace(" ","").isdigit()]
    
    if not filtered:return
    text = filtered[0][1][0].replace(" ","")
    if not text:return
    num = ""
    currms = ws
    for i in text:
        if i == "." or i.isdigit():
            num += i
    print(num)
    try:
        num = float(num)
        if num > ws:
            with open("haste.txt","w") as f:
                f.write(str(num))
            f.close()
            return
    except Exception as e:
        #print(e)
        pass
    with open("haste.txt","w") as f:
        f.write(str(ws))
    f.close()
    
async def asyncRejoin():
    setdat = loadsettings.load()
    for i in range(2):
        cmd = """
            osascript -e 'tell application "Roblox" to quit' 
            """
        os.system(cmd)
        savedata = loadRes()
        ww = savedata['ww']
        wh = savedata['wh']
        webhook("","Rejoining","dark brown")
        await asyncio.sleep(5)
        if is_running("roblox"):
                cmd = """
                    osascript -e 'tell application "Roblox" to quit' 
                    """
                os.system(cmd)
                await asyncio.sleep(3)
        link  = ""
        if setdat["private_server_link"]:
            link = setdat['private_server_link']
        else:
            link = 'https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129'
        rm = loadsettings.load()['rejoin_method']
        if rm == "new tab":
            webbrowser.open("https://docs.python.org/3/library/webbrowser.html", autoraise=True)
            await asyncio.sleep(1)
            with keyboard.pressed(Key.cmd):
                keyboard.press('t')
                keyboard.release('t')
            keyboard.type(link)
            keyboard.press(Key.enter)
        else:
            webbrowser.open(link)
        if not setdat['private_server_link']:
            await asyncio.sleep(10)
        await asyncio.sleep(setdat['rejoin_delay']*(i+1))
        cmd = """
            osascript -e 'activate application "Roblox"' 
        """
        os.system(cmd)
        
        await asyncio.sleep(0.5)
        keyboard.press(Key.cmd)
        await asyncio.sleep(0.05)
        keyboard.press(Key.ctrl)
        await asyncio.sleep(0.05)
        keyboard.press("f")
        await asyncio.sleep(0.1)
        keyboard.release(Key.cmd)
        keyboard.release(Key.ctrl)
        keyboard.release("f")
        
        await asyncio.sleep(2)
        pag.keyDown("w")
        await asyncio.sleep(5)
        pag.keyUp("w")
        pag.keyDown("s")
        await asyncio.sleep(0.55)
        pag.keyUp("s")
        foundHive = 0
        move.apkey('space')
        await asyncio.sleep(0.5)
        webhook("","Finding Hive", "dark brown",1)
        if setdat['hive_number'] == 3:
            if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found: 3","dark brown",1)
                break
        elif setdat['hive_number'] == 2:
            pag.keyDown("d")
            await asyncio.sleep(0.8)
            pag.keyUp("d")
            for _ in range(4):
                pag.keyDown("d")
                await asyncio.sleep(0.1)
                pag.keyUp("d")
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 2","dark brown",1)
                    break
        elif setdat['hive_number'] == 1:
            pag.keyDown("d")
            await asyncio.sleep(2)
            pag.keyUp("d")
            for _ in range(4):
                pag.keyDown("d")
                await asyncio.sleep(0.1)
                pag.keyUp("d")
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 1","dark brown",1)
                    break
        elif setdat['hive_number'] == 4:
            pag.keyDown("a")
            await asyncio.sleep(0.4)
            pag.keyUp("a")
            for _ in range(4):
                pag.keyDown("a")
                await asyncio.sleep(0.1)
                pag.keyUp("a")
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 4","dark brown",1)
                    break
        elif setdat['hive_number'] == 5:
            pag.keyDown("a")
            await asyncio.sleep(1.7)
            pag.keyUp("a")
            for _ in range(4):
                pag.keyDown("a")
                await asyncio.sleep(0.1)
                pag.keyUp("a")
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 5","dark brown",1)
                    break
        else:
            pag.keyDown("a")
            await asyncio.sleep(3.3)
            pag.keyUp("a")
            if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 6","dark brown",1)
                    break
        while True:   
            if not foundHive:
                pag.keyDown("d")
                await asyncio.sleep(12)
                pag.keyUp("d")
                webhook("","Hive already claimed, finding new hive","dark brown",1)
                pag.keyDown("a")
                await asyncio.sleep(0.2)
                pag.keyUp("a")
                for _ in range(3):
                    pag.keyDown("a")
                    await asyncio.sleep(0.1)
                    pag.keyUp("a")
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(1)
                        break
                if foundHive: break
                pag.keyDown("a")
                await asyncio.sleep(0.4)
                pag.keyUp("a")
                for _ in range(3):
                    pag.keyDown("a")
                    await asyncio.sleep(0.1)
                    pag.keyUp("a")
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(2)
                        break
                if foundHive: break
                pag.keyDown("a")
                await asyncio.sleep(0.5)
                pag.keyUp("a")
                for _ in range(3):
                    pag.keyDown("a")
                    await asyncio.sleep(0.1)
                    pag.keyUp("a")
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(3)
                        break
                if foundHive: break
                pag.keyDown("a")
                await asyncio.sleep(0.7)
                pag.keyUp("a")
                for _ in range(3):
                    pag.keyDown("a")
                    await asyncio.sleep(0.1)
                    pag.keyUp("a")
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(4)
                        break
                if foundHive: break
                pag.keyDown("a")
                await asyncio.sleep(0.7)
                pag.keyUp("a")
                for _ in range(3):
                    pag.keyDown("a")
                    await asyncio.sleep(0.1)
                    pag.keyUp("a")
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(5)
                        break
                if foundHive: break
                move.hold('a',0.7)
                for _ in range(3):
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(6)
                        break
                break
            else: break
        if not foundHive:
            rawreset()
            webhook("","Unable to claim hive, using final resort method","dark brown",1)
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
        resetCheck = 0
        ths = loadsettings.load()["hivethreshold"]
        loadSave()
        ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
        xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
        for _ in range(2):
            webhook("","Reset Check","dark brown")
            mouse.position = (mw/(4.11*xsm),mh/(9*ysm))
            ww = savedata["ww"]
            wh = savedata["wh"]
            xo = ww//4
            yo = wh//100*90
            xt = xo*2
            yt = wh//100*20
            await asyncio.sleep(2)
            pag.press('esc')
            await asyncio.sleep(0.1)
            pag.press('r')
            await asyncio.sleep(0.2)
            pag.press('enter')
            await asyncio.sleep(8)
            for _ in range(4):
                pag.press('pgup')
            await asyncio.sleep(0.1)
            for _ in range(6):
                pag.press('o')
            #im = pag.screenshot(region = (xo,yo,xt,yt))
            #im.save('a.png')

            await asyncio.sleep(0.4)
            for _ in range(4):
                r = imagesearch.find("hive1.png",ths, xo, yo, xt, yt)
                if r:
                    await asyncio.sleep(0.1)
                    for _ in range(4):
                        pag.press(".")

                    await asyncio.sleep(0.1)
                    for _ in range(4):
                        pag.press('pgdn')
                    resetCheck = 1
                    break
                for _ in range(4):
                    pag.press(",")
                    
                await asyncio.sleep(0.5)
            await asyncio.sleep(1)
        for _ in range(4):
            pag.press(",")
        webhook("Notice","Hive not found.","red",1)
        if resetCheck:
            webhook("","Rejoin successful","dark brown")
            break
        webhook("",'Rejoin unsuccessful, attempt 2','dark brown')
    

def openRoblox(link):
    rm = loadsettings.load()['rejoin_method']
    if rm == "new tab":
        webbrowser.open(link)
    else:
        webbrowser.open("https://docs.python.org/3/library/webbrowser.html", autoraise=True)
        time.sleep(3)
        with keyboard.pressed(Key.cmd):
            keyboard.press('t')
            keyboard.release('t')
        time.sleep(1)
        keyboard.type(link)
        time.sleep(0.5)
        keyboard.press(Key.enter)
    
def rejoin():
    setdat = loadsettings.load()
    for i in range(3):
        cmd = """
            osascript -e 'tell application "Roblox" to quit' 
            """
        os.system(cmd)
        savedata = loadRes()
        ww = savedata['ww']
        wh = savedata['wh']
        webhook("","Rejoining","dark brown",1)
        time.sleep(3)
        if is_running("roblox"):
                cmd = """
                    osascript -e 'tell application "Roblox" to quit' 
                    """
                os.system(cmd)
                time.sleep(3)
        if setdat["private_server_link"]:
            openRoblox(setdat["private_server_link"])
        else:
            openRoblox('https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129')
            time.sleep(10)
                
        time.sleep(setdat['rejoin_delay']*(i+1))
        cmd = """
            osascript -e 'activate application "Roblox"' 
        """
        
        os.system(cmd)
        time.sleep(1)
        if setdat['manual_fullscreen']:
            fullscreen()
        time.sleep(2)
        move.hold("w",5,0)
        move.hold("w",i*2,0)
        move.hold("s",0.6,0)
        foundHive = 0
        move.apkey('space')
        time.sleep(0.5)
        webhook("","Finding Hive", "dark brown",1)
        if setdat['hive_number'] == 3:
            if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found: 3","dark brown",1)
                break
        elif setdat['hive_number'] == 2:
            move.hold('d',1,0)
            for _ in range(4):
                move.hold('d',0.1)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 2","dark brown",1)
                    break
        elif setdat['hive_number'] == 1:
            move.hold('d',2,0)
            for _ in range(4):
                move.hold('d',0.1,0)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 1","dark brown",1)
                    break
        elif setdat['hive_number'] == 4:
            move.hold('a',0.6,0)
            for _ in range(4):
                move.hold('a',0.1,0)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 4","dark brown",1)
                    break
        elif setdat['hive_number'] == 5:
            move.hold('a',1.9,0)
            for _ in range(4):
                move.hold('a',0.1,0)
                if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 5","dark brown",1)
                    break
        else:
            move.hold('a',3.3,0)
            if ebutton():
                    move.press('e')
                    foundHive = 1
                    webhook("","Hive Found: 6","dark brown",1)
                    break
        while True:   
            if not foundHive:
                move.hold("d",12,0)
                webhook("","Hive already claimed, finding new hive","dark brown",1)
                move.hold('a',0.2)
                for _ in range(3):
                    move.hold('a',0.1,0)
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(1)
                        break
                if foundHive: break
                move.hold('a',0.9,0)
                for _ in range(3):
                    move.hold('a',0.1,0)
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(2)
                        break
                if foundHive: break
                move.hold("a",0.9,0)
                for _ in range(3):
                    move.hold('a',0.1,0)
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(3)
                        break
                if foundHive: break
                move.hold('a',0.8,0)
                for _ in range(3):
                    move.hold('a',0.1,0)
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(4)
                        break
                if foundHive: break
                move.hold('a',0.9,0)
                for _ in range(3):
                    move.hold('a',0.1,0)
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(5)
                        break
                if foundHive: break
                move.hold('a',0.9,0)
                for _ in range(3):
                    move.hold('a',0.1,0)
                    if ebutton():
                        move.press('e')
                        foundHive = 1
                        updateHive(6)
                        break
                break
            else: break
        if not foundHive:
            rawreset()
            webhook("","Unable to claim hive, using final resort method","dark brown",1)
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
        if setdat['haste_compensation']: openSettings()
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
            
    
def gather(gfid):
    if str(gfid).isdigit():
        gfid = int(gfid)
        setdat = loadsettings.load()
    else:
        gfid = str(gfid)
    canon()
    webhook("","Traveling: {}".format(setdat['gather_field'][gfid]),"dark brown")
    exec(open("field_{}.py".format(setdat['gather_field'][gfid])).read())
    cf = setdat['gather_field'][gfid].replace(" ","").lower()
    time.sleep(0.2)
    s_l = setdat['start_location'][gfid].lower()
    rotTowards = []
    rotBack = []
    if s_l != 'center':
        if s_l == "upper right":
            rotTowards = ["."]
        elif s_l == "right":
            rotTowards = ["."]*2
        elif s_l == "lower right":
            rotTowards = ["."]*3
        elif s_l == "bottom":
            rotTowards = ["."]*4
        elif s_l == "lower left":
            rotTowards = [","]*3
        elif s_l == "left":
            rotTowards = [","]*2
        elif s_l == "upper left":
            rotTowards = [","]
        for i in rotTowards:
            move.press(i)
            if i == ".":
                rotBack.append(",")
            elif i:
                rotBack.append(".")
        
        move.hold("w",setdat['distance_from_center'][gfid]/2.5)
        
        for i in rotBack:
            move.press(i)

    print(setdat["before_gather_turn"][gfid])
       
    if setdat["before_gather_turn"][gfid] == "left":
        for _ in range(setdat["turn_times"][gfid]):
            move.press(",")
    elif setdat["before_gather_turn"][gfid] == "right":
        for _ in range(setdat["turn_times"][gfid]):
            move.press(".")
    
    time.sleep(0.2)
    placeSprinkler()
    pag.click()
    gp = setdat["gather_pattern"][gfid].lower()
    webhook("Gathering: {}".format(setdat['gather_field'][gfid]),"Limit: {}.00 - {} - Backpack: {}%".format(setdat["gather_time"][gfid],setdat["gather_pattern"][gfid],setdat["pack"][gfid]),"light green")
    time.sleep(0.2)
    timestart = time.perf_counter()
    fullTime = 0
    stingerFound = 0
    while True:
        time.sleep(0.05)
        mouse.press(Button.left)
        time.sleep(0.05)
        exec(open("gather_{}.py".format(gp)).read())
        bpcap = backpack.bpc()
        resetMobTimer(cf.lower())
        timespent = (time.perf_counter() - timestart)/60
        if bpcap >= setdat["pack"][gfid]:
            webhook("Gathering: ended","Time: {:.2f} - Backpack - Return: {}".format(timespent, setdat["return_to_hive"][gfid]),"light green")
            break
            
        if timespent > setdat["gather_time"][gfid]:
            webhook("Gathering: ended","Time: {:.2f} - Time Limit - Return: {}".format(timespent, setdat["return_to_hive"][gfid]),"light green")
            break
        if setdat['field_drift_compensation'][gfid] and gp != "stationary":
            fieldDriftCompensation()
        shv = stingerHunt(0,1)
        if  shv == "success":
            stingerFound = 1
            break
        elif shv == "dc":
            return
            
        mouse.release(Button.left)
    time.sleep(0.5)
    if not stingerFound:
        if setdat["before_gather_turn"][gfid] == "left":
            for _ in range(setdat["turn_times"][gfid]):
                move.press(".")
        elif setdat["before_gather_turn"][gfid] == "right":
            for _ in range(setdat["turn_times"][gfid]):
                move.press(",")
                
        if setdat['return_to_hive'][gfid] == "walk":
            walk_to_hive(gfid)
        elif setdat['return_to_hive'][gfid] == "reset":
            reset.reset()
            convert()
        elif setdat['return_to_hive'][gfid] == "rejoin":
            rejoin()
            reset.reset()
        elif setdat['return_to_hive'][gfid] == "whirligig":
            webhook("","Activating whirligig","dark brown")
            if setdat['whirligig_slot'][gfid] == "none":
                webhook("Notice","Whirligig option selected but no whirligig slot given, walking back","red")
                walk_to_hive(gfid)
            else:
                move.press(str(setdat['whirligig_slot'][gfid]))
                time.sleep(1)
                r = 0
                for _ in range(2):
                    re = ebutton()
                    if re:
                        r = 1
                if r:
                    convert()
                    reset.reset()
                else:
                    webhook("Notice","Whirligig failed to activate, walking back","red")
                    walk_to_hive()

def placeSprinkler():
    sprinklerCount = {
        "basic":1,
        "silver":2,
        "golden":3,
        "diamond":4,
        "saturator":1

        }
    setdat = loadsettings.load()
    times = sprinklerCount[setdat['sprinkler_type']]
    if times == 1:
        move.press(str(setdat['sprinkler_slot']))
        keyboard.press(Key.space)
        time.sleep(0.1)
        keyboard.release(Key.space)
    else:
        keyboard.press(Key.space)
        st = time.time()
        while True:
            if time.time() - st > times*2:
                break
            else:
                move.press(str(setdat['sprinkler_slot']))
        keyboard.release(Key.space)
        
def startLoop(planterTypes_prev, planterFields_prev,session_start):
    global invalid_prev_honey
    setStatus()
    setdat = loadsettings.load()   
    val = validateSettings()
    setStatus()
    with open('canonfails.txt', 'w') as f:
        f.write('0')
    f.close()
    if val:
        pag.alert(text='Your settings are incorrect! Check the terminal to see what is wrong.', title='Invalid settings', button='OK')
        print(val)
        sys.exit()
    cmd = """
            osascript -e 'activate application "Roblox"' 
        """
    savetimings('rejoin_every')
    os.system(cmd)
    continuePlanters = 1
    with open('firstRun.txt', 'r') as f:
        if int(f.read()) == 1:
            continuePlanters = 0
    f.close()
    with open('firstRun.txt', 'w') as f:
        f.write("0")
    f.close()
    invalid_prev_honey = 0
    if session_start:
        log("Session Start")
        if setdat['haste_compensation']:
            rawreset(1)
            openSettings()
        else: rawreset()
        currHoney = imToString('honey')
        loadsettings.save('start_honey',currHoney)
        loadsettings.save('prev_honey',currHoney)
        if honeyHist[0] == 0:
            invalid_prev_honey = 1
    reset.reset()
    convert()
    savedata = loadRes()
    planterset = loadsettings.planterLoad()
    ww = savedata['ww']
    wh = savedata['wh']
    gfid = 0
    if planterset['enable_planters']:
        with open("planterdata.txt","r") as f:
            lines = f.read().split("\n")
        f.close()
        occupiedStuff = ast.literal_eval(lines[0])
        print(occupiedStuff)
        planterTypes = ast.literal_eval(lines[1])
        planterFields = ast.literal_eval(lines[2])
        #if planterTypes == planterTypes_prev and planterFields == planterFields_prev:
            #continuePlanters = 1
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
        #Stump snail check
        if setdat['stump_snail'] and checkRespawn("stump_snail","96h"):
            canon()
            webhook("","Traveling: Stump snail (stump) ","brown")
            exec(open("field_stump.py").read())
            time.sleep(0.2)
            placeSprinkler()
            pag.click()
            webhook("","Starting stump snail","brown")
            while True:
                time.sleep(10)
                pag.click()
                if checkwithOCR("disconnect"):
                    return
                if imagesearch.find("keepold.png",0.9):
                    savetimings("stump_snail")
                    if setdat['continue_after_stump_snail']:break
            webhook("","Stump snail killed, keeping amulet","bright green")
            mouse.move(mw//2-30,mh//100*60)
            pag.click()
            reset.reset()
            
        #Collect check
        stingerHunt()
        if getStatus() == "disconnect":
            print("aaaa")
            return
        
        if setdat['wealthclock']  and checkRespawn('wealthclock',"1h"):
            collect("wealth clock")
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['blueberrydispenser'] and checkRespawn('blueberrydispenser','4h'):
            collect('blueberry dispenser')
            stingerHunt()
            if getStatus() == "disconnect": return
        
        
        if setdat['strawberrydispenser'] and checkRespawn('strawberrydispenser','4h'):
            collect('strawberry dispenser')
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['royaljellydispenser'] and checkRespawn('royaljellydispenser','22h'):
            collect('royal jelly dispenser')
            stingerHunt()
            if getStatus() == "disconnect": return
            
        if setdat['treatdispenser'] and checkRespawn('treatdispenser','1h'):
            collect('treat dispenser')
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['stockings'] and checkRespawn('stockings','1h'):
            collect('stockings',1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['wreath'] and checkRespawn('wreath','30m'):
            wreath()
            stingerHunt()
            if getStatus() == "disconnect": return
            
        if setdat['feast'] and checkRespawn('feast','90m'):
            collect('feast',1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['samovar'] and checkRespawn('samovar','6h'):
            collect('samovar',1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['snow_machine'] and checkRespawn('snow_machine','2h'):
            collect('snow_machine')
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['lid_art'] and checkRespawn('lid_art','8h'):
            collect('lid_art',1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['candles'] and checkRespawn('candles','4h'):
            collect('candles',1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['gluedispenser'] and checkRespawn('gluedispenser','22h'):
            collect('glue dispenser')
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat['mondo_buff']:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            hour,minute,_ = [int(x) for x in current_time.split(":")]
            if minute < 10 and checkRespawn('mondo_buff','20m'):
                tempdict = loadtimings()
                tempdict['mondo_buff'] = time.time()//3600
                templist = []
                
                for i in tempdict:
                    templist.append("\n{}:{}".format(i,tempdict[i]))
                with open('timings.txt','w') as f:
                    f.writelines(templist)
                f.close()
                mondo_buff()
                webhook("","Collected: Mondo Buff","bright green",1)
                reset.reset()
                convert()
                stingerHunt()
                if getStatus() == "disconnect": return
        
            
        
        #Planter check
        
        if planterset['enable_planters']:
            if not continuePlanters or not occupiedStuff:
                
                occupiedStuff = []
                for i in range(maxPlanters):
                    bestPlanter = getBestPlanter(planterFields[i],occupiedStuff,planterTypes)
                    webhook('',"Traveling: {} ({})\nObjective: Place Planter".format(displayPlanterName(bestPlanter),planterFields[i].title()),"dark brown")
                    goToPlanter(planterFields[i],1)
                    if getStatus() == "disconnect": return
                    placePlanter(bestPlanter)
                    occupiedStuff.append((bestPlanter,planterFields[i]))
                continuePlanters = 1
                log(occupiedStuff)
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
                        for i in range(2):
                            goToPlanter(currField)
                            if getStatus() == "disconnect": return
                            webhook('',"Traveling: {} ({})\nObjective: Collect Planter, Attempt: {}".format(displayPlanterName(currPlanter),currField.title(),i+1),"dark brown")
                            if ebutton():
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
                                break
                            else:
                                webhook("","Cant find Planter","red",1)
                                reset.reset()
                        else:
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
                log(occupiedStuff)
                log(occupiedFields)
                log(planterFields)
                for _ in range(maxPlanters-len(occupiedStuff)):
                    for i in planterFields:
                        if not i in fieldsToPlace and not i in occupiedFields:
                            fieldsToPlace.append(i)
                            break
                    
                log(fieldsToPlace)
                for i in fieldsToPlace:
                    bestPlanter = getBestPlanter(i,occupiedStuff,planterTypes)
                    webhook('',"Traveling: {} ({})\nObjective: Place Planter".format(displayPlanterName(bestPlanter),i.title()),"dark brown")
                    goToPlanter(i,1)
                    if getStatus() == "disconnect": return
                    placePlanter(bestPlanter)
                    occupiedStuff.append((bestPlanter,i))
                    
                with open("planterdata.txt","w") as f:
                    f.write("{}\n{}\n{}".format(occupiedStuff,planterTypes,planterFields))
                f.close()             
                                                                                        
        #Mob run check
        stingerHunt()
        if getStatus() == "disconnect": return
        if setdat['werewolf'] and checkRespawn("werewolf","1h"):
            killMob("pumpkin","werewolf",1)
        if setdat["ladybug"] and checkRespawn("ladybug_strawberry","5m"):
            
            if checkRespawn("ladybug_mushroom","5m"):
                killMob("strawberry","ladybug",0)
                stingerHunt()
                if getStatus() == "disconnect": return
                move.hold("s",4)
                move.hold("a",3)
                move.hold("w",5.5)
                move.hold("s",3)
                lootMob("mushroom","ladybug",1)
            else:
                killMob("strawberry","ladybug",1)
        stingerHunt()
        if getStatus() == "disconnect": return
        if setdat["ladybug"] and checkRespawn("ladybug_clover","5m"):
            killMob("clover","ladybug",1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat["ladybug"] and checkRespawn("ladybug_mushroom","5m"):
            killMob("mushroom","ladybug",1)
            stingerHunt()
            if getStatus() == "disconnect": return
       
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_clover","5m"):
            if checkRespawn("rhinobeetle_blueflower","5m"):
                #webhook("","hi","red")
                killMob("clover","rhino beetle",0)
                stingerHunt()
                if getStatus() == "disconnect": return
                move.hold("s",7)
                time.sleep(1)
                lootMob("blue flower","rhinobeetle",1)
            else:
                killMob("clover","rhino beetle",1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_blueflower","5m"):
            killMob("blue flower","rhino beetle",1)
            stingerHunt()
            if getStatus() == "disconnect": return
            
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_bamboo","5m"):
            killMob("bamboo","rhino beetle",1)
            stingerHunt()
        if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_pineapple","5m"):
            killMob("pineapple","rhino beetle",1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat["mantis"] and checkRespawn("mantis_pinetree","20m"):
            killMob("pine tree","mantis",1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat["mantis"] and checkRespawn("mantis_pineapple","20m"):
            killMob("pineapple","mantis",1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat["scorpion"] and checkRespawn("scorpion_rose","20m"):
            killMob("rose","scorpion",1)
            stingerHunt()
            if getStatus() == "disconnect": return
        
        if setdat["spider"] and checkRespawn("spider_spider","30m"):
            killMob("spider","spider",1)
        #gather check
        stingerHunt()
        if getStatus() == "disconnect": return
        
        if setdat['gather_enable']:
            gather(gfid)
            gfid += 1
            while True:
                if gfid >= len(setdat['gather_field']):
                    gfid = 0
                if setdat["gather_field"][gfid].lower() == "none":
                    gfid += 1
                else: break
        else:
            mouse.click(Button.left, 1)
        

            

def haste_comp():
    while True:
        getHaste()
        time.sleep(1)
        print('a')
def setResolution():
    wwd = int(pag.size()[0])
    whd = int(pag.size()[1])
    warnings = []
    info  = str(subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)).lower()
    if "retina" in info or "m1" in info or "m2" in info:
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
        "1366x768": [0.8,1,1,1.2],
        "4096x2304": [1.45,0.91,1.32,1.5],
        "3024x1964": [1,0.98, 1.2, 1.2],
        "3360x2100": [1.2,0.95,1.2,1.3],
        "4480x2520": [1.4,0.89,1.4,1.9],
        "3600x2338": [1.45,0.93,1.2,1.6],
        "3584x2240": [1.3, 0.93, 1.2, 1.5],
        "1280x800": [0.9,1.03,1,1],
        "3840x2160": [2.3,1.85,2.35,2.6]
        }
    if ndisplay in multiInfo:
        loadsettings.save("y_screenshot_multiplier",multiInfo[ndisplay][0],"multipliers.txt")
        loadsettings.save("x_screenshot_multiplier",multiInfo[ndisplay][1],"multipliers.txt")
        loadsettings.save("y_length_multiplier",multiInfo[ndisplay][2],"multipliers.txt")
        loadsettings.save("x_length_multiplier",multiInfo[ndisplay][3],"multipliers.txt")
    else:
        warnings.append("\nScreen Coordinates not found in supported list. Contact Existance to get it supported")
    if warnings:
        print("\033[0;31mWarnings:\n{}\033[00m".format(warnings))
if __name__ == "__main__":
    with open('macroLogs.log', 'w'):
        pass
    with open('firstRun.txt', 'w') as f:
        f.write("1")
    f.close()
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = bool(subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True).communicate()[0])
    print("\033[0;32m\n\nTo launch the macro manually, enter the following 2 commands in terminal:\033[00m")
    print("cd path/to/macro-folder\npython3 e_macro.py\n")
    print("\033[0;32mTo stop the macro\033[00m")
    print("tab out of roblox, make sure terminal is in focus and press ctrl c\nor,\nright click the macro app in the dock and force quit")
    print("\n\nYour python version is {}".format(python_ver))
    print("Your macro version is {}\n\n".format(macrov))
    log("Your macro version is {}\n\n".format(macrov))
    setResolution()
    loadSave()
    plantdat = loadsettings.planterLoad()
    firstRun = 1
    ww = savedata["ww"]
    wh = savedata["wh"]
    root = tk.Tk(className='exih_macro')
    root.geometry('780x460')
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
    frame1 = ttk.Frame(notebook, width=780, height=460)
    frame2 = ttk.Frame(notebook, width=780, height=460)
    frame3 = ttk.Frame(notebook, width=780, height=460)
    frame4 = ttk.Frame(notebook, width=780, height=460)
    frame6 = ttk.Frame(notebook, width=780, height=460)
    frame7 = ttk.Frame(notebook, width=780, height=460)

    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    frame3.pack(fill='both', expand=True)
    frame4.pack(fill='both', expand=True)
    frame6.pack(fill='both', expand=True)
    frame7.pack(fill='both', expand=True)

    notebook.add(frame1, text='Gather')
    notebook.add(frame2, text='Bug run')
    notebook.add(frame4, text='Collect')
    notebook.add(frame6, text='Planters')
    notebook.add(frame3, text='In Game Settings')
    notebook.add(frame7, text='Other Settings')

    #get variables
    gather_enable = tk.IntVar(value=setdat["gather_enable"])
    gather_field_one = tk.StringVar(root)
    gather_field_one.set(setdat["gather_field"][0].title())
    gather_field_two = tk.StringVar(root)
    gather_field_two.set(setdat["gather_field"][1].title())
    gather_field_three = tk.StringVar(root)
    gather_field_three.set(setdat["gather_field"][2].title())
    
    return_to_hive_one = tk.StringVar(root)
    return_to_hive_one.set(setdat["return_to_hive"][0].title())
    return_to_hive_two = tk.StringVar(root)
    return_to_hive_two.set(setdat["return_to_hive"][1].title())
    return_to_hive_three = tk.StringVar(root)
    return_to_hive_three.set(setdat["return_to_hive"][2].title())
    
    gather_pattern_one = tk.StringVar(root)
    gather_pattern_one.set(setdat["gather_pattern"][0])
    gather_pattern_two = tk.StringVar(root)
    gather_pattern_two.set(setdat["gather_pattern"][1])
    gather_pattern_three = tk.StringVar(root)
    gather_pattern_three.set(setdat["gather_pattern"][2])
    
    gather_size_one = tk.StringVar(root)
    gather_size_one.set(setdat["gather_size"][0].title())
    gather_size_two = tk.StringVar(root)
    gather_size_two.set(setdat["gather_size"][1].title())
    gather_size_three = tk.StringVar(root)
    gather_size_three.set(setdat["gather_size"][2].title())

    
    gather_width_one = tk.IntVar(value=setdat["gather_width"][0])
    gather_width_two = tk.IntVar(value=setdat["gather_width"][1])
    gather_width_three = tk.IntVar(value=setdat["gather_width"][2])
    
    gather_time_one = setdat["gather_time"][0]
    gather_time_two = setdat["gather_time"][1]
    gather_time_three = setdat["gather_time"][2]
    
    pack_one =setdat["pack"][0]
    pack_two =setdat["pack"][1]
    pack_three =setdat["pack"][2]
    
    before_gather_turn_one = tk.StringVar(root)
    before_gather_turn_one.set(setdat["before_gather_turn"][0])
    before_gather_turn_two = tk.StringVar(root)
    before_gather_turn_two.set(setdat["before_gather_turn"][1])
    before_gather_turn_three = tk.StringVar(root)
    before_gather_turn_three.set(setdat["before_gather_turn"][2])
    
    turn_times_one = tk.IntVar(value=setdat["turn_times"][0])
    turn_times_two = tk.IntVar(value=setdat["turn_times"][1])
    turn_times_three = tk.IntVar(value=setdat["turn_times"][2])
      
    start_location_one = tk.StringVar(root)
    start_location_one.set(setdat["start_location"][0].title())
    start_location_two = tk.StringVar(root)
    start_location_two.set(setdat["start_location"][1].title())
    start_location_three = tk.StringVar(root)
    start_location_three.set(setdat["start_location"][2].title())
    
    distance_from_center_one = tk.StringVar(root)
    distance_from_center_one.set(setdat["distance_from_center"][0])
    distance_from_center_two = tk.StringVar(root)
    distance_from_center_two.set(setdat["distance_from_center"][1])
    distance_from_center_three = tk.StringVar(root)
    distance_from_center_three.set(setdat["distance_from_center"][2])
    
    whirligig_slot_one = tk.StringVar(root)
    whirligig_slot_one.set(setdat["whirligig_slot"][0])
    whirligig_slot_two = tk.StringVar(root)
    whirligig_slot_two.set(setdat["whirligig_slot"][1])
    whirligig_slot_three = tk.StringVar(root)
    whirligig_slot_three.set(setdat["whirligig_slot"][2])
    
    field_drift_compensation_one = tk.IntVar(value=setdat["field_drift_compensation"][0])
    field_drift_compensation_two = tk.IntVar(value=setdat["field_drift_compensation"][1])
    field_drift_compensation_three = tk.IntVar(value=setdat["field_drift_compensation"][2])
    
    
    stump_snail = tk.IntVar(value=setdat["stump_snail"])
    continue_after_stump_snail = tk.IntVar(value=setdat["continue_after_stump_snail"])
    ladybug = tk.IntVar(value=setdat["ladybug"])
    rhinobeetle = tk.IntVar(value=setdat["rhinobeetle"])
    werewolf = tk.IntVar(value=setdat["werewolf"])
    scorpion = tk.IntVar(value=setdat["scorpion"])
    spider = tk.IntVar(value=setdat["spider"])
    mantis = tk.IntVar(value=setdat["mantis"])
    stinger = tk.IntVar(value=setdat["stinger"])
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
    haste_compensation = tk.IntVar(value=setdat["haste_compensation"])
    low_performance_haste_compensation = tk.IntVar(value=setdat["low_performance_haste_compensation"])
    rejoin_every_enabled = tk.IntVar(value=setdat["rejoin_every_enabled"])
    rejoin_every = setdat['rejoin_every']
    rejoin_delay = setdat['rejoin_delay']
    rejoin_method = tk.StringVar(root)
    rejoin_method.set(setdat['rejoin_method'])
    manual_fullscreen = tk.IntVar(value=setdat['manual_fullscreen'])
    
    wealthclock = tk.IntVar(value=setdat["wealthclock"])
    blueberrydispenser = tk.IntVar(value=setdat["blueberrydispenser"])
    strawberrydispenser = tk.IntVar(value=setdat["strawberrydispenser"])
    royaljellydispenser  = tk.IntVar(value=setdat["royaljellydispenser"])
    treatdispenser = tk.IntVar(value=setdat["treatdispenser"])
    gluedispenser = tk.IntVar(value=setdat["gluedispenser"])
    gumdrop_slot = tk.StringVar(root)
    gumdrop_slot.set(setdat["gumdrop_slot"])
    stockings = tk.IntVar(value=setdat["stockings"])
    feast = tk.IntVar(value=setdat["feast"])
    samovar = tk.IntVar(value=setdat["samovar"])
    wreath = tk.IntVar(value=setdat["wreath"])
    snow_machine = tk.IntVar(value=setdat["snow_machine"])
    mondo_buff = tk.IntVar(value=setdat["mondo_buff"])
    lid_art = tk.IntVar(value=setdat["lid_art"])
    candles = tk.IntVar(value=setdat["candles"])
    
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

    multipliers = loadsettings.load('multipliers.txt')



    
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
            mouse.press(Button.left)
            time.sleep(0.05)
            exec(open("gather_{}.py".format(setdat['gather_pattern'])).read())
            time.sleep(0.05)
            time.sleep(0.05)
            timespent = (time.perf_counter() - timestart)/60
            if timespent > 20:
                webhook("Gathering: ended","Time: {:.2f}".format(timespent),"light green")
                break
            if setdat['field_drift_compensation'] and setdat['gather_pattern'] != "stationary":
                fieldDriftCompensation()
            mouse.release(Button.left)
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
            vals.append(imagesearch.find("eb.png",0,ww//3,0,ww//3,wh//3)[3])
            
        webhook("","Done obtaining vals","dark brown")
            
        vals = sorted(vals,reverse=True)
        log(vals)
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
            #calibrateebutton()
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
            "haste_compensation": haste_compensation.get(),
            "low_performance_haste_compensation": low_performance_haste_compensation.get(),
            "rejoin_every_enabled": rejoin_every_enabled.get(),
            "rejoin_every": rejoinetextbox.get(1.0,"end").replace("\n",""),
            "rejoin_delay": rejoindelaytextbox.get(1.0,"end").replace("\n",""),
            "rejoin_method": rejoin_method.get(),
            "manual_fullscreen": manual_fullscreen.get(),
            
            "gather_enable": gather_enable.get(),
            "gather_field": [gather_field_one.get(),gather_field_two.get(),gather_field_three.get()],
            "gather_pattern": [gather_pattern_one.get(), gather_pattern_two.get(), gather_pattern_three.get()],
            "gather_size": [gather_size_one.get(), gather_size_two.get(), gather_size_three.get()],
            "gather_width": [gather_width_one.get(), gather_width_two.get(), gather_width_three.get()],
            "gather_time": [timetextbox_one.get(1.0,"end").replace("\n",""), timetextbox_two.get(1.0,"end").replace("\n",""), timetextbox_three.get(1.0,"end").replace("\n","")],
            "pack": [packtextbox_one.get(1.0,"end").replace("\n",""), packtextbox_two.get(1.0,"end").replace("\n",""), packtextbox_three.get(1.0,"end").replace("\n","")],
            "before_gather_turn": [before_gather_turn_one.get(), before_gather_turn_two.get(), before_gather_turn_three.get()],  
            "turn_times": [turn_times_one.get(), turn_times_two.get(), turn_times_three.get()],
            "return_to_hive": [return_to_hive_one.get(), return_to_hive_two.get(), return_to_hive_three.get()],
            "whirligig_slot": [whirligig_slot_one.get(), whirligig_slot_two.get(), whirligig_slot_three.get()],
            "start_location": [start_location_one.get(), start_location_two.get(), start_location_three.get()],
            "distance_from_center": [distance_from_center_one.get(), distance_from_center_two.get(), distance_from_center_three.get()],
            "field_drift_compensation": [field_drift_compensation_one.get(), field_drift_compensation_two.get(), field_drift_compensation_three.get()],
                
            "stump_snail": stump_snail.get(),
            "continue_after_stump_snail": continue_after_stump_snail.get(),
            "ladybug": ladybug.get(),
            "rhinobeetle": rhinobeetle.get(),
            "spider": spider.get(),
            "scorpion": scorpion.get(),
            "werewolf": werewolf.get(),
            "mantis": mantis.get(),
            "stinger": stinger.get(),

            "wealthclock": wealthclock.get(),
            "blueberrydispenser": blueberrydispenser.get(),
            "strawberrydispenser": strawberrydispenser.get(),
            "royaljellydispenser":royaljellydispenser.get(),
            "treatdispenser":treatdispenser.get(),
            "gluedispenser":gluedispenser.get(),
            "gumdrop_slot":gumdrop_slot.get(),
            "stockings":stockings.get(),
            "feast": feast.get(),
            "samovar": samovar.get(),
            "wreath": wreath.get(),
            "snow_machine": snow_machine.get(),
            "mondo_buff": mondo_buff.get(),
            "lid_art":lid_art.get(),
            "candles": candles.get(),

            "start_honey":0,
            "prev_honey":0,
            "start_time":time.time(),
            "canon_time":1.0,#cttextbox.get(1.0,"end").replace("\n",""),
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
                
                with open("planterdata.txt","w") as a:
                    a.write("[]\n{}\n{}".format(planterTypes_set,planterFields_set))
                a.close()
                with open("plantertimings.txt","r") as b:
                    lines = b.read().split("\n")
                b.close()
                with open("plantertimings.txt","w") as c:
                    writeStuff = []
                    for i in lines:
                        if ":" in i:
                            k,_ = i.split(':')
                            writeStuff.append("{}:0".format(k))
                    print(writeStuff)
                    c.write('\n'.join(writeStuff))
                c.close()
                planterTypes_prev, planterFields_prev = planterTypes_set, planterFields_set
                
                            
        '''
        if int(setdict['hivethreshold']) == 1:
            window = tk.Toplevel() 
            label = tk.Label(window,text="You have not calibrated your macro yet. Do you want to calibrate it automatically?")
            button_yes = ttk.Button(window, text="Yes",command=lambda: [calibrate(), window.destroy()]) 
            button_no = ttk.Button(window, text="No",command=lambda: [macro(),window.destroy()]) 
            label.grid(row=0, column=0, columnspan=2)
            button_yes.grid(row=1, column=0)
            button_no.grid(row=1, column=1)
        
        else:
        '''
        macro()
    def macro():
        global  prevHour, prevMin, honeyHist
        savedat = loadRes()
        ww = savedat['ww']
        wh = savedat['wh']
        webhook("Macro started - Report","exih_macro\nVersion {}\nScreen Coordinates: {}x{}\nPython {}".format(macrov,ww,wh,python_ver),"dark brown")
        setdat = loadsettings.load()
        if not is_running("roblox"):
            rejoin()
        cmd = """
            osascript -e 'activate application "Roblox"' 
        """
        os.system(cmd)
        time.sleep(0.5)
        #fullscreen()
        gather.value = 0
        timeupdate.value = int(time.time())
        time.sleep(0.5)
        prevHour = datetime.now().hour
        prevMin = datetime.now().minute
        honeyHist = [setdat['prev_honey']]*60
        hastecompbg_proc = multiprocessing.Process(target=hastecompbg)
        vic_proc = multiprocessing.Process(target=vic)
        discord_bot_proc = multiprocessing.Process(target=discord_bot)
        if setdat['enable_discord_bot']:
            discord_bot_proc.start()
        if setdat['haste_compensation']:
            hastecompbg_proc.start()
        if setdat['stinger'] or (setdat['enable_discord_webhook'] and setdat['send_screenshot']):
            vic_proc.start()
        try:
            ses_start = 1
            while True:
                #if keyboard.is_pressed('q'):
                    #raise KeyboardInterrupt
               startLoop(planterTypes_prev, planterFields_prev,ses_start) 
               rejoin()
               ses_start = 0
                

                    
        except KeyboardInterrupt:
            hastecompbg_proc.terminate()
            discord_bot_proc.terminate()
            vic_proc.terminate()
            webhook("Macro Stopped","","dark brown")
    
    def savedisplaytype(event):
        loadsettings.save("display_type",display_type.get().lower())
        setResolution()
        
    def disablews_one(event):
        if return_to_hive_one.get().lower() == "whirligig":
            wslotmenu_one.configure(state="normal")
        else:
            wslotmenu_one.configure(state="disable")
            
    def disablews_two(event):
        if return_to_hive_two.get().lower() == "whirligig":
            wslotmenu_two.configure(state="normal")
        else:
            wslotmenu_two.configure(state="disable")
            
    def disablews_three(event):
        if return_to_hive_three.get().lower() == "whirligig":
            wslotmenu_three.configure(state="normal")
        else:
            wslotmenu_three.configure(state="disable")

    def disableeb(event):
        pass
        '''
        if ebdetect.get().lower() == "pyautogui":
            ebtextbox.configure(state="disable")
        else:
            ebtextbox.configure(state="normal")
        '''
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

    tkinter.Label(frame1, text = "Pattern").place(x = 230, y = 15)
    tkinter.Label(frame1, text = "Gather Until").place(x = 450, y = 15) 
    tkinter.Label(frame1, text = "Fields").place(x = 35, y = 50)
    tkinter.Label(frame1, text = "Shape").place(x = 160, y = 50)
    tkinter.Label(frame1, text = "Size").place(x = 260, y = 50)
    tkinter.Label(frame1, text = "Width").place(x = 320, y = 50)
    tkinter.Label(frame1, text = "Start Location").place(x = 625, y = 50)
    tkinter.Label(frame1, text = "Mins").place(x = 400, y = 50)
    tkinter.Label(frame1, text = "Backpack%").place(x = 440, y = 50)
    tkinter.Label(frame1, text = "To Hive By").place(x = 520, y = 50)
    tkinter.Label(frame1, text = "Start Location").place(x = 625, y = 50)
    ttk.Separator(frame1,orient="vertical").place(x=610, y=30, width=2, height=310)    
    ttk.Separator(frame1,orient="vertical").place(x=386, y=30, width=2, height=310)
    ttk.Separator(frame1,orient="vertical").place(x=130, y=30, width=2, height=310)
    ttk.Separator(frame1,orient="horizontal").place(x=15, y=75, width=700, height=2)
    ttk.Separator(frame1,orient="horizontal").place(x=15, y=160, width=700, height=2)
    ttk.Separator(frame1,orient="horizontal").place(x=15, y=250, width=700, height=2)
    
    ylevel = 50
    dropField = ttk.OptionMenu(frame1, gather_field_one,setdat['gather_field'][0].title(), *gather_fields[1:],style='smaller.TMenubutton' )
    dropField.place(x = 10, y = ylevel+35,height=22,width=100)
    tkinter.Checkbutton(frame1, text="Field Drift\nCompensation", variable=field_drift_compensation_one).place(x=10, y = ylevel+65)

    dropField = ttk.OptionMenu(frame1, gather_pattern_one,setdat['gather_pattern'][0], *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")],style='smaller.TMenubutton')
    dropField.place(width=90,x = 145, y = ylevel+35,height=22)
    dropField = ttk.OptionMenu(frame1, gather_size_one,setdat['gather_size'][0].title(), *["S","M","L"],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 255, y = ylevel+35,height = 22)
    dropField = ttk.OptionMenu(frame1, gather_width_one,setdat['gather_width'][0], *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 320, y = ylevel+35,height=22)

    tkinter.Label(frame1, text = "Before Gathering,\nRotate Camera").place(x = 140, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, before_gather_turn_one,setdat['before_gather_turn'][0].title(), *["None","Left","Right"],style='smaller.TMenubutton' )
    dropField.place(width=60,x = 255, y = ylevel+75,height=22)
    dropField = ttk.OptionMenu(frame1, turn_times_one,setdat['turn_times'][0], *[(x+1) for x in range(4)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 325, y = ylevel+75,height=22)

    timetextbox_one = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    timetextbox_one.insert("end",gather_time_one)
    timetextbox_one.place(x = 400, y=ylevel+35)
    packtextbox_one = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    packtextbox_one.insert("end",pack_one)
    packtextbox_one.place(x = 460, y=ylevel+35)
    dropConvert = ttk.OptionMenu(frame1 , return_to_hive_one,setdat['return_to_hive'][0].title(), command = disablews_one, *["Walk","Reset","Rejoin","Whirligig"],style='smaller.TMenubutton')
    dropConvert.place(width=75,x = 520, y = ylevel+35,height=22)
    tkinter.Label(frame1, text = "Whirligig Slot").place(x = 452, y = ylevel+65)
    wslotmenu_one = ttk.OptionMenu(frame1 , whirligig_slot_one,setdat['whirligig_slot'][0], *[1,2,3,4,5,6,7,"none"],style='smaller.TMenubutton')
    wslotmenu_one.place(width=50,x = 542, y = ylevel+65,height=22)


    dropField = ttk.OptionMenu(frame1, start_location_one,setdat['start_location'][0].title(), *["Center","Upper Right","Right","Lower Right","Bottom","Lower Left","Left","Upper Left","Top"],style='smaller.TMenubutton' )
    dropField.place(width=100,x = 625, y = ylevel+35,height=22)
    tkinter.Label(frame1, text = "Distance").place(x = 625, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, distance_from_center_one,setdat['distance_from_center'][0], *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 695, y = ylevel+65,height=22)

    ylevel = 140
    dropField = ttk.OptionMenu(frame1, gather_field_two,setdat['gather_field'][1].title(), *gather_fields,style='smaller.TMenubutton' )
    dropField.place(x = 10, y = ylevel+35,height=22,width=100)
    tkinter.Checkbutton(frame1, text="Field Drift\nCompensation", variable=field_drift_compensation_two).place(x=10, y = ylevel+65)

    dropField = ttk.OptionMenu(frame1, gather_pattern_two,setdat['gather_pattern'][1], *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")],style='smaller.TMenubutton')
    dropField.place(width=90,x = 145, y = ylevel+35,height=22)
    dropField = ttk.OptionMenu(frame1, gather_size_two,setdat['gather_size'][1].title(), *["S","M","L"],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 255, y = ylevel+35,height = 22)
    dropField = ttk.OptionMenu(frame1, gather_width_two,setdat['gather_width'][1], *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 320, y = ylevel+35,height=22)

    tkinter.Label(frame1, text = "Before Gathering,\nRotate Camera").place(x = 140, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, before_gather_turn_two,setdat['before_gather_turn'][1].title(), *["None","Left","Right"],style='smaller.TMenubutton' )
    dropField.place(width=60,x = 255, y = ylevel+75,height=22)
    dropField = ttk.OptionMenu(frame1, turn_times_two,setdat['turn_times'][1], *[(x+1) for x in range(4)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 325, y = ylevel+75,height=22)

    timetextbox_two = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    timetextbox_two.insert("end",gather_time_two)
    timetextbox_two.place(x = 400, y=ylevel+35)
    packtextbox_two = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    packtextbox_two.insert("end",pack_two)
    packtextbox_two.place(x = 460, y=ylevel+35)
    dropConvert = ttk.OptionMenu(frame1 , return_to_hive_two,setdat['return_to_hive'][1].title(), command = disablews_two, *["Walk","Reset","Rejoin","Whirligig"],style='smaller.TMenubutton')
    dropConvert.place(width=75,x = 520, y = ylevel+35,height=22)
    tkinter.Label(frame1, text = "Whirligig Slot").place(x = 452, y = ylevel+65)
    wslotmenu_two = ttk.OptionMenu(frame1 , whirligig_slot_two,setdat['whirligig_slot'][1], *[1,2,3,4,5,6,7,"none"],style='smaller.TMenubutton')
    wslotmenu_two.place(width=50,x = 542, y = ylevel+65,height=22)


    dropField = ttk.OptionMenu(frame1, start_location_two,setdat['start_location'][1].title(), *["Center","Upper Right","Right","Lower Right","Bottom","Lower Left","Left","Upper Left","Top"],style='smaller.TMenubutton' )
    dropField.place(width=100,x = 625, y = ylevel+35,height=22)
    tkinter.Label(frame1, text = "Distance").place(x = 625, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, distance_from_center_two,setdat['distance_from_center'][1], *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 695, y = ylevel+65,height=22)

    ylevel = 230
    dropField = ttk.OptionMenu(frame1, gather_field_three,setdat['gather_field'][2].title(), *gather_fields,style='smaller.TMenubutton' )
    dropField.place(x = 10, y = ylevel+35,height=22,width=100)
    tkinter.Checkbutton(frame1, text="Field Drift\nCompensation", variable=field_drift_compensation_three).place(x=10, y = ylevel+65)

    dropField = ttk.OptionMenu(frame1, gather_pattern_three,setdat['gather_pattern'][2], *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")],style='smaller.TMenubutton')
    dropField.place(width=90,x = 145, y = ylevel+35,height=22)
    dropField = ttk.OptionMenu(frame1, gather_size_three,setdat['gather_size'][2].title(), *["S","M","L"],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 255, y = ylevel+35,height = 22)
    dropField = ttk.OptionMenu(frame1, gather_width_three,setdat['gather_width'][2], *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 320, y = ylevel+35,height=22)

    tkinter.Label(frame1, text = "Before Gathering,\nRotate Camera").place(x = 140, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, before_gather_turn_three,setdat['before_gather_turn'][2].title(), *["None","Left","Right"],style='smaller.TMenubutton' )
    dropField.place(width=60,x = 255, y = ylevel+75,height=22)
    dropField = ttk.OptionMenu(frame1, turn_times_three,setdat['turn_times'][2], *[(x+1) for x in range(4)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 325, y = ylevel+75,height=22)

    timetextbox_three = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    timetextbox_three.insert("end",gather_time_three)
    timetextbox_three.place(x = 400, y=ylevel+35)
    packtextbox_three = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    packtextbox_three.insert("end",pack_three)
    packtextbox_three.place(x = 460, y=ylevel+35)
    dropConvert = ttk.OptionMenu(frame1 , return_to_hive_three,setdat['return_to_hive'][2].title(), command = disablews_three, *["Walk","Reset","Rejoin","Whirligig"],style='smaller.TMenubutton')
    dropConvert.place(width=75,x = 520, y = ylevel+35,height=22)
    tkinter.Label(frame1, text = "Whirligig Slot").place(x = 452, y = ylevel+65)
    wslotmenu_three = ttk.OptionMenu(frame1 , whirligig_slot_three,setdat['whirligig_slot'][2], *[1,2,3,4,5,6,7,"none"],style='smaller.TMenubutton')
    wslotmenu_three.place(width=50,x = 542, y = ylevel+65,height=22)


    dropField = ttk.OptionMenu(frame1, start_location_three,setdat['start_location'][2].title(), *["Center","Upper Right","Right","Lower Right","Bottom","Lower Left","Left","Upper Left","Top"],style='smaller.TMenubutton' )
    dropField.place(width=100,x = 625, y = ylevel+35,height=22)
    tkinter.Label(frame1, text = "Distance").place(x = 625, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, distance_from_center_three,setdat['distance_from_center'][2], *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 695, y = ylevel+65,height=22)
    

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
    tkinter.Checkbutton(frame4, text="Candles", variable=candles).place(x=595, y = 85)
    tkinter.Checkbutton(frame4, text="Glue Dispenser", variable=gluedispenser).place(x=0, y = 120)
    tkinter.Label(frame4, text = "Gumdrop Slot").place(x = 130, y = 122)
    dropField = ttk.OptionMenu(frame4, gumdrop_slot,setdat['gumdrop_slot'], *[x for x in range(1,8)],style='smaller.TMenubutton')
    dropField.place(width=65,x = 225, y = 124,height=20)
    tkinter.Checkbutton(frame4, text="Stinger Hunt", variable=stinger).place(x=0, y = 155)
    
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

    tkinter.Label(frame3, text = "Sprinkler Type").place(x = 0, y = 85)
    dropField = ttk.OptionMenu(frame3, sprinkler_type, setdat['sprinkler_type'], *["Basic","Silver","Golden","Diamond","Saturator"],style='my.TMenubutton' )
    dropField.place(width=90,x = 100, y = 85,height=24)

    tkinter.Label(frame3, text = "Slot").place(x = 205, y = 85)
    dropField = ttk.OptionMenu(frame3, sprinkler_slot, setdat['sprinkler_slot'], *[x+1 for x in range(6)],style='my.TMenubutton' )
    dropField.place(width=60,x = 245, y = 85,height=24)

    tkinter.Checkbutton(frame3, text="Enable Haste Compensation", variable=haste_compensation).place(x=0, y = 120)
    


    #Tab 6
    tkinter.Checkbutton(frame7, text="Enable Discord Webhook", command = disabledw,variable=enable_discord_webhook).place(x=0, y = 15)
    tkinter.Label(frame7, text = "Discord Webhook Link").place(x = 350, y = 15)
    urltextbox = tkinter.Text(frame7, width = 24, height = 1, yscrollcommand = True, bg= wbgc)
    urltextbox.insert("end",discord_webhook_url)
    sendss = tkinter.Checkbutton(frame7, text="Send screenshots", variable=send_screenshot)
    sendss.place(x=200, y = 15)
    urltextbox.place(x = 500, y=17)
    
    tkinter.Label(frame7, text = "Private Server Link (optional)").place(x = 0, y = 85)
    linktextbox = tkinter.Text(frame7, width = 24, height = 1, bg= wbgc)
    linktextbox.insert("end",private_server_link)
    linktextbox.place(x=190,y=87)
    
    tkinter.Checkbutton(frame7, text="Enable Discord Bot", variable=enable_discord_bot).place(x=0, y = 50)
    tkinter.Label(frame7, text = "Discord Bot Token").place(x = 170, y = 50)
    tokentextbox = tkinter.Text(frame7, width = 24, height = 1, bg= wbgc)
    tokentextbox.insert("end",discord_bot_token)
    tokentextbox.place(x = 300, y=52)
    

    tkinter.Checkbutton(frame7, text="Rejoin every", variable=rejoin_every_enabled).place(x=0, y = 120)
    rejoinetextbox = tkinter.Text(frame7, width = 4, height = 1, bg= wbgc)
    rejoinetextbox.insert("end",rejoin_every)
    rejoinetextbox.place(x=104,y=123)
    tkinter.Label(frame7, text = "hours").place(x = 140, y = 120)

    tkinter.Label(frame7, text = "Wait for").place(x = 0, y = 155)
    rejoindelaytextbox = tkinter.Text(frame7, width = 4, height = 1, bg= wbgc)
    rejoindelaytextbox.insert("end",rejoin_delay)
    rejoindelaytextbox.place(x=55,y=158)
    tkinter.Label(frame7, text = "secs when rejoining").place(x = 90, y = 155)
    tkinter.Checkbutton(frame7, text="Manually fullscreen when rejoining (Enable when roblox doesnt launch in fullscreen)", variable=manual_fullscreen).place(x=0, y = 190)
    tkinter.Label(frame7, text = "Rejoin method").place(x = 250, y = 155)
    dropField = ttk.OptionMenu(frame7, rejoin_method, setdat['rejoin_method'].title(), *["New Tab","Type In Link"],style='my.TMenubutton' )
    dropField.place(width=90,x = 360, y = 155,height=24)
    
    #Tab 7
    '''
    ttk.Button(frame5, text = "Calibrate Hive", command = calibratehive, width = 10).place(x=0,y=13)
    tkinter.Checkbutton(frame5, text="Reverse Hive Direction", variable=reverse_hive_direction).place(x=140, y = 15)
    tkinter.Label(frame5, text = "Screenshot multiplier").place(x = 0, y = 50)
    #dropField = ttk.OptionMenu(frame5, ebdetect,setdat['ebdetect'], command = disableeb, *["cv2","pyautogui"],style='my.TMenubutton' )
    #dropField.place(width=130,x = 158, y = 51,height=24)
    #tkinter.Label(frame5, text = " Threshold").place(x = 300, y = 50)
    #smtextbox = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    #smtextbox.insert("end",multipliers['screenshot_multiplier'])
    #smtextbox.place(x=158,y=53)
    tkinter.Label(frame5, text = "Flight Multiplier").place(x = 0, y = 85)
    cttextbox = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    cttextbox.insert("end",canon_time)
    cttextbox.place(x=110,y=88)
    '''
    #Root
    ttk.Button(root, text = "Start", command = startGo, width = 7 ).place(x=10,y=420)
    ttk.Button(root, text = "Update",command = updateFiles, width = 9,).place(x=150,y=420)
    ttk.Button(root, text = "Experimental update",command = expu, width = 16,).place(x=300,y=420)
    ttk.Label(root, text = "version {}".format(macrov)).place(x = 680, y = 440)

    disablews_one("1")
    disablews_two("1")
    disablews_three("1")
    disabledw()
    disableeb("1")
    root.mainloop()
    


        




