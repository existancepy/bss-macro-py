def printRed(txt):
    print("\033[0;31m{}\033[00m".format(txt))
    
import sys
sv_i = sys.version_info
python_ver = '.'.join([str(sv_i[i]) for i in range(0,3)])
if (sv_i[1]>=10):
    printRed("{} is an incorrect python version. Visit #common-fixes 'resintalling-python' to fix it.".format(python_ver))
    quit()
print(python_ver)
try:
    import pyautogui as pag
except Exception as e:
    print(e)
    printRed("This error means that libraries arent installed. Here are some common causes:\n1. You didnt run the commands to install the library\n2. An incorrect version of python (such as 3.11) was installed. Visit #common-fixes 'reinstalling python' in the discord server\n3. There was an error when installing the libraries, preventing them from being downloaded. Create a support ticket in the discord server ")
    quit()

from difflib import SequenceMatcher
from tkinter_tooltips import *
import time, os, ctypes, tty
import tkinter
import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
import backpack, reset, loadsettings, move,update,updateexperiment
import multiprocessing, webbrowser, imagesearch, discord, subprocess
from webhook import webhook
global savedata
global setdat
from tkinter import messagebox
import numpy as np
import asyncio
from logpy import log
import logging
import pynput
import traceback
from importlib import reload
from pynput.keyboard import Key
from pynput.mouse import Button
from html2image import Html2Image
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
if __name__ == '__main__':
    print("\033[1;35m\nStarting Macro...  \n")
try:
    import ocrpy
    from ocrpy import imToString,customOCR
except:
    os.system("pip3 install --user --force-reinstall paddlepaddle==2.5.0")
    reload(ocrpy)
    from ocrpy import imToString,customOCR
import sv_ttk
import math
import ast
import calibrate_hive
from datetime import datetime
import pyscreeze
import shutil
    
if tuple(map(int, np.__version__.split("."))) >= (1,24,0):
    os.system('pip3 install --user "numpy<1.24.0"')
    reload(numpy)
    import numpy as np
    #printRed("Invalid numpy version. Your current numpy version is {} but the required one is < 1.24.0.\nTo fix this, run the command\npip3 install \"numpy<1.24.0\"".format(np.__version__))
    #quit()
    
if tuple(map(int, pyscreeze.__version__.split("."))) >= (0,1,29):
    os.system('pip3 install --user "pyscreeze<0.1.29"')
    reload(pyscreeze)
    #printRed("Invalid pyscreeze version. Your current pyscreeze version is {} but the required one is < 0.1.29\nTo fix this, run the command\npip3 install \"pyscreeze<0.1.29\"".format(pyscreeze.__version__))
    #quit()

info  = str(subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)).lower()
retina = "retina" in info or "m1" in info or "m2" in info
savedata = {}
ww = ""
wh = ""
ms = pag.size()
mw = ms[0]
mh = ms[1]
stop = 1
setdat = loadsettings.load()
macrov = "1.50.3"
planterInfo = loadsettings.planterInfo()
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
hti = Html2Image()
questData = {}
questBear = ""
questTitle = ""
questInfo = []
with open("quest_data.txt", "r") as f:
    qdata = [x for x in f.read().split("\n") if x]
f.close()

for i in qdata:
    if i.startswith("="):
        i = i.replace("=","")
        questBear = i
        questData[questBear] = {}
    elif i.startswith("-"):
        if questTitle:
            questData[questBear][questTitle] = questInfo
        questTitle = i[1:]
        questInfo = []
    elif i.startswith("#"):
        questData[questBear][questTitle] = questInfo
    else:
        questInfo.append(i)

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
    reservedImages = ['test.png','roblox.png']
    for i in os.listdir():
        if ".png" in i and not i in reservedImages:
            os.remove(i)

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
    cmd = """
            osascript -e 'activate application "Roblox"' 
        """
    os.system(cmd)
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
    try:
        intents.message_content = True
    except:
        intents.messages = True
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
                await message.channel.send("Now attempting to rejoin shortly. Forcing a disconnect")
                setStatus("disconnect")
            elif cmd == "screenshot":
                await message.channel.send("Sending a screenshot via webhook")
                webhook("User Requested: Screenshot","","light blue",1)
            elif cmd == "report":
                await message.channel.send("Sending Hourly Report")
                hourlyReport(0)
                
    client.run(setdat['discord_bot_token'])
    
def getStatus():
    with open("status.txt","r") as f:
        out = f.read()
    f.close()
    return out

def setStatus(msg="none"):
    if msg != "none" and getStatus() == "disconnect": return
    with open("status.txt","w") as f:
        f.write(msg)
    f.close()

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

def addStat(name, value):
    file = loadsettings.load("stats.txt")
    if isinstance(file[name], list):
        if len(file[name]) == 1 and file[name][0] == 0:
            file[name][0] = value
        else:
            file[name].append(value)
    else:
        file[name] += value
    savesettings(file, "stats.txt")

def resetStats():
    file = loadsettings.load("stats.txt")
    resetStats = {
        "gather_time":[0],
        "convert_time":[0],
        "bug_time":0,
        "rejoin_time":0,
        "objective_time":0,
        "bug_kills":0
        }
    out = {**file, **resetStats}
    savesettings(out, "stats.txt")
            
def resetAllStats():
    file = loadsettings.load("stats.txt")
    out = {}
    for k,v in file.items():
        if isinstance(v, list):
            out[k] = [0]
        elif isinstance(v, int) or isinstance(v, float):
            out[k] = 0
        else:
            out[k] = v
    savesettings(out, "stats.txt")
    
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
        if "bear" in text or "talk" in text:
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

def getBesideE():
    text = imToString("bee bear").lower()
    log(text)
    return text

def ebutton(pagmode=0):
    ocrval = ''.join([x for x in list(imToString('ebutton').strip()) if x.isalpha()])
    log(ocrval)
    return "E" in ocrval and len(ocrval) <= 3

def rebutton():
    return "claim" in getBesideE()

def detectNight(bypasstime=0):
    savedat = loadRes()
    ww = savedat['ww']
    wh = savedat['wh']
    if not setdat['stinger']: return False
    if not checkRespawn("night","10m") and not bypasstime:
        return False
    y = 30
    if retina:
        y*=2
    night = pyscreeze.screenshot(region = (0,0,ww/1.8,y))
    res = list(pyscreeze._locateAll_python("./images/general/nightsky.png", night, limit=1))
    if res:
        webhook("","Night Detected","dark brown",1)
        savetimings("night")
        night.save("night.png")
        return True
    return False

def getTop(y):
    height = 30
    if retina:
        height*=2
        y*=2
    res = customOCR(ww/3.5,y,ww/2.5,height,0)
    log(f"{y},{res}")
    if not res: return False
    text = [x[1][0].lower() for x in res]
    
    return "honey" in text or "pollen" in text

def millify(n):
    if not n: return "0"
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def minAndSecs(m):
    secs = round((float(m) - int(m))*60)
    return f"{int(m)}m {secs}s"

def hourlyReport(hourly=1):
    setdat = loadsettings.load()
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
        #remove values less than 1000
        for i, e in enumerate(honeyHist[:]):
            if len(str(e)) <= 4:
                honeyHist.pop(i)
        #remove values less than the previous one
        honeyHist = honeyHist[1:]
        counter = 1
        while counter < len(honeyHist):
            if honeyHist[counter] < honeyHist[counter-1]:
                honeyHist.pop(counter)
            else:
                counter += 1
        if hourly == 0:
            setdat['prev_honey'] = honeyHist[-1]
        log('prev honey: {}'.format(setdat['prev_honey']))
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
        rootDir = os.path.dirname(os.path.abspath(__file__)) + "/hourlyReport"
        with open("./hourlyReport/index.html", "r") as f:
            data = f.read().split("\n")
            data.insert(0,"")
        f.close()
        
        stats = loadsettings.load("stats.txt")
        rejoin_time = minAndSecs(stats["rejoin_time"])
        gather_time = minAndSecs(sum(stats["gather_time"]))
        convert_time = minAndSecs(sum(stats["convert_time"]))
        bug_time = minAndSecs(stats["bug_time"])
        objective_time = minAndSecs(stats["objective_time"])

        gather_avg = minAndSecs(sum(stats["gather_time"])/len(stats["gather_time"]))
        convert_avg = minAndSecs(sum(stats["convert_time"])/len(stats["convert_time"]))
        
        print(data)
        data[30] = f"Rejoining:\t{rejoin_time}"
        data[34] = f"Gathering:\t{gather_time}"
        data[38] = f"Bug Runs:\t{bug_time}"
        data[42] = f"Converting:\t{convert_time}"
        data[46] = f"Collecting Objectives:\t{objective_time}"
        data[55] = f"{rootDir}/assets/buffs.png"
        data[65] = session_time
        data[70] = millify(currHoney)
        data[75] = millify(session_honey)
        data[80] = str(stats["vic_kills"])
        data[92] = millify(hourly_honey)
        data[98] = gather_avg
        data[104] = convert_avg
        data[109] = str(stats["bug_kills"])
        data[132] = f"const time = {xvals}"
        data[133] = f"const honey = {yvals}"
        data[197] = f'const times = [{stats["rejoin_time"]},{sum(stats["gather_time"])},{stats["bug_time"]},{sum(stats["convert_time"])},{stats["objective_time"]}]'

        print(data)
        with open("./hourlyReport/index.html","w") as f:
            f.write('\n'.join(data[1:]))
        f.close()
        
        if setdat["new_ui"]:
            UI = wh/(16*ysm)
        else:
            UI = wh/(30*ysm)
        buffim = pag.screenshot(region = (0,UI,ww/2.1,wh/(16*ylm)))
        buffim.save("./hourlyReport/assets/buffs.png")

        hti.screenshot(html_file='./hourlyReport/index.html', save_as='hourlyReport-resized.png')
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
    disconnect = False
    eb_freeze = False
    for i in range(3):
        #Move to canon:
        if not fast:
            if checkwithOCR("disconnect"):
                return "dc"
            webhook("","Moving to cannon","dark brown")
        time.sleep(1)
        move.hold("w",0.8)
        move.hold("d",0.9*(setdat["hive_number"])+1)
        if ebutton():
            eb_freeze = True
        pag.keyDown("d")
        time.sleep(0.5)
        move.press("space")
        time.sleep(0.2)
        r = ""
        pag.keyUp("d")
        move.hold("w",0.2)
        if ebutton() and eb_freeze:
            webhook("","E button detected. Roblox is frozen", "red",1)
            disconnect = True
            break
        if fast:
            move.hold("d",0.95)
            time.sleep(0.1)
            return
        move.hold("d",0.3)
        for _ in range(6):
            move.hold("d",0.2)
            time.sleep(0.05)
            if "fire" in getBesideE():
                webhook("","Cannon found","dark brown")
                with open('canonfails.txt', 'w') as f:
                    f.write('0')
                f.close()
                return
        mouse.position = (mw//2,mh//5*4)
        reset.reset()
    else:
        webhook("","Cannon failed too many times, rejoining", "red")
        disconnect = True
        
    if disconnect:
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

def collect_mondo_buff():
    webhook("","Travelling: Mondo Buff","dark brown")
    if canon() == "dc": return
    time.sleep(2)
    move.hold("e",0)
    sleep(2.5)
    move.hold("w",1.4)
    move.hold("d",4)
    sleep(120)

def collect_wreath():
    savedata = loadRes()
    setdat = loadsettings.load()
    ww = savedata['ww']
    wh = savedata['wh']
    for _ in range(2):
        webhook("","Travelling: Honey Wreath","dark brown")
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
                for _ in range(3):
                    acchold("s",0.4)
                    acchold("a",0.3)
                    acchold("w",0.4)
                    acchold("d",0.3)
                reset.reset()
                return
        webhook("","Honey Wreath not found, resetting","dark brown",1)
        reset.reset()
    
def convert(bypass=0):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    if not bypass:
        r = False
        for _ in range(2):
            r = "make" in getBesideE()
            if r: break
            time.sleep(0.25)
        if not r: return
    move.press("e")
    if setdat['stinger']:
        move.press(",")
    webhook("","Starting convert","brown",1)
    st = time.perf_counter()
    setStatus("hive")
    while True:
        sh = stingerHunt(1,1)
        if sh == "dc" or sh == "success":
            return
        c = "stop" in getBesideE()
        if not c:
            webhook("","Convert done","brown")
            wait = setdat["convert_wait"]
            if wait: webhook("", f'Waiting for an additional {wait} seconds', "light green")
            time.sleep(wait)
            break
        if time.perf_counter()  - st > 600:
            webhook("","Converting took too long, moving on","brown")
            break
    addStat("convert_time",round((time.perf_counter()  - st)/60,2))
    setStatus()
    if setdat['stinger']:
        move.press(".")
        
def walk_to_hive(field):
    setdat = loadsettings.load()
    hive = setdat['hive_number']
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    webhook("","Going back to hive: {}".format(field.title()),"dark brown")
    exec(open("walk_{}.py".format(field)).read())
    move.hold("a",(hive-1)*0.9)
    for _ in range(50):
        move.hold("a",0.12)
        time.sleep(0.06)
        text = getBesideE()
        if "make" in text:
            convert(1)
            reset.reset()
            return
        
    webhook("","Cant find hive, resetting","dark brown",1)
    reset.reset()
    convert()

def keepOldLoop(claim = True):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    region = (ww/3.15,wh/2.15,ww/2.7,wh/4.2)
    while True:
        ocr = customOCR(*region,0)
        for i in ocr:
            if "kee" in i[1][0].lower():
                mouse.release(Button.left)
                if claim:
                    mouse.position = ((i[0][0][0]+region[0])//2, (i[0][0][1]+region[1])//2)
                    mouse.click(Button.left)
                return
        
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
            if checkRespawn("ladybug_mushroom","5m"):
                addStat("bug_kills",1)
                savetimings("ladybug_mushroom")
        elif cfield == "strawberry":
            if checkRespawn("ladybug_strawberry","5m"):
                addStat("bug_kills",2)
                savetimings("ladybug_strawberry")
        elif cfield == "clover":
            if checkRespawn("ladybug_clover","5m"):
                addStat("bug_kills",2)
                savetimings("ladybug_clover")
                savetimings("rhinobeetle_clover")
        elif cfield == "pumpkin" or cfield == "cactus":
            if checkRespawn("werewolf","1h"):
                addStat("bug_kills",1)
                savetimings("werewolf")
        elif cfield == "pinetree":
            if checkRespawn("werewolf","1h"):
                addStat("bug_kills",1)
                savetimings("werewolf")
            if checkRespawn("mantis_pinetree","20m"):
                addStat("bug_kills",2)
                savetimings("mantis_pinetree")
        elif cfield == "pineapple":
            if checkRespawn("mantis_pineapple","20m"):
                addStat("bug_kills",1)
                savetimings("mantis_pineapple")
            if checkRespawn("rhinobeetle_pineapple","5m"):
                addStat("bug_kills",1)
                savetimings("rhinobeetle_pineapple")
        elif cfield == "spider":
            if checkRespawn("spider_spider","30m"):
                addStat("bug_kills",1)
                savetimings("spider_spider")
        elif cfield == "rose":
            if checkRespawn("scorpion_rose","20m"):
                addStat("bug_kills",2)
                savetimings("scorpion_rose")
        elif cfield == "blueflower":
            if checkRespawn("rhinobeetle_blueflower","5m"):
                addStat("bug_kills",2)
                savetimings("rhinobeetle_blueflower")
        elif cfield == "bamboo":
            if checkRespawn("rhinobeetle_bamboo","5m"):
                addStat("bug_kills",2)
                savetimings("rhinobeetle_bamboo")

def antChallenge():
    webhook("","Travelling: Ant Challenge","dark brown")
    canon()
    exec(open("collect_antpass.py").read())
    move.hold("w",4)
    move.hold("d",1.5)
    move.hold("s",0.4)
    time.sleep(0.5)
    besideE = getBesideE()
    if "spen" in besideE or "play" in besideE:
        webhook("","Start Ant Challenge","bright green",1)
        move.press("e")
        placeSprinkler()
        mouse.press(Button.left)
        time.sleep(1)
        move.hold("s",1.5)
        move.hold("w",0.15)
        move.hold("d",0.3)
        keepOldLoop()
        webhook("","Ant Challenge Complete","bright green",1)
        reset.reset()
        return
    webhook("", "Cant start ant challenge", "red", 1)
    reset.reset()
    return
    
def stingerHunt(convert=0,gathering=0):
    setdat = loadsettings.load()
    fields = ['pepper','mountain top','rose','cactus','spider','clover']
    if not gathering:
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
        time.sleep(1)
        if killvb:
            setStatus("killing_vb")
            st = time.time()
            while True:
                exec(open("killvb_{}.py".format(fieldGoTo)).read())
                status = getStatus()
                if status == "vb_killed":
                    webhook("","Vicious Bee Killed","bright green")
                    addStat("vic_kills", 1)
                    break
                if time.time()-st > 300:
                    webhook("","Took too long to kill vicious bee, leaving","red")
                    break
                if status == "killing_vb_died":
                    webhook("","Died to vicious bee", "red")
                    reset.reset()
                    if canon(1) == "dc": return "dc"
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
        mouse.move(27,102)
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
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    mw,mh = pag.size()
    a = imagesearch.find("yes.png",0.2,0,0,ww,wh)
    multi = 1
    if setdat['display_type'] == "built-in retina display":
        multi = 2
    if a:
        mouse.position = (a[1]//multi+urows//(multi*2),a[2]//multi+ucols//(multi*2))
        time.sleep(1)
        mouse.click(Button.left, 1)    
    mouse.position = (mw/(xsm*2.311),mh/(1.851*ysm))
    time.sleep(1)
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
        move.hold("s",2)
    elif field == "spider":
        move.hold("s",3)
        move.hold("d",4)
    elif field == "sunflower":
        move.hold("d",3)
        move.hold("w",4.5)
        move.hold("a",0.4)
        move.hold("s",0.4)
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
'''
def on_press(key):
    if hasattr(key, "char") and key.char == ('z'):
        print("stopped key pressed")
        _thread.interrupt_main()
        return False
'''
      
def vic():
    try:
        setdat = loadsettings.load()
        fields = ['pepper','mountain','rose','cactus','spider','clover']
        prevHour = datetime.now().hour
        prevMin = datetime.now().minute
        invalid_prev_honey = 1
        honeyHist = [0]*60
        slots_last_used = [0]*7
        while True:
            status = getStatus()
            
            #r = imagesearch.find('disconnect.png',0.7,ww//3,wh//2.8,ww//2.3,wh//2.5)
            currtime = time.time()
            for i in range(len(setdat['slot_enable'])):
                slot_enable = setdat['slot_enable'][i]
                slot_freq = setdat['slot_freq'][i]
                slot_use = setdat['slot_use'][i]
                slot_time = setdat['slot_time'][i]
                if slot_enable and status != "disconnect":
                    if slot_freq == "mins":
                        slot_time*= 60
                    if currtime - slots_last_used[i] < slot_time:
                        continue
                    if slot_use == "gathering" and status != "gathering":
                        continue
                    if slot_use == "hive" and status != "hive":
                        continue
                    move.press(str(i+1))
                    slots_last_used[i] = currtime
                    
                    
                        
            if "gather" in status:
                bluetexts = imToString("blue").lower()
                if "died" in bluetexts:
                    webhook("","Player Died","red")
                    setStatus("died")
                
            elif "vb" in status:
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
            elif setdat['stinger']:
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
                    resetStats()
    except Exception:
        print(traceback.format_exc())
        log(traceback.format_exc())
        webhook("","An error has occured with the background process. Stinger Hunt, Hourly Report and Slot usage are affected. Check terminal/macro logs for error message","red")
        
def killMob(field,mob,reset):
    st = time.perf_counter()
    webhook("","Travelling: {} ({})".format(mob.title(),field.title()),"dark brown")
    convert()
    if canon() == "dc": return
    time.sleep(1)
    exec(open("field_{}.py".format(field)).read())
    if mob == "spider":
        for _ in range(4):
            move.press(",")
    lootMob(field,mob,reset)
    addStat("bug_time", round((time.perf_counter() - st)/60, 2))
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
def get_booster(booster):
    for i in range(2):
        collected = 0
        if canon() == "dc": return
        webhook("","Traveling: {} Booster".format(booster.title()),"dark brown")
        exec(open("collect_{}_booster.py".format(booster)).read())
        if booster == "blue":
            fields = ["pine tree", "blue flower", "bamboo"]
            for _ in range(9):
                move.hold("w",0.15)
                if ebutton():
                    move.press("e")
                    collected = 1
                    break
        elif booster == "red":
            fields = ["rose", "strawberry", "mushroom"]
            for _ in range(2):
                if ebutton():
                    move.press("e")
                    collected = 1
                    break
        else:
            fields = ["sunflower", "dandelion", "spider", "clover", "pineapple", "pumpkin", "cactus"]
            for _ in range(2):
                if ebutton():
                    move.press("e")
                    collected = 1
                    break
                
        savetimings("{}_booster".format(booster))
        if collected:
            sleep(4)
            bluetexts = ""
            for _ in range(3):
                bluetexts += imToString("blue").lower()
            print(bluetexts)
            boostedField = ""
            for f in fields:
                sub_name = f.split(" ")
                for sn in sub_name:
                    if sn in bluetexts:
                        boostedField = f
                        break
                if boostedField: break
            webhook("","Collected: {} Booster.\n Boosted Field: {}".format(booster.title(), boostedField.title()),"bright green",1)
            reset.reset()
            return boostedField
        
        webhook("","Unable To Collect: {} Booster".format((booster.title())),"dark brown",1)
        reset.reset()
    return
            
def collect(name,beesmas=0):
    savedata = loadRes()
    st = time.perf_counter()
    ww = savedata['ww']
    wh = savedata['wh']
    dispname = name.replace("_"," ").title()
    usename = name.replace(" ","")
    claimLoot = 0
    for _ in range(2):
        convert()
        if canon() == "dc": return
        webhook("","Travelling: {}".format(dispname),"dark brown")
        exec(open("collect_{}.py".format(usename)).read())
        
        if usename == "wealthclock" or usename == "samovar":
            for _ in range(6):
                move.hold("w",0.2)
                if "use" in getBesideE():
                    claimLoot = 1
                    break
                
        elif usename == "candles":
            for _ in range(7):
                move.hold("w",0.2)
                if ebutton():
                    claimLoot = 1
                    break
                
        elif usename == "lid_art" or usename == "feast":
            for _ in range(7):
                move.hold("s",0.2)
                if ebutton():
                    claimLoot = 1
                    break
                
        elif usename == "gluedispenser":
            time.sleep(1)
            move.press(str(setdat['gumdrop_slot']))
            time.sleep(2)
            move.hold("w",2.5)
            time.sleep(0.5)
            
        elif usename == "feast":
            if checkwithOCR("bee bear"):
                pag.keyDown("w")
                time.sleep(1)
                move.apkey("space")
                time.sleep(1.5)
                pag.keyUp("w")
        else:
            for _ in range(2):
                besideE = getBesideE()
                if "use" in besideE or "dispenser" in besideE:
                    claimLoot =  1
                    break
        if claimLoot:
            webhook("","Collected: {}".format(dispname),"bright green",1)
            break
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
    addStat("objective_time",round((time.perf_counter() - st)/60,2))
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
    webhook("","Guessed Hive: {}".format(h),"bright green")
    loadsettings.save('hive_number',h)

def clickdialog(t=20):
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    mouse.position = (mw//(2*xsm),round(mh*(4/5*ysm)))
    for _ in range(t):
        mouse.press(Button.left)
        sleep(0.25)
        mouse.release(Button.left)
    
def getQuest(giver):
    setdat = loadsettings.load()
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    pag.typewrite("\\")
    for _ in range(5):
        keyboard.press(Key.up)
        time.sleep(0.05)
        keyboard.release(Key.up)
        time.sleep(0.1)   
    keyboard.press(Key.down)
    time.sleep(0.05)
    keyboard.release(Key.down)
    move.press("enter")
    keyboard.press(Key.down)
    time.sleep(0.05)
    keyboard.release(Key.down)
    for _ in range(10):
        keyboard.press(Key.page_up)
        time.sleep(0.02)
        keyboard.release(Key.page_up)
        time.sleep(0.01)

    q_title = ""
    for _ in range(10):
        ocr = customOCR(0,wh/(7*ysm),ww/(4.5*xsm),wh/2,0)
        lines = [x[1][0].lower() for x in ocr]
        for i in lines:
            if giver in i:
                if ":" in i: i  = i.split(":")[1]
                q_title = i.replace(giver,"").replace("bear","")
                break
        if q_title:
            break
        for _ in range(2):
            keyboard.press(Key.page_down)
            time.sleep(0.02)
            keyboard.release(Key.page_down)

    keyboard.press(Key.up)
    time.sleep(0.05)
    keyboard.release(Key.up)
    move.press("enter")
    pag.typewrite("\\")
    if not q_title: return False

    highest_match = [0,"",[]]
    for k,v in questData[giver].items():
        match = SequenceMatcher(None, k, q_title).ratio()
        if match > highest_match[0]:
            highest_match[0] = match
            highest_match[1] = k
            highest_match[2] = v
    webhook('',f'Quest detected: {highest_match[1]}',"light blue")

    if setdat["haste_compensation"]: openSettings()
    return highest_match[2]
    
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
    for _ in range(26):
        keyboard.press(Key.page_down)
        time.sleep(0.02)
        keyboard.release(Key.page_down)
    time.sleep(0.5)
    for _ in range(1):
        keyboard.press(Key.page_up)
        time.sleep(0.02)
        keyboard.release(Key.page_up)
    for _ in range(8):
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
    msh = mp['msh']
    msy = mp['msy']
    ww = loadRes()['ww']
    if str(msh) == "-1": return
    ocr = customOCR(ww/8,msy,ww/10,msh)
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
        webbrowser.open(link, new = 2)
    elif rm == "reload":
        webbrowser.open(link, new = 2)
        time.sleep(2)
        with keyboard.pressed(Key.cmd):
            keyboard.press('r')
            time.sleep(0.1)
            keyboard.release('r')
    elif rm == "copy paste":
        webbrowser.open("https://docs.python.org/3/library/webbrowser.html", autoraise=True, new = 2)
        time.sleep(3)
        with keyboard.pressed(Key.cmd):
            keyboard.press('t')
            keyboard.release('t')
        time.sleep(1)
        keyboard.type(link)
        time.sleep(0.5)
        with keyboard.pressed(Key.cmd):
            keyboard.press('a')
            time.sleep(0.1)
            keyboard.release('a')
            time.sleep(0.3)
            keyboard.press('c')
            time.sleep(0.1)
            keyboard.release('c')
            time.sleep(0.3)
            keyboard.press('w')
            time.sleep(0.1)
            keyboard.release('w')
            time.sleep(0.5)
            keyboard.press('t')
            time.sleep(0.1)
            keyboard.release('t')
            time.sleep(1)
            keyboard.press('v')
            time.sleep(0.1)
            keyboard.release('v')
        time.sleep(1)
        keyboard.press(Key.enter)
        
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
    st = time.perf_counter()
    for i in range(3):
        savedata = loadRes()
        ww = savedata['ww']
        wh = savedata['wh']
        webhook("","Rejoining","dark brown",1)
        time.sleep(3)
        subprocess.run(['pkill', '-9', '"Roblox"'])
        cmd = """
            osascript -e 'quit application "Roblox"'
        """
        os.system(cmd)
        subprocess.Popen("osascript -e 'quit app \"Roblox\"'", shell=True)
        time.sleep(3)
        ps = setdat["private_server_link"]
        if setdat["rejoin_method"] == "deeplink":
            deeplink = "roblox://placeID=1537690962"
            if ps and i < 2:
                deeplink += f"&linkCode={ps.lower().split('code=')[1]}"
            subprocess.call(["open", deeplink])
            
        elif ps and i < 2:
            openRoblox(setdat["private_server_link"])
        else:
            openRoblox('https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129')
            time.sleep(10)
                
        time.sleep(setdat['rejoin_delay']*(i+1))
        if not is_running("roblox"):
            webhook("","Roblox is not running, waiting for another min", "red", 1)
            time.sleep(60)
        cmd = """
            osascript -e 'activate application "Roblox"' 
        """
        os.system(cmd)
        time.sleep(1)
        if setdat['manual_fullscreen']:
            menubarRaw = customOCR(0, 0, 300, 60, 0)
            menubar = ""
            try:
                for x in menubarRaw:
                    menubar += x[1][0]
            except:
                pass
            menubar = menubar.lower()
            if "rob" in menubar or "lox" in menubar:
                webhook("","Roblox is not in fullscreen, activating fullscreen", "dark brown",1)
                fullscreen()
            else:
                webhook("","Roblox is already in fullscreen, not activating fullscreen", "dark brown",1)
        time.sleep(2)
        webbrowser.open("https://docs.python.org/3/library/webbrowser.html", autoraise=True)
        time.sleep(0.5)
        for _ in range(2):
            with keyboard.pressed(Key.cmd):
                keyboard.press('w')
                time.sleep(0.1)
                keyboard.release('w')
            time.sleep(0.5)
        cmd = """
                osascript -e 'activate application "Roblox"' 
            """
        os.system(cmd)
        move.hold("w",5,0)
        move.hold("w",i*2,0)
        move.hold("s",0.6,0)
        time.sleep(0.5)
        webhook("","Finding Hive", "dark brown",1)
        move.hold("d",4)
        for j in range(40):
            move.hold("a",0.4)
            time.sleep(0.06)
            text = getBesideE()
            if "claim" in text:
                move.press("e")
                print(j)
                print((j+1)//2)
                updateHive(max(1,min(6,(j+1)//2)))
                convert()
                webhook("","Rejoin successful","dark brown")
                currentTime = datetime.now().strftime("%H:%M")
                if setdat["so_broke"]:
                    pag.typewrite("/")
                    pag.typewrite(f'Existance so broke :weary: {currentTime}', interval = 0.04)
                    keyboard.press(Key.enter)
                if setdat['haste_compensation']: openSettings()
                addStat("rejoin_time", round((time.perf_counter() - st)/60, 2))
                return
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
    settings = loadsettings.load()
    with open(f"./profiles/{settings['current_profile']}/fieldsettings.txt","r") as f:
        fields = ast.literal_eval(f.read())
    f.close()
    if str(gfid).isdigit():
        gfid = int(gfid)
        currfield = loadsettings.load()['gather_field'][gfid]
    else:
        currfield =  gfid
    setdat = fields[currfield]
    for key in setdat:
        val = str(setdat[key])
        if val.isdigit():
            setdat[key] = int(val)
        elif "." in val:
            setdat[key] = float(val)
        else:
            setdat[key] = val.lower()
    canon()
    if getStatus() == "disconnect": return
    webhook("","Travelling: {}".format(currfield.title()),"dark brown")
    exec(open("field_{}.py".format(currfield)).read())
    cf = currfield.replace(" ","").lower()
    time.sleep(0.2)
    s_l = setdat['start_location'].lower()
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
        
        move.hold("w",setdat['distance_from_center']/2.5)
        
        for i in rotBack:
            move.press(i)

       
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
    webhook("Gathering: {}".format(currfield),"Limit: {}.00 - {} - Backpack: {}%".format(setdat["gather_time"],setdat["gather_pattern"],setdat["pack"]),"light green")
    setStatus("gathering")
    time.sleep(0.2)
    timestart = time.perf_counter()
    fullTime = 0
    stingerFound = 0
    end_gather = 0
    bpcap = 0
    cycleCount = 0
    prev_bp = 0
    repeat_bp = 0
    while not end_gather:
        time.sleep(0.05)
        mouse.press(Button.left)
        if setdat['shift_lock']: pag.press('shift')
        exec(open("gather_{}.py".format(gp)).read())
        resetMobTimer(cf.lower())
        timespent = (time.perf_counter() - timestart)/60
        status = getStatus()
        if bpcap >= setdat["pack"]:
            webhook("Gathering: ended","Time: {:.2f} - Backpack - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
            end_gather = 1
            break
        if timespent > setdat["gather_time"]:
            webhook("Gathering: ended","Time: {:.2f} - Time Limit - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
            end_gather = 1
            break
        if status == "died":
            webhook("Gathering: ended","Time: {:.2f} - Died - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
            end_gather = 1
            setdat['return_to_hive'] = "reset"
            break
        if status == "disconnect": return
        
        if setdat['field_drift_compensation'] and gp != "stationary":
            fieldDriftCompensation()
        if setdat['shift_lock']: pag.press('shift')
        shv = stingerHunt(0,1)
        if  shv == "success":
            stingerFound = 1
            break
        if not cycleCount%20:
            if checkwithOCR("disconnect"): return
            
        if not cycleCount%2:
            bpcap = backpack.bpc()
            if bpcap == prev_bp and prev_bp != 0:
                repeat_bp += 1
            else:
                prev_bp = bpcap
                repeat_bp = 0
        if settings["backpack_freeze"]:
            if repeat_bp >= 15:
                setStatus("disconnect")
                webhook("","Backpack has not changed. Roblox is frozen","red")
                addStat("gather_time",round(timespent,2))
                return 
        mouse.release(Button.left)
        cycleCount += 1
    time.sleep(0.5)
    setStatus()
    addStat("gather_time",round(timespent,2))
    if not stingerFound:
        if setdat["before_gather_turn"] == "left":
            for _ in range(setdat["turn_times"]):
                move.press(".")
        elif setdat["before_gather_turn"] == "right":
            for _ in range(setdat["turn_times"]):
                move.press(",")
        print(setdat['return_to_hive'])
        if setdat['return_to_hive'] == "walk":
            walk_to_hive(currfield)
        elif setdat['return_to_hive'] == "reset":
            reset.reset()
            convert()
        elif setdat['return_to_hive'] == "rejoin":
            rejoin()
            convert()
            reset.reset()
        elif setdat['return_to_hive'] == "whirligig":
            webhook("","Activating whirligig","dark brown")
            if setdat['whirligig_slot'] == "none":
                webhook("Notice","Whirligig option selected but no whirligig slot given, walking back","red")
                walk_to_hive(currfield)
            else:
                move.press(str(setdat['whirligig_slot']))
                time.sleep(2)
                r = 0
                for _ in range(2):
                    if ebutton():
                        r = 1
                if r:
                    convert()
                    reset.reset()
                else:
                    webhook("Notice","Whirligig failed to activate, walking back","red")
                    walk_to_hive(currfield)
    stingerHunt()

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
    global invalid_prev_honey, quest_kills, quest_gathers
    setStatus()
    userset = loadsettings.load()
    setdat = userset
    val = validateSettings()
    setStatus()
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    with open('canonfails.txt', 'w') as f:
        f.write('0')
    f.close()
    resetAllStats()
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
        setdat = userset
        #quests
        if setdat["polar_quest"]:
            #check if quest done, else read curr quest
            if session_start:
                for _ in range(2):
                    canon()
                    webhook("","Travelling: Polar Bear (quest) ","brown")
                    exec(open("quest_polar.py").read())
                    sleep(0.5)
                    if ebutton():
                        move.press("e")
                        sleep(0.2)
                        move.press("e")
                        break
                    reset.reset()
                    sleep(0.7)
                clickdialog()
                quest = getQuest("polar")
                polar_quest = {}
                reset.reset()
                print(quest)
                for i in quest:
                    if i.startswith("gather"):
                        f = i.split("_")[1]
                        quest_gathers[f] = ["polar", 0, 1]
                    elif i.startswith("kill"):
                        _,c,m = i.split("_")
                        setdat[i.split("_")[2]] = 1
                        quest_kills[m] = ["polar",0, int(c)]
                
                
                
            
        #Stump snail check
        if setdat['stump_snail'] and checkRespawn("stump_snail","96h"):
            canon()
            webhook("","Travelling: Stump snail (stump) ","brown")
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
        if getStatus() == "disconnect": return
        
        if setdat['wealthclock']  and checkRespawn('wealthclock',"1h"):
            print("hello")
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
            collect_wreath()
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

        if setdat['antpass'] and checkRespawn('antpass','2h'):
            collect('antpass')
            stingerHunt()
            if getStatus() == "disconnect": return
            
        if setdat['ant_challenge']:
            antChallenge()
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
                collect_mondo_buff()
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
                    webhook('',"Travelling: {} ({})\nObjective: Place Planter".format(displayPlanterName(bestPlanter),planterFields[i].title()),"dark brown")
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
                            webhook('',"Travelling: {} ({})\nObjective: Collect Planter, Attempt: {}".format(displayPlanterName(currPlanter),currField.title(),i+1),"dark brown")
                            getBeside = getBesideE()
                            if "harv" in getBeside or "plant" in getBeside:
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
                    webhook('',"Travelling: {} ({})\nObjective: Place Planter".format(displayPlanterName(bestPlanter),i.title()),"dark brown")
                    goToPlanter(i,1)
                    if getStatus() == "disconnect": return
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
            stingerHunt()
            if getStatus() == "disconnect": return

        if setdat['blue_booster'] and checkRespawn("blue_booster","1h"):
            boostedField = get_booster("blue")
            print(boostedField)
            if boostedField and setdat['gather_in_boosted']:
                st = time.time()
                while time.time() -st < 900:
                    gather(boostedField)
                    if getStatus() == "disconnect": return
        if setdat['red_booster'] and checkRespawn("red_booster","1h"):
            boostedField = get_booster("red")
            print(boostedField)
            if boostedField and setdat['gather_in_boosted']:
                st = time.time()
                while time.time() -st < 900:
                    gather(boostedField)
                    stingerHunt()
                    if getStatus() == "disconnect": return
            
            stingerHunt()
            if getStatus() == "disconnect": return
        if setdat['mountain_booster'] and checkRespawn("mountain_booster","1h"):
            boostedField = get_booster("mountain")
            print(boostedField)
            if boostedField and setdat['gather_in_boosted']:
                st = time.time()
                while time.time() -st < 900:
                    gather(boostedField)
                    if getStatus() == "disconnect": return
            stingerHunt()
            if getStatus() == "disconnect": return
            
        #gather check
        if setdat['gather_enable']:
            gather(gfid)
            if getStatus() == "disconnect": return
            gfid += 1
            while True:
                if gfid >= len(setdat['gather_field']):
                    gfid = 0
                    
                f = setdat["gather_field"][gfid].lower()
                if f in quest_gathers:
                    quest_gathers.remove(f)
                if f == "none":
                    gfid += 1
                else: break
                
        else:
            mouse.click(Button.left, 1)

        if quest_gathers:
            for i in quest_gathers:
                gather(i)
                if getStatus() == "disconnect": return
        

            


def setResolution():
    global warnings
    wwd = int(pag.size()[0])
    whd = int(pag.size()[1])
    warnings = []
    scw = "\nScreen Coordinates not found in supported list. Contact Existance to get it supported."
    if retina:
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
        "3840x2160": [1.08,0.92,1.3,1.5],
        "3456x2234": [1.2, 0.93, 1.3, 1.6],
        "2560x1600": [0.9, 1.02, 1, 1.1],
        "2560x1440": [1.45,0.87,1.8,2.2],
        "5120x2880": [1.4,0.87,1.7,2],
        "3420x2224":[0.81, 0.95, 1.12, 1.24],
        "3840x2486": [1.3, 0.92, 1.45, 1.45],
        "3420x2214":[0.9, 0.95, 1.1, 1.15]
        }
    if ndisplay in multiInfo:
        loadsettings.save("y_screenshot_multiplier",multiInfo[ndisplay][0],"multipliers.txt")
        loadsettings.save("x_screenshot_multiplier",multiInfo[ndisplay][1],"multipliers.txt")
        loadsettings.save("y_length_multiplier",multiInfo[ndisplay][2],"multipliers.txt")
        loadsettings.save("x_length_multiplier",multiInfo[ndisplay][3],"multipliers.txt")
    else:
        scw+= "Your screen coordinates are: {}".format(ndisplay)
        warnings.append(scw)
        pag.alert(scw)
    if warnings:
        print("\033[0;31mWarnings:\n{}\033[00m".format(warnings))
if __name__ == "__main__":
    global show_haste_warn
    with open('macroLogs.log', 'w'):
        pass
    with open('firstRun.txt', 'w') as f:
        f.write("1")
    f.close()
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = bool(subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True).communicate()[0])
    
    print("\033[0;32mTo stop the macro\033[00m")
    print("tab out of roblox, make sure terminal is in focus and press ctrl c\nor,\nright click the macro app in the dock and force quit")
    print("\n\nYour python version is {}".format(python_ver))
    print("Your macro version is {}\n\n".format(macrov))
    log("Your macro version is {}\n\n".format(macrov))
    time.sleep(5)
    setResolution()
    loadSave()
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
    s.configure('small.TButton', font=('Helvetica', 12))

    def updateProfile(profile = None):
        reference = loadsettings.loadFile(f"./src/default settings/settings.txt")
        if not profile:
            profile = loadsettings.loadFile("generalsettings.txt")["current_profile"]

        originalPath = f"./profiles/{profile}/settings.txt"
        original = loadsettings.loadFile(originalPath)
        out = []
        for i in reference.keys():
            if not i in original:
                original[i] = reference[i]
            out.append(f"{i}:{original[i]}")
        with open(originalPath, "w") as f:
            f.write("\n".join(out))
        f.close()
        
    updateProfile()
    
    setdat = loadsettings.load()
    plantdat = loadsettings.planterLoad()
    with open(f"./profiles/{setdat['current_profile']}/fieldsettings.txt","r") as f:
        fields = ast.literal_eval(f.read())
    f.close()
            
    def loadSettings(profile):
        global setdat, plantdat, fields
        setdat = loadsettings.load(profile = profile)
        plantdat = loadsettings.planterLoad(profile)
        with open(f"./profiles/{profile}/fieldsettings.txt","r") as f:
            fields = ast.literal_eval(f.read())
        f.close()
    # create frames
    frame1 = ttk.Frame(notebook, width=780, height=460)
    frame2 = ttk.Frame(notebook, width=780, height=460)
    frame3 = ttk.Frame(notebook, width=780, height=460)
    frame4 = ttk.Frame(notebook, width=780, height=460)
    frame6 = ttk.Frame(notebook, width=780, height=460)
    frame7 = ttk.Frame(notebook, width=780, height=460)
    frame5 = ttk.Frame(notebook, width=780, height=460)
    #frame8 = ttk.Frame(notebook, width=780, height=460)
    frame9 = ttk.Frame(notebook, width=780, height=460)
    
    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    frame3.pack(fill='both', expand=True)
    frame4.pack(fill='both', expand=True)
    frame6.pack(fill='both', expand=True)
    frame7.pack(fill='both', expand=True)
    frame5.pack(fill='both', expand=True)
    #frame8.pack(fill='both', expand=True)
    frame9.pack(fill='both', expand=True)

    notebook.add(frame1, text='Gather')
    notebook.add(frame2, text='Bug run')
    notebook.add(frame4, text='Collect')
    notebook.add(frame5, text='Boost')
    notebook.add(frame6, text='Planters')
    #notebook.add(frame8, text='Quests')
    notebook.add(frame3, text='In Game Settings')
    notebook.add(frame7, text='Other Settings')
    notebook.add(frame9, text='Profile')    

    #get variables
    gather_enable = tk.IntVar(value=setdat["gather_enable"])
    gather_field_one = tk.StringVar(root)
    gather_field_two = tk.StringVar(root)
    gather_field_three = tk.StringVar(root)

    return_to_hive_one = tk.StringVar(root)
    return_to_hive_two = tk.StringVar(root)
    return_to_hive_three = tk.StringVar(root)
    gather_pattern_one = tk.StringVar(root)
    gather_pattern_two = tk.StringVar(root)
    gather_pattern_three = tk.StringVar(root)
    gather_size_one = tk.StringVar(root)
    gather_size_two = tk.StringVar(root)
    gather_size_three = tk.StringVar(root)
    gather_width_one = tk.IntVar(value=1)
    gather_width_two = tk.IntVar(value=1)
    gather_width_three = tk.IntVar(value=1)
    before_gather_turn_one = tk.StringVar(root)
    before_gather_turn_two = tk.StringVar(root)
    before_gather_turn_three = tk.StringVar(root)
    turn_times_one = tk.IntVar(value=1)
    turn_times_two = tk.IntVar(value=1)
    turn_times_three = tk.IntVar(value=1)
    start_location_one = tk.StringVar(root)
    start_location_two = tk.StringVar(root)
    start_location_three = tk.StringVar(root)
    distance_from_center_one = tk.StringVar(root)
    distance_from_center_two = tk.StringVar(root)
    distance_from_center_three = tk.StringVar(root)
    whirligig_slot_one = tk.StringVar(root)
    whirligig_slot_two = tk.StringVar(root)
    whirligig_slot_three = tk.StringVar(root)
    field_drift_compensation_one = tk.IntVar(value=1)
    field_drift_compensation_two = tk.IntVar(value=1)
    field_drift_compensation_three = tk.IntVar(value=1)
    shift_lock_one = tk.IntVar(value=1)
    shift_lock_two = tk.IntVar(value=1)
    shift_lock_three = tk.IntVar(value=1)
    

    def fieldOne(value):
        setdat = fields[value.lower()]
        return_to_hive_one.set(setdat["return_to_hive"].title())
        gather_pattern_one.set(setdat["gather_pattern"])
        gather_size_one.set(setdat["gather_size"].title())
        gather_width_one.set(value=setdat["gather_width"])
        gather_time_one = fields[value.lower()]["gather_time"]
        before_gather_turn_one.set(setdat["before_gather_turn"])
        turn_times_one.set(value=setdat["turn_times"])
        start_location_one.set(setdat["start_location"].title())
        distance_from_center_one.set(setdat["distance_from_center"])
        whirligig_slot_one.set(setdat["whirligig_slot"])
        field_drift_compensation_one.set(value=setdat["field_drift_compensation"])
        shift_lock_one.set(value=setdat['shift_lock'])
        
        timetextbox_one.delete("1.0", 'end')
        timetextbox_one.insert("end",gather_time_one)
        packtextbox_one.delete("1.0", 'end')
        packtextbox_one.insert("end",setdat["pack"])
        
    
    def fieldTwo(value):
        setdat = fields[value.lower()]
        return_to_hive_two.set(setdat["return_to_hive"].title())
        gather_pattern_two.set(setdat["gather_pattern"])
        gather_size_two.set(setdat["gather_size"].title())
        gather_width_two.set(value=setdat["gather_width"])
        gather_time_two = fields[value.lower()]["gather_time"]
        before_gather_turn_two.set(setdat["before_gather_turn"])
        turn_times_two.set(value=setdat["turn_times"])
        start_location_two.set(setdat["start_location"].title())
        distance_from_center_two.set(setdat["distance_from_center"])
        whirligig_slot_two.set(setdat["whirligig_slot"])
        field_drift_compensation_two.set(value=setdat["field_drift_compensation"])
        shift_lock_two.set(value=setdat['shift_lock'])
        
        timetextbox_two.delete("1.0", 'end')
        timetextbox_two.insert("end",gather_time_two)
        packtextbox_two.delete("1.0", 'end')
        packtextbox_two.insert("end",setdat["pack"])
        
    def fieldThree(value):
        setdat = fields[value.lower()]
        return_to_hive_three.set(setdat["return_to_hive"].title())
        gather_pattern_three.set(setdat["gather_pattern"])
        gather_size_three.set(setdat["gather_size"].title())
        gather_width_three.set(value=setdat["gather_width"])
        gather_time_three = fields[value.lower()]["gather_time"]
        before_gather_turn_three.set(setdat["before_gather_turn"])
        turn_times_three.set(value=setdat["turn_times"])
        start_location_three.set(setdat["start_location"].title())
        distance_from_center_three.set(setdat["distance_from_center"])
        whirligig_slot_three.set(setdat["whirligig_slot"])
        field_drift_compensation_three.set(value=setdat["field_drift_compensation"])
        shift_lock_three.set(value=setdat['shift_lock'])
        
        timetextbox_three.delete("1.0", 'end')
        timetextbox_three.insert("end",gather_time_three)
        packtextbox_three.delete("1.0", 'end')
        packtextbox_three.insert("end",setdat["pack"])

      
    stump_snail = tk.IntVar()
    continue_after_stump_snail = tk.IntVar()
    ladybug = tk.IntVar()
    rhinobeetle = tk.IntVar()
    werewolf = tk.IntVar()
    scorpion = tk.IntVar()
    spider = tk.IntVar()
    mantis = tk.IntVar()
    stinger = tk.IntVar()
    gifted_vicious_bee = tk.IntVar()
    enable_discord_webhook = tk.IntVar()
    discord_webhook_url= ""
    send_screenshot  = tk.IntVar()
    walkspeed = ""
    hive_number = tk.IntVar()
    display_type = tk.StringVar(root)
    new_ui = tk.IntVar()
    private_server_link = ""
    enable_discord_bot = tk.IntVar()
    sprinkler_slot = tk.StringVar(root)
    sprinkler_type = tk.StringVar(root)
    discord_bot_token = ""
    haste_compensation = tk.IntVar()

    rejoin_every_enabled = tk.IntVar()
    rejoin_every = setdat['rejoin_every']
    rejoin_delay = setdat['rejoin_delay']
    rejoin_method = tk.StringVar(root)
    manual_fullscreen = tk.IntVar()
    
    convert_wait = ""
    #convert_every_enabled = tk.IntVar()
    #convert_every = ""
    
    wealthclock = tk.IntVar()
    blueberrydispenser = tk.IntVar()
    strawberrydispenser = tk.IntVar()
    royaljellydispenser  = tk.IntVar()
    treatdispenser = tk.IntVar()
    gluedispenser = tk.IntVar()
    gumdrop_slot = tk.StringVar(root)
    stockings = tk.IntVar()
    feast = tk.IntVar()
    samovar = tk.IntVar()
    wreath = tk.IntVar()
    snow_machine = tk.IntVar()
    mondo_buff = tk.IntVar()
    lid_art = tk.IntVar()
    candles = tk.IntVar()
    antpass = tk.IntVar()
    antchallenge = tk.IntVar()

    blue_booster = tk.IntVar()
    red_booster = tk.IntVar()
    mountain_booster = tk.IntVar()
    gather_in_boosted = tk.IntVar()

    polar_quest = tk.IntVar()

    backpack_freeze = tk.IntVar()
    
    canon_time = ""
    reverse_hive_direction = tk.IntVar()
    so_broke = tk.IntVar()

    enable_planters = tk.IntVar()
    paper_planter = tk.IntVar()
    ticket_planter = tk.IntVar()
    plastic_planter = tk.IntVar()
    candy_planter = tk.IntVar()
    blueclay_planter = tk.IntVar()
    redclay_planter = tk.IntVar()
    tacky_planter = tk.IntVar()
    pesticide_planter = tk.IntVar()
    heattreated_planter = tk.IntVar()
    hydroponic_planter = tk.IntVar()
    petal_planter = tk.IntVar()
    plenty_planter = tk.IntVar()
    festive_planter = tk.IntVar()
    paper_slot = tk.StringVar(root)
    ticket_slot = tk.StringVar(root)
    plastic_slot = tk.StringVar(root)
    candy_slot = tk.StringVar(root)
    blueclay_slot = tk.StringVar(root)
    redclay_slot = tk.StringVar(root)
    tacky_slot = tk.StringVar(root)
    pesticide_slot = tk.StringVar(root)
    heattreated_slot = tk.StringVar(root)
    hydroponic_slot = tk.StringVar(root)
    petal_slot = tk.StringVar(root)
    plenty_slot = tk.StringVar(root)
    festive_slot = tk.StringVar(root)
    harvest = plantdat['harvest']
    planter_count = tk.StringVar(root)
    show_haste_warn = ""
    harvest_full = tk.IntVar()
    harvest_auto = tk.IntVar()
    harvest_int = 0
    planter_fields = []

    current_profile = tk.StringVar(root)

    def loadVariables():
        global walkspeed, discord_webhook_url, private_server_link, discord_bot_token, planter_fields,convert_wait

        gather_field_one.set(setdat["gather_field"][0].title())
        gather_field_two.set(setdat["gather_field"][1].title())
        gather_field_three.set(setdat["gather_field"][2].title())

        stump_snail.set(setdat["stump_snail"])
        continue_after_stump_snail.set(setdat["continue_after_stump_snail"])
        ladybug.set(setdat["ladybug"])
        rhinobeetle.set(setdat["rhinobeetle"])
        werewolf.set(setdat["werewolf"])
        scorpion.set(setdat["scorpion"])
        spider.set(setdat["spider"])
        mantis.set(setdat["mantis"])
        stinger.set(setdat["stinger"])
        gifted_vicious_bee.set(setdat["gifted_vicious_bee"])
        enable_discord_webhook.set(setdat["enable_discord_webhook"])
        discord_webhook_url= setdat["discord_webhook_url"]
        send_screenshot.set(setdat["send_screenshot"])
        walkspeed = setdat["walkspeed"]
        hive_number.set(setdat["hive_number"])
        display_type.set(setdat["display_type"].capitalize())
        new_ui.set(setdat["new_ui"])
        private_server_link = setdat["private_server_link"]
        enable_discord_bot.set(setdat["enable_discord_bot"])
        sprinkler_slot.set(setdat["sprinkler_slot"])
        sprinkler_type.set(setdat["sprinkler_type"].title())
        discord_bot_token = setdat['discord_bot_token']
        haste_compensation.set(setdat["haste_compensation"])

        rejoin_every_enabled.set(setdat["rejoin_every_enabled"])
        rejoin_every = setdat['rejoin_every']
        rejoin_delay = setdat['rejoin_delay']
        rejoin_method.set(setdat['rejoin_method'])
        manual_fullscreen.set(setdat['manual_fullscreen'])
        
        convert_wait = setdat['convert_wait']
        #convert_every_enabled.set(setdat["convert_every_enabled"])
        #convert_every = setdat['convert_every']
        
        wealthclock.set(setdat["wealthclock"])
        blueberrydispenser.set(setdat["blueberrydispenser"])
        strawberrydispenser.set(setdat["strawberrydispenser"])
        royaljellydispenser.set(setdat["royaljellydispenser"])
        treatdispenser.set(setdat["treatdispenser"])
        gluedispenser.set(setdat["gluedispenser"])
        gumdrop_slot.set(setdat["gumdrop_slot"])
        stockings.set(setdat["stockings"])
        feast.set(setdat["feast"])
        samovar.set(setdat["samovar"])
        wreath.set(setdat["wreath"])
        snow_machine.set(setdat["snow_machine"])
        mondo_buff.set(setdat["mondo_buff"])
        lid_art.set(setdat["lid_art"])
        candles.set(setdat["candles"])
        antpass.set(setdat["antpass"])
        antchallenge.set(setdat["ant_challenge"])

        blue_booster.set(setdat["blue_booster"])
        red_booster.set(setdat["red_booster"])
        mountain_booster.set(setdat["mountain_booster"])
        gather_in_boosted.set(setdat["gather_in_boosted"])

        polar_quest.set(setdat["polar_quest"])

        backpack_freeze.set(setdat["backpack_freeze"])
        
        canon_time = setdat['canon_time']
        reverse_hive_direction.set(setdat['reverse_hive_direction'])
        so_broke.set(setdat['so_broke'])

        enable_planters.set(plantdat['enable_planters'])
        paper_planter.set(plantdat['paper_planter'])
        ticket_planter.set(plantdat['ticket_planter'])
        plastic_planter.set(plantdat['plastic_planter'])
        candy_planter.set(plantdat['candy_planter'])
        blueclay_planter.set(plantdat['blueclay_planter'])
        redclay_planter.set(plantdat['redclay_planter'])
        tacky_planter.set(plantdat['tacky_planter'])
        pesticide_planter.set(plantdat['pesticide_planter'])
        heattreated_planter.set(plantdat['heattreated_planter'])
        hydroponic_planter.set(plantdat['hydroponic_planter'])
        petal_planter.set(plantdat['petal_planter'])
        plenty_planter.set(plantdat['plenty_planter'])
        festive_planter.set(plantdat['festive_planter'])
        paper_slot.set(plantdat['paper_slot'])
        ticket_slot.set(plantdat['ticket_slot'])
        plastic_slot.set(plantdat['plastic_slot'])
        candy_slot.set(plantdat['candy_slot'])
        blueclay_slot.set(plantdat['blueclay_slot'])
        redclay_slot.set(plantdat['redclay_slot'])
        tacky_slot.set(plantdat['tacky_slot'])
        pesticide_slot.set(plantdat['pesticide_slot'])
        heattreated_slot.set(plantdat['heattreated_slot'])
        hydroponic_slot.set(plantdat['hydroponic_slot'])
        petal_slot.set(plantdat['plenty_slot'])
        plenty_slot.set(plantdat['plenty_slot'])
        festive_slot.set(plantdat['festive_slot'])
        harvest = plantdat['harvest']
        planter_count.set(plantdat['planter_count'])
        show_haste_warn = setdat['show_haste_warn']
        harvest_full.set(boolToInt(str(harvest)=="full"))
        harvest_auto.set(boolToInt(str(harvest)=="auto"))
        harvest_int = plantdat['harvest']
        slot_options = ["none"]+[x+1 for x in range(7)]
        planter_fields = plantdat['planter_fields']

        #current_profile.set(setdat["current_profile"])

    multipliers = loadsettings.load('multipliers.txt')
    loadVariables()
    
    slot_options = ["none"]+[x+1 for x in range(7)]
    gather_fields = [x.split("_")[1][:-3].title() for x in os.listdir("./") if x.startswith("field_")]
    gather_fields.insert(0,"None")
    field_options = tk.Variable(value=[x.split("_")[1][:-3].title() for x in os.listdir("./") if x.startswith("field_")])
    profiles = []

    def loadTextBoxes():
        slottextbox_one.delete("1.0", tk.END)
        slottextbox_one.insert("end",setdat['slot_time'][0])
        slottextbox_two.delete("1.0", tk.END)
        slottextbox_two.insert("end",setdat['slot_time'][1])
        slottextbox_three.delete("1.0", tk.END)
        slottextbox_three.insert("end",setdat['slot_time'][2])
        slottextbox_four.delete("1.0", tk.END)
        slottextbox_four.insert("end",setdat['slot_time'][3])
        slottextbox_five.delete("1.0", tk.END)
        slottextbox_five.insert("end",setdat['slot_time'][4])
        slottextbox_six.delete("1.0", tk.END)
        slottextbox_six.insert("end",setdat['slot_time'][5])
        slottextbox_seven.delete("1.0", tk.END)
        slottextbox_seven.insert("end",setdat['slot_time'][6])

        harvesttextbox.delete("1.0", tk.END)
        harvesttextbox.insert("end",plantdat['harvest'])

        convertwaittextbox.delete("1.0", tk.END)
        convertwaittextbox.insert("end",setdat["convert_wait"])

        rejoinetextbox.delete("1.0", tk.END)
        rejoinetextbox.insert("end",setdat["rejoin_every"])

    def reloadProfileList(updateOptions = True):
        global profiles
        profiles = [x for x in os.listdir("./profiles") if "." not in x]
        if not updateOptions: return
        menu = profileField["menu"]
        menu.delete(0, "end")
        for i in profiles:
            menu.add_command(label=i, 
                             command=lambda value=i: current_profile.set(value))
    reloadProfileList(False)
    for i,e in enumerate(setdat['slot_enable']):
        globals()['slot_enable_%s' % (i+1)] = tk.IntVar(value=e)
        
    for i,e in enumerate(setdat['slot_freq']):
        globals()['slot_freq_%s' % (i+1)] = tk.StringVar(root)
        globals()['slot_freq_%s' % (i+1)].set(e)
    print(setdat['slot_use'])
    for i,e in enumerate(setdat['slot_use']):
        globals()['slot_use_%s' % (i+1)] = tk.StringVar(root)
        globals()['slot_use_%s' % (i+1)].set(e)


    
    wwa  = savedata['ww']
    wha = savedata['wh']

            
    def updateGo():
        update.update()
        exit()
    def updateExp():
        uupdate.update("e")
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
    def saveFields(e = ""):
        global fields
        fields[gather_field_one.get().lower()] = {'gather_pattern': gather_pattern_one.get(),
                                          'gather_size': gather_size_one.get(),
                                          'gather_width': gather_width_one.get(),
                                          'gather_time': timetextbox_one.get(1.0,"end").replace("\n",""),
                                          'pack': packtextbox_one.get(1.0,"end").replace("\n",""),
                                          'before_gather_turn': before_gather_turn_one.get(),
                                          'turn_times': turn_times_one.get(),
                                          'return_to_hive': return_to_hive_one.get(),
                                          'whirligig_slot': whirligig_slot_one.get(),
                                          'start_location': start_location_one.get(),
                                          'distance_from_center': distance_from_center_one.get(),
                                          'field_drift_compensation': field_drift_compensation_one.get(),
                                          'shift_lock': shift_lock_one.get()

                                                  }
        if gather_field_two.get().lower() != "none":
            print('saved field 2')
            fields[gather_field_two.get().lower()] = {'gather_pattern': gather_pattern_two.get(),
                                              'gather_size': gather_size_two.get(),
                                              'gather_width': gather_width_two.get(),
                                              'gather_time': timetextbox_two.get(1.0,"end").replace("\n",""),
                                              'pack': packtextbox_two.get(1.0,"end").replace("\n",""),
                                              'before_gather_turn': before_gather_turn_two.get(),
                                              'turn_times': turn_times_two.get(),
                                              'return_to_hive': return_to_hive_two.get(),
                                              'whirligig_slot': whirligig_slot_two.get(),
                                              'start_location': start_location_two.get(),
                                              'distance_from_center': distance_from_center_two.get(),
                                              'field_drift_compensation': field_drift_compensation_two.get(),
                                              'shift_lock': shift_lock_two.get()

                                                      }

        if gather_field_three.get().lower() != "none":
            print('saved field 3')
            fields[gather_field_two.get().lower()] = {'gather_pattern': gather_pattern_three.get(),
                                              'gather_size': gather_size_three.get(),
                                              'gather_width': gather_width_three.get(),
                                              'gather_time': timetextbox_three.get(1.0,"end").replace("\n",""),
                                              'pack': packtextbox_three.get(1.0,"end").replace("\n",""),
                                              'before_gather_turn': before_gather_turn_three.get(),
                                              'turn_times': turn_times_three.get(),
                                              'return_to_hive': return_to_hive_three.get(),
                                              'whirligig_slot': whirligig_slot_three.get(),
                                              'start_location': start_location_three.get(),
                                              'distance_from_center': distance_from_center_three.get(),
                                              'field_drift_compensation': field_drift_compensation_three.get(),
                                              'shift_lock': shift_lock_three.get()


                                                      }
        with open(f"./profiles/{current_profile.get()}/fieldsettings.txt","w") as f:
            f.write(str(fields))
        f.close()
        
    def loadProfile(e):
        print(e)
        try:
            updateProfile(e)
            loadSettings(e)
            loadVariables()
            loadTextBoxes()
            fieldOne(gather_field_one.get())
            fieldTwo(gather_field_two.get())
            fieldThree(gather_field_three.get())
            loadsettings.save("current_profile",e)
        except FileNotFoundError:
            print("Profile not found")
            reloadProfileList()

    def importProfile():
        path = tk.filedialog.askdirectory(initialdir = "~/Downloads")
        files = os.listdir(path)
        nameOri = path.split("/")[-1]
        validFiles = ["fieldsettings.txt","settings.txt","plantersettings.txt"]
        print(files)
        for i in validFiles:
            if i not in files:
                pag.alert("Not a valid profile folder")
                return
                path = f"./profiles/{name}"
        count = 0
        name = nameOri
        while True:
            try:
                shutil.copytree(path, f"./profiles/{name}")
                break
            except FileExistsError:
                if count: name = f"{nameOri} ({count})"
                count += 1
            
        current_profile.set(name)
        reloadProfileList()
        loadProfile(name)
        
        
    def deleteProfile():
        window = tk.Toplevel() #creates a window to confirm if the user wants to start deleting files
        #window.config(bg=wbgc)
        selectedProfile = tk.StringVar(window)
        selectedProfile.set(current_profile.get())
        label = tk.Label(window, text = "Profile name:")
        dropField = ttk.OptionMenu(window, selectedProfile, current_profile.get(), *profiles)
        button_yes = ttk.Button(window, text="Delete",command=lambda: [removeProfile(selectedProfile.get()), window.destroy()], style = "small.TButton")
        button_no = ttk.Button(window, text="Cancel", command=window.destroy, style = "small.TButton")

        label.grid(row = 0, column = 0, sticky = tk.W, pady = 2)
        dropField.grid(row = 0, column = 1, pady = 2)
        button_yes.grid(row=1, column=0)
        button_no.grid(row=1, column=1)
        
    def removeProfile(profile):
        if len(profiles) <= 1: return
        shutil.rmtree(f"./profiles/{profile}")
        reloadProfileList()
        name = profiles[0]
        current_profile.set(name)
        loadProfile(name)
        
    def newProfile():
        window = tk.Toplevel() #creates a window to confirm if the user wants to start deleting files
        #window.config(bg=wbgc)
        label = tk.Label(window, text = "Profile name:")
        nameentry = tkinter.Entry(window, bg= wbgc)
        nameentry.bind('<Return>', lambda e: "break")
        button_yes = ttk.Button(window, text="Create",command=lambda: [createProfile(nameentry.get()), window.destroy()], style = "small.TButton")
        button_no = ttk.Button(window, text="Cancel", command=window.destroy, style = "small.TButton")

        label.grid(row = 0, column = 0, sticky = tk.W, pady = 2)
        nameentry.grid(row = 0, column = 1, pady = 2)
        button_yes.grid(row=1, column=0)
        button_no.grid(row=1, column=1)

    def createProfile(name):
        path = f"./profiles/{name}"
        os.mkdir(path)
        files = ["fieldsettings.txt", "plantersettings.txt",  "settings.txt"]
        for i in files:
            shutil.copyfile(f"./src/default settings/{i}", f"{path}/{i}")
        current_profile.set(name)
        reloadProfileList()
        loadProfile(name)
        
    def startGo():
        global setdat, stop, planterTypes_prev, planterFields_prev, quest_kill, quest_gathers
        quest_kill = {}
        quest_gathers = {}
        setdat = loadsettings.load()
        planterFields_set = []
        for i in listbox.curselection():
            planterFields_set.append(listbox.get(i).lower())
        saveFields()
        slot_enable_list = []
        slot_use_list = []
        slot_freq_list = []
        slot_time_list = []
        nums = ['one','two','three','four','five','six','seven']
        for i in range(1,8):
            slot_enable_list.append(globals()[f'slot_enable_{i}'].get())
            slot_freq_list.append(globals()[f'slot_freq_{i}'].get())
            slot_use_list.append(globals()[f'slot_use_{i}'].get())
            slot_time_list.append(globals()[f'slottextbox_{nums[i-1]}'].get(1.0,"end").replace("\n",""))

        generalDict = {
            "hive_number": hive_number.get(),
            "walkspeed": speedtextbox.get(1.0,"end").replace("\n",""),
            "gifted_vicious_bee": gifted_vicious_bee.get(),
            "enable_discord_webhook": enable_discord_webhook.get(),
            "discord_webhook_url": urltextbox.get(1.0,"end").replace("\n",""),
            "send_screenshot": send_screenshot.get(),
            "sprinkler_slot": sprinkler_slot.get(),
            "sprinkler_type": sprinkler_type.get(),
            "display_type": display_type.get().lower(),
            "new_ui": new_ui.get(),
            "private_server_link":linktextbox.get(1.0,"end").replace("\n",""),
            "enable_discord_bot":enable_discord_bot.get(),
            "discord_bot_token":tokentextbox.get(1.0,"end").replace("\n",""),
            "show_haste_warn": show_haste_warn,
            "current_profile": current_profile.get(),
            "start_honey":0,
            "prev_honey":0,
            "start_time":time.time(),
            "canon_time":1.0,#cttextbox.get(1.0,"end").replace("\n",""),
            "reverse_hive_direction": reverse_hive_direction.get(),
            "rejoin_delay": rejoindelaytextbox.get(1.0,"end").replace("\n",""),
            "rejoin_method": rejoin_method.get(),
            "so_broke": so_broke.get()
        } 
        setDict = {
            "haste_compensation": haste_compensation.get(),
            "rejoin_every_enabled": rejoin_every_enabled.get(),
            "rejoin_every": rejoinetextbox.get(1.0,"end").replace("\n",""),
            "manual_fullscreen": manual_fullscreen.get(),
            "convert_wait": convertwaittextbox.get(1.0,"end").replace("\n",""),
            #"convert_every_enabled": convert_every_enabled.get(),
            #"convert_every": converttextbox.get(1.0,"end").replace("\n",""),
            
            "gather_enable": gather_enable.get(),
            "gather_field": [gather_field_one.get(),gather_field_two.get(),gather_field_three.get()],
            
            "stump_snail": stump_snail.get(),
            "continue_after_stump_snail": continue_after_stump_snail.get(),
            "ladybug": ladybug.get(),
            "rhinobeetle": rhinobeetle.get(),
            "spider": spider.get(),
            "scorpion": scorpion.get(),
            "werewolf": werewolf.get(),
            "mantis": mantis.get(),
            "stinger": stinger.get(),
            "ant_challenge": antchallenge.get(),

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
            "antpass": antpass.get(),

            "blue_booster": blue_booster.get(),
            "red_booster": red_booster.get(),
            "mountain_booster": mountain_booster.get(),
            "gather_in_boosted": gather_in_boosted.get(),

            "slot_enable": slot_enable_list,
            "slot_time": slot_time_list,
            "slot_freq": slot_freq_list,
            "slot_use": slot_use_list,
            "polar_quest": polar_quest.get(),
            "backpack_freeze": backpack_freeze.get()

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
            a = float(generalDict["walkspeed"])
        except:
            pag.alert(text="The walkspeed of {} is not a valid number/decimal".format(generalDict['walkspeed']),title="Invalid setting",button="OK")
            return
        if float(generalDict["walkspeed"]) > 40:
            pag.alert(text="The walkspeed of {} is unusually high. Make sure that the value is entered correctly and there are no haste stacks")
        
        savesettings(generalDict,"generalsettings.txt")
        savesettings(planterdict,f"./profiles/{current_profile.get()}/plantersettings.txt")
        savesettings(setDict,f"./profiles/{current_profile.get()}/settings.txt")
        with open("haste.txt","w") as a:
            a.write(generalDict["walkspeed"])
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
                
                            
        macro()
    def macro():
        global  prevHour, prevMin, honeyHist, warnings
        savedat = loadRes()
        planterset = loadsettings.planterLoad()
        with open("planterdata.txt","r") as f:
            lines = f.read().split("\n")
        f.close()
        planterFields = ast.literal_eval(lines[2])
        if planterset['enable_planters'] and not planterFields:
            pag.alert(text='Planters enabled but no fields are selected', title='Warning', button='OK')
            return
        
        ww = savedat['ww']
        wh = savedat['wh']
        webhook("Macro started - Report","exih_macro\nVersion {}\nScreen Coordinates: {}x{}\nPython {}\n{}".format(macrov,ww,wh,python_ver,warnings),"dark brown")
        setdat = loadsettings.load()
        if not is_running("roblox"):
            rejoin()
        cmd = """
            osascript -e 'activate application "Roblox"' 
        """
        os.system(cmd)
        time.sleep(0.5)
        #fullscreen()
        im = pag.screenshot()
        im.save("roblox.png")
        
        if getTop(0):
            newUI = 0
            webhook("","Detected: Old UI","light blue")
        elif getTop(30):
            newUI = 1
            webhook("","Detected: New UI","light blue")
            log("applying new UI fix")
        else:
            webhook("","Unable to detect UI","red")
            newUI = 0    
        loadsettings.save("new_ui",newUI)
        
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
        
        vic_proc.start()
        try:
            #listener = pynput.keyboard.Listener(on_press=on_press)
            #listener.start()
            ses_start = 1
            
            while True:
                #if keyboard.is_pressed('q'):
                    #raise KeyboardInterrupt
               startLoop(planterTypes_prev, planterFields_prev,ses_start) 
               rejoin()
               ses_start = 0
                

                    
        except KeyboardInterrupt:
            setStatus()
            hastecompbg_proc.terminate()
            discord_bot_proc.terminate()
            vic_proc.terminate()
            webhook("Macro Stopped","","dark brown")
    
    def savedisplaytype(event):
        loadsettings.save("display_type",display_type.get().lower())
        setResolution()
        
    def disablews_one(event=""):
        if return_to_hive_one.get().lower() == "whirligig":
            wslotmenu_one.configure(state="normal")
        else:
            wslotmenu_one.configure(state="disable")
        if event: saveFields()
            
    def disablews_two(event=""):
        if return_to_hive_two.get().lower() == "whirligig":
            wslotmenu_two.configure(state="normal")
        else:
            wslotmenu_two.configure(state="disable")
        if event: saveFields()
            
    def disablews_three(event=""):
        if return_to_hive_three.get().lower() == "whirligig":
            wslotmenu_three.configure(state="normal")
        else:
            wslotmenu_three.configure(state="disable")
        if event: saveFields()

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
    def warnHasteComp():
        global show_haste_warn
        if not show_haste_warn and str(haste_compensation.get()) == "1":
            pag.alert("Note: Enabling haste compensation will cause the macro to use the roblox UI navigation. This is normal behavior.")
            show_haste_warn = 1
            
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

    class Tooltip:
        def __init__(self, widget,
                     *,
                     bg='#FFFFEA',
                     pad=(5, 3, 5, 3),
                     text='widget info',
                     waittime=400,
                     wraplength=250):

            self.waittime = waittime  # in miliseconds, originally 500
            self.wraplength = wraplength  # in pixels, originally 180
            self.widget = widget
            self.text = text
            self.widget.bind("<Enter>", self.onEnter)
            self.widget.bind("<Leave>", self.onLeave)
            self.widget.bind("<ButtonPress>", self.onLeave)
            self.bg = bg
            self.pad = pad
            self.id = None
            self.tw = None

        def onEnter(self, event=None):
            self.schedule()

        def onLeave(self, event=None):
            self.unschedule()
            self.hide()

        def schedule(self):
            self.unschedule()
            self.id = self.widget.after(self.waittime, self.show)

        def unschedule(self):
            id_ = self.id
            self.id = None
            if id_:
                self.widget.after_cancel(id_)

        def show(self):
            def tip_pos_calculator(widget, label,
                                   *,
                                   tip_delta=(10, 5), pad=(5, 3, 5, 3)):

                w = widget

                s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

                width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                                 pad[1] + label.winfo_reqheight() + pad[3])

                mouse_x, mouse_y = w.winfo_pointerxy()

                x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
                x2, y2 = x1 + width, y1 + height

                x_delta = x2 - s_width
                if x_delta < 0:
                    x_delta = 0
                y_delta = y2 - s_height
                if y_delta < 0:
                    y_delta = 0

                offscreen = (x_delta, y_delta) != (0, 0)

                if offscreen:

                    if x_delta:
                        x1 = mouse_x - tip_delta[0] - width

                    if y_delta:
                        y1 = mouse_y - tip_delta[1] - height

                offscreen_again = y1 < 0  # out on the top

                if offscreen_again:
                    # No further checks will be done.

                    # TIP:
                    # A further mod might automagically augment the
                    # wraplength when the tooltip is too high to be
                    # kept inside the screen.
                    y1 = 0

                return x1, y1

            bg = self.bg
            pad = self.pad
            widget = self.widget

            # creates a toplevel window
            self.tw = tk.Toplevel(widget)

            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)

            win = ttk.Frame(self.tw)
            label = tkinter.Label(win, text=self.text, wraplength = 250, justify=tk.LEFT)

            label.grid(padx=(pad[0], pad[2]),
                       pady=(pad[1], pad[3]),
                       sticky=tk.NSEW)
            win.grid()

            x, y = tip_pos_calculator(widget, label)

            self.tw.wm_geometry("+%d+%d" % (x, y))

        def hide(self):
            tw = self.tw
            if tw:
                tw.destroy()
            self.tw = None

     
    #Tab 1
            
    checkbox = tkinter.Checkbutton(frame1, text="Enable Gathering", variable=gather_enable)
    checkbox.place(x=0, y = 15)
    Tooltip(checkbox, text = "The macro will rotate and gather between the assigned fields")
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
    dropField = ttk.OptionMenu(frame1, gather_field_one,setdat['gather_field'][0].title(), *gather_fields[1:],style='smaller.TMenubutton', command = fieldOne )
    dropField.place(x = 10, y = ylevel+35,height=22,width=100)
    Tooltip(dropField,text = "First field to gather")
    checkbox = tkinter.Checkbutton(frame1, text="Saturator\nAlign", variable=field_drift_compensation_one, command = saveFields)
    checkbox.place(x=10, y = ylevel+65)
    Tooltip(checkbox, text = "Moves the player to the supreme saturator")
    checkbox = tkinter.Checkbutton(frame1, text="Gather w/ Shift Lock", variable=shift_lock_one, command = saveFields)
    checkbox.place(x=140, y = ylevel+85)
    Tooltip(checkbox, text = "Activate shift lock when gathering")
    
    dropField = ttk.OptionMenu(frame1, gather_pattern_one,gather_pattern_one.get(), *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")],style='smaller.TMenubutton', command = saveFields)
    dropField.place(width=90,x = 145, y = ylevel+35,height=22)
    Tooltip(dropField, text = "The pattern/shape that the player walks when gathering")
    dropField = ttk.OptionMenu(frame1, gather_size_one,gather_size_one.get(), *["S","M","L"],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 255, y = ylevel+35,height = 22)
    Tooltip(dropField, text = "The size of the shape. Generally affects the area covered")
    dropField = ttk.OptionMenu(frame1, gather_width_one,gather_width_one.get(), *[(x+1) for x in range(10)],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 320, y = ylevel+35,height=22)
    Tooltip(dropField, text = "Affects each shape differently")

    tkinter.Label(frame1, text = "Rotate Camera").place(x = 140, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, before_gather_turn_one,before_gather_turn_one.get(), *["None","Left","Right"],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=60,x = 255, y = ylevel+67,height=22)
    Tooltip(dropField, text = "The direction to turn after landing on the field. Direction is relative to the hives (faces the hives by default)")
    dropField = ttk.OptionMenu(frame1, turn_times_one,turn_times_one.get(), *[(x+1) for x in range(4)],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 325, y = ylevel+67,height=22)
    Tooltip(dropField, text = "The number of turns")

    timetextbox_one = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    timetextbox_one.place(x = 400, y=ylevel+35)
    timetextbox_one.bind('<KeyRelease>', saveFields)
    timetextbox_one.bind('<Return>', lambda e: "break")
    Tooltip(timetextbox_one, text = "Maximum time to gather for")
    packtextbox_one = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    packtextbox_one.place(x = 460, y=ylevel+35)
    packtextbox_one.bind('<KeyRelease>', saveFields)
    packtextbox_one.bind('<Return>', lambda e: "break")
    Tooltip(packtextbox_one, text = "Minimum backpack capacity to gather for.\nSet to 101 to disable")
    dropConvert = ttk.OptionMenu(frame1 , return_to_hive_one,return_to_hive_one.get().title(), command = disablews_one, *["Walk","Reset","Rejoin","Whirligig"],style='smaller.TMenubutton')
    dropConvert.place(width=75,x = 520, y = ylevel+35,height=22)
    Tooltip(dropConvert, text = "How the macro returns to hive after gathering")
    tkinter.Label(frame1, text = "Whirligig Slot").place(x = 452, y = ylevel+65)
    wslotmenu_one = ttk.OptionMenu(frame1 , whirligig_slot_one,whirligig_slot_one.get(), *[1,2,3,4,5,6,7,"none"],style='smaller.TMenubutton', command = saveFields)
    wslotmenu_one.place(width=50,x = 542, y = ylevel+65,height=22)
    Tooltip(wslotmenu_one, text = "The hotbar slot of the whirligig")


    dropField = ttk.OptionMenu(frame1, start_location_one,start_location_one.get().title(), *["Center","Upper Right","Right","Lower Right","Bottom","Lower Left","Left","Upper Left","Top"],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=100,x = 625, y = ylevel+35,height=22)
    Tooltip(dropField, text = "The area on the field that the macro will walk towards. Direction is relative to the hives")
    tkinter.Label(frame1, text = "Distance").place(x = 625, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, distance_from_center_one,distance_from_center_one.get(), *[(x+1) for x in range(10)],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 695, y = ylevel+65,height=22)
    Tooltip(dropField, text = "The distance that the player should walk to the start location")

    ylevel = 140
    dropField = ttk.OptionMenu(frame1, gather_field_two,setdat['gather_field'][1].title(), *gather_fields,style='smaller.TMenubutton', command = fieldTwo )
    dropField.place(x = 10, y = ylevel+35,height=22,width=100)
    Tooltip(dropField,text = "Second field to gather")
    checkbox = tkinter.Checkbutton(frame1, text="Saturator\nAlign", variable=field_drift_compensation_two, command = saveFields)
    checkbox.place(x=10, y = ylevel+65)
    Tooltip(checkbox, text = "Moves the player to the supreme saturator")
    checkbox = tkinter.Checkbutton(frame1, text="Gather w/ Shift Lock", variable=shift_lock_two, command = saveFields)
    checkbox.place(x=140, y = ylevel+85)
    Tooltip(checkbox, text = "Activate shift lock when gathering")
    
    dropField = ttk.OptionMenu(frame1, gather_pattern_two,gather_pattern_two.get(), *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")],style='smaller.TMenubutton', command = saveFields)
    dropField.place(width=90,x = 145, y = ylevel+35,height=22)
    Tooltip(dropField, text = "The pattern/shape that the player walks when gathering")
    dropField = ttk.OptionMenu(frame1, gather_size_two,gather_size_two.get().title(), *["S","M","L"],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 255, y = ylevel+35,height = 22)
    Tooltip(dropField, text = "The size of the shape. Generally affects the area covered")
    dropField = ttk.OptionMenu(frame1, gather_width_two,gather_width_two.get(), *[(x+1) for x in range(10)],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 320, y = ylevel+35,height=22)
    Tooltip(dropField, text = "Affects each shape differently")

    tkinter.Label(frame1, text = "Rotate Camera").place(x = 140, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, before_gather_turn_two,before_gather_turn_two.get().title(), *["None","Left","Right"],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=60,x = 255, y = ylevel+67,height=22)
    Tooltip(dropField, text = "The direction to turn after landing on the field. Direction is relative to the hives (faces the hives by default)")
    dropField = ttk.OptionMenu(frame1, turn_times_two,turn_times_two.get(), *[(x+1) for x in range(4)],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 325, y = ylevel+67,height=22)
    Tooltip(dropField, text = "The number of turns")

    timetextbox_two = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    timetextbox_two.place(x = 400, y=ylevel+35)
    timetextbox_two.bind('<KeyRelease>', saveFields)
    timetextbox_two.bind('<Return>', lambda e: "break")
    Tooltip(timetextbox_two, text = "Maximum time to gather for")
    packtextbox_two = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    packtextbox_two.place(x = 460, y=ylevel+35)
    packtextbox_two.bind('<KeyRelease>', saveFields)
    packtextbox_two.bind('<Return>', lambda e: "break")
    Tooltip(packtextbox_two, text = "Minimum backpack capacity to gather for.\nSet to 101 to disable")
    dropConvert = ttk.OptionMenu(frame1 , return_to_hive_two,return_to_hive_two.get().title(), command = disablews_two, *["Walk","Reset","Rejoin","Whirligig"],style='smaller.TMenubutton')
    dropConvert.place(width=75,x = 520, y = ylevel+35,height=22)
    Tooltip(dropConvert, text = "How the macro returns to hive after gathering")
    tkinter.Label(frame1, text = "Whirligig Slot").place(x = 452, y = ylevel+65)
    wslotmenu_two = ttk.OptionMenu(frame1 , whirligig_slot_two,whirligig_slot_two.get(), *[1,2,3,4,5,6,7,"none"],style='smaller.TMenubutton', command = saveFields)
    wslotmenu_two.place(width=50,x = 542, y = ylevel+65,height=22)
    Tooltip(wslotmenu_two, text = "The hotbar slot of the whirligig")


    dropField = ttk.OptionMenu(frame1, start_location_two,start_location_two.get().title(), *["Center","Upper Right","Right","Lower Right","Bottom","Lower Left","Left","Upper Left","Top"],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=100,x = 625, y = ylevel+35,height=22)
    Tooltip(dropField, text = "The area on the field that the macro will walk towards. Direction is relative to the hives")
    tkinter.Label(frame1, text = "Distance").place(x = 625, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, distance_from_center_two,distance_from_center_two.get(), *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 695, y = ylevel+65,height=22)
    Tooltip(dropField, text = "The distance that the player should walk to the start location")

    ylevel = 230
    dropField = ttk.OptionMenu(frame1, gather_field_three,setdat['gather_field'][2].title(), *gather_fields,style='smaller.TMenubutton', command = fieldThree )
    dropField.place(x = 10, y = ylevel+35,height=22,width=100)
    Tooltip(dropField,text = "Third field to gather")
    checkbox = tkinter.Checkbutton(frame1, text="Saturator\nAlign", variable=field_drift_compensation_three, command = saveFields)
    checkbox.place(x=10, y = ylevel+65)
    Tooltip(checkbox, text = "Moves the player to the supreme saturator")
    checkbox = tkinter.Checkbutton(frame1, text="Gather w/ Shift Lock", variable=shift_lock_three, command = saveFields)
    checkbox.place(x=140, y = ylevel+85)
    Tooltip(checkbox, text = "Activate shift lock when gathering")
    
    dropField = ttk.OptionMenu(frame1, gather_pattern_three,gather_pattern_three.get(), *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")],style='smaller.TMenubutton', command = saveFields)
    dropField.place(width=90,x = 145, y = ylevel+35,height=22)
    Tooltip(dropField, text = "The pattern/shape that the player walks when gathering")
    dropField = ttk.OptionMenu(frame1, gather_size_three,gather_size_three.get().title(), *["S","M","L"],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 255, y = ylevel+35,height = 22)
    Tooltip(dropField, text = "The size of the shape. Generally affects the area covered")
    dropField = ttk.OptionMenu(frame1, gather_width_three,gather_width_three.get(), *[(x+1) for x in range(10)],style='smaller.TMenubutton' )
    dropField.place(width=50,x = 320, y = ylevel+35,height=22)
    Tooltip(dropField, text = "Affects each shape differently")

    tkinter.Label(frame1, text = "Rotate Camera").place(x = 140, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, before_gather_turn_three,before_gather_turn_three.get().title(), *["None","Left","Right"],style='smaller.TMenubutton', command = saveFields)
    dropField.place(width=60,x = 255, y = ylevel+67,height=22)
    Tooltip(dropField, text = "The direction to turn after landing on the field. Direction is relative to the hives (faces the hives by default)")
    dropField = ttk.OptionMenu(frame1, turn_times_three,turn_times_three.get(), *[(x+1) for x in range(4)],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 325, y = ylevel+67,height=22)
    Tooltip(dropField, text = "The number of turns")

    timetextbox_three = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    timetextbox_three.place(x = 400, y=ylevel+35)
    timetextbox_three.bind('<KeyRelease>', saveFields)
    timetextbox_three.bind('<Return>', lambda e: "break")
    Tooltip(timetextbox_three, text = "Maximum time to gather for")
    packtextbox_three = tkinter.Text(frame1, width = 4, height = 1, bg= wbgc)
    packtextbox_three.place(x = 460, y=ylevel+35)
    packtextbox_three.bind('<KeyRelease>', saveFields)
    packtextbox_three.bind('<Return>', lambda e: "break")
    Tooltip(packtextbox_three, text = "Minimum backpack capacity to gather for.\nSet to 101 to disable")
    dropConvert = ttk.OptionMenu(frame1 , return_to_hive_three,return_to_hive_three.get().title(), command = disablews_three, *["Walk","Reset","Rejoin","Whirligig"],style='smaller.TMenubutton')
    dropConvert.place(width=75,x = 520, y = ylevel+35,height=22)
    Tooltip(dropConvert, text = "How the macro returns to hive after gathering")
    tkinter.Label(frame1, text = "Whirligig Slot").place(x = 452, y = ylevel+65)
    wslotmenu_three = ttk.OptionMenu(frame1 , whirligig_slot_three,whirligig_slot_three.get(), *[1,2,3,4,5,6,7,"none"],style='smaller.TMenubutton', command = saveFields)
    wslotmenu_three.place(width=50,x = 542, y = ylevel+65,height=22)
    Tooltip(wslotmenu_three, text = "The hotbar slot of the whirligig")


    dropField = ttk.OptionMenu(frame1, start_location_three,start_location_three.get().title(), *["Center","Upper Right","Right","Lower Right","Bottom","Lower Left","Left","Upper Left","Top"],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=100,x = 625, y = ylevel+35,height=22)
    Tooltip(dropField, text = "The area on the field that the macro will walk towards. Direction is relative to the hives")
    tkinter.Label(frame1, text = "Distance").place(x = 625, y = ylevel+65)
    dropField = ttk.OptionMenu(frame1, distance_from_center_three,distance_from_center_three.get(), *[(x+1) for x in range(10)],style='smaller.TMenubutton', command = saveFields )
    dropField.place(width=50,x = 695, y = ylevel+65,height=22)
    Tooltip(dropField, text = "The distance that the player should walk to the start location")

    #Tab 2 
    checkbox = tkinter.Checkbutton(frame2, text="Apply gifted vicious bee hive bonus", variable=gifted_vicious_bee)
    checkbox.place(x=0, y = 15)
    Tooltip(checkbox, text = "Accounts for gifted vicious' hive bonus in the calculation of mob respawn times")
    checkbox = tkinter.Checkbutton(frame2, text="Stump Snail", variable=stump_snail)
    checkbox.place(x=0, y = 50)
    Tooltip(checkbox, text = "Afks at stump snail indefinitely (unless 'continue macro after stump snail' is enabled)")
    checkbox = tkinter.Checkbutton(frame2, text="Continue macro after stump snail is killed", variable=continue_after_stump_snail)
    checkbox.place(x=120, y = 50)
    Tooltip(checkbox, text = "Detects when stump snail is killed and continues macroing. Does not replace amulet")
    tkinter.Checkbutton(frame2, text="Ladybug", variable=ladybug).place(x=0, y = 85)
    tkinter.Checkbutton(frame2, text="Rhino Beetle", variable=rhinobeetle).place(x=80, y = 85)
    tkinter.Checkbutton(frame2, text="Scorpion", variable=scorpion).place(x=190, y = 85)
    tkinter.Checkbutton(frame2, text="Mantis", variable=mantis).place(x=275, y = 85)
    tkinter.Checkbutton(frame2, text="Spider", variable=spider).place(x=345, y = 85)
    tkinter.Checkbutton(frame2, text="Werewolf", variable=werewolf).place(x=415, y = 85)

    #Tab 3
    tkinter.Checkbutton(frame4, text="Wealth Clock", variable=wealthclock).place(x=0, y = 15)
    checkbox = tkinter.Checkbutton(frame4, text="Mondo Buff", variable=mondo_buff)
    checkbox.place(x=120, y = 15)
    Tooltip(checkbox, text = "Goes to the mondo chick within the first 20mins of the hour.\n Stays for 2mins")
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
    Tooltip(dropField, text = "hotbar slot of the gumdrop")
    checkbox = tkinter.Checkbutton(frame4, text="Stinger Hunt", variable=stinger)
    checkbox.place(x=0, y = 155)
    Tooltip(checkbox, text = "Detects night, finds vicious bee and fights it.\n\nNote that night detection requires the sky/wall to be visible in the upper left corner of the screen")
    tkinter.Checkbutton(frame4, text="(Free) Ant Pass Dispenser", variable=antpass).place(x=0, y = 190)
    tkinter.Checkbutton(frame4, text="Ant Challenge", variable=antchallenge).place(x=200, y = 190)
    
    #Tab 4

    tkinter.Checkbutton(frame5, text="Blue Booster", variable=blue_booster).place(x=10, y = 15)
    tkinter.Checkbutton(frame5, text="Red Booster", variable=red_booster).place(x=10, y = 50)
    tkinter.Checkbutton(frame5, text="Mountain Booster", variable=mountain_booster).place(x=10, y = 85)
    checkbox = tkinter.Checkbutton(frame5, text="Gather in\nBoosted Field", variable=gather_in_boosted)
    checkbox.place(x=15, y = 130)
    Tooltip(checkbox, text = "Gather in the field with the field boost for 15mins")
    ttk.Separator(frame5,orient="vertical").place(x=190, y=15, width=2, height=310)
    label = tkinter.Label(frame5, text = "Slot")
    label.place(x = 300, y = 15)
    Tooltip(label, text = "Use the item in the associated hotbar slot")
    tkinter.Checkbutton(frame5, text="Slot 1", variable=slot_enable_1).place(x=210, y = 60)
    tkinter.Checkbutton(frame5, text="Slot 2", variable=slot_enable_2).place(x=210, y = 95)
    tkinter.Checkbutton(frame5, text="Slot 3", variable=slot_enable_3).place(x=210, y = 130)
    tkinter.Checkbutton(frame5, text="Slot 4", variable=slot_enable_4).place(x=210, y = 165)
    tkinter.Checkbutton(frame5, text="Slot 5", variable=slot_enable_5).place(x=210, y = 200)
    tkinter.Checkbutton(frame5, text="Slot 6", variable=slot_enable_6).place(x=210, y = 235)
    tkinter.Checkbutton(frame5, text="Slot 7", variable=slot_enable_7).place(x=210, y = 270)
    useOptions = ["Always", "Hive", "Gathering"]
    timeOptions = ["secs", "mins"]
    dropField = ttk.OptionMenu(frame5, slot_use_1, slot_use_1.get().title(), *useOptions,style='smaller.TMenubutton')
    dropField.place(width=85,x = 290, y = 60,height=20)
    dropField = ttk.OptionMenu(frame5, slot_use_2, slot_use_2.get().title(), *useOptions,style='smaller.TMenubutton')
    dropField.place(width=85,x = 290, y = 95,height=20)
    dropField = ttk.OptionMenu(frame5, slot_use_3, slot_use_3.get().title(), *useOptions,style='smaller.TMenubutton')
    dropField.place(width=85,x = 290, y = 130,height=20)
    dropField = ttk.OptionMenu(frame5, slot_use_4, slot_use_4.get().title(), *useOptions,style='smaller.TMenubutton')
    dropField.place(width=85,x = 290, y = 165,height=20)
    dropField = ttk.OptionMenu(frame5, slot_use_5, slot_use_5.get().title(), *useOptions,style='smaller.TMenubutton')
    dropField.place(width=85,x = 290, y = 200,height=20)
    dropField = ttk.OptionMenu(frame5, slot_use_6, slot_use_6.get().title(), *useOptions,style='smaller.TMenubutton')
    dropField.place(width=85,x = 290, y = 235,height=20)
    dropField = ttk.OptionMenu(frame5, slot_use_7, slot_use_7.get().title(), *useOptions,style='smaller.TMenubutton')
    dropField.place(width=85,x = 290, y = 270,height=20)
    slottextbox_one = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    slottextbox_one.place(x = 390, y=60)
    slottextbox_two = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    slottextbox_two.place(x = 390, y=95)
    slottextbox_three = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    slottextbox_three.place(x = 390, y=130)
    slottextbox_four = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    slottextbox_four.place(x = 390, y=165)
    slottextbox_five = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    slottextbox_five.place(x = 390, y=200)
    slottextbox_six = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    slottextbox_six.place(x = 390, y=235)
    slottextbox_seven = tkinter.Text(frame5, width = 4, height = 1, bg= wbgc)
    slottextbox_seven.place(x = 390, y=270)
    dropField = ttk.OptionMenu(frame5, slot_freq_1, slot_freq_1.get().title(), *timeOptions,style='smaller.TMenubutton')
    dropField.place(width=65,x = 430, y = 60,height=20)
    dropField = ttk.OptionMenu(frame5, slot_freq_2, slot_freq_2.get().title(), *timeOptions,style='smaller.TMenubutton')
    dropField.place(width=65,x = 430, y = 95,height=20)
    dropField = ttk.OptionMenu(frame5, slot_freq_3, slot_freq_3.get().title(), *timeOptions,style='smaller.TMenubutton')
    dropField.place(width=65,x = 430, y = 130,height=20)
    dropField = ttk.OptionMenu(frame5, slot_freq_4, slot_freq_4.get().title(), *timeOptions,style='smaller.TMenubutton')
    dropField.place(width=65,x = 430, y = 165,height=20)
    dropField = ttk.OptionMenu(frame5, slot_freq_5, slot_freq_5.get().title(), *timeOptions,style='smaller.TMenubutton')
    dropField.place(width=65,x = 430, y = 200,height=20)
    dropField = ttk.OptionMenu(frame5, slot_freq_6, slot_freq_6.get().title(), *timeOptions,style='smaller.TMenubutton')
    dropField.place(width=65,x = 430, y = 235,height=20)
    dropField = ttk.OptionMenu(frame5, slot_freq_7, slot_freq_7.get().title(), *timeOptions,style='smaller.TMenubutton')
    dropField.place(width=65,x = 430, y = 270,height=20)
    
    #Tab 5
    checkbox = tkinter.Checkbutton(frame6, text="Enable Planters", variable=enable_planters)
    checkbox.place(x=545, y = 20)
    Tooltip(checkbox, text = "Automatically places and collects planters.\nAutomatically decides on which planter to place per field\nRotates between fields  and planters to avoid degration.")
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
    Tooltip(listbox, text = "Which fields the macro can place planters in")
    scrollbar.place(x=513,y=75,height=110)
    for i in planter_fields:
        listbox.select_set(field_options.get().index(i.title()))

    
    dropField = ttk.OptionMenu(frame6, planter_count,plantdat['planter_count'], *[1,2,3],style='my.TMenubutton' )
    dropField.place(x = 630, y = 70,height=24,width=60)
    tkinter.Label(frame6, text = "Max planters").place(x=545,y=70)
    tkinter.Label(frame6, text = "Harvest Every").place(x=545,y=105)
    harvesttextbox = tkinter.Text(frame6, width = 4, height = 1, bg= wbgc)
    harvesttextbox.place(x = 637, y=107)
    harvesttextbox.bind('<Return>', lambda e: "break")
    Tooltip(harvesttextbox, text = "How often the macro will collect the planters")
    tkinter.Label(frame6, text = "Hours").place(x=674,y=105)
    checkbox = tkinter.Checkbutton(frame6, text="Full Grown", variable=harvest_full,command=lambda: changeHarvest("full"))
    checkbox.place(x=545, y = 140)
    Tooltip(checkbox, text = "Override the harvest setting to collect the planters when full")
   #tkinter.Checkbutton(frame6, text="Auto", variable=harvest_auto,command=lambda: changeHarvest("auto")).place(x=640, y = 140)

    
    #Tab 6

    #tkinter.Checkbutton(frame8, text="Polar Bear quest", variable=polar_quest).place(x=0, y = 30)

    #Tab 7
    tkinter.Label(frame3, text = "Hive Slot (6-5-4-3-2-1)").place(x = 0, y = 15)
    dropField = ttk.OptionMenu(frame3, hive_number, setdat['hive_number'], *[x+1 for x in range(6)],style='my.TMenubutton' )
    dropField.place(width=60,x = 160, y = 15,height=24)
    Tooltip(dropField, text = "what hive is currently claimed.\n1 is the closest to red cannon, 6 is closest to the noob shop")
    tkinter.Label(frame3, text = "Move Speed (without haste)").place(x = 0, y = 50)
    speedtextbox = tkinter.Text(frame3, width = 4, height = 1, bg= wbgc)
    speedtextbox.insert("end",walkspeed)
    speedtextbox.place(x = 185, y=52)
    speedtextbox.bind('<Return>', lambda e: "break")
    Tooltip(speedtextbox, text = "The movespeed of the player without any additional haste.\nThe movespeed can be found in the bee swarm settings")

    tkinter.Label(frame3, text = "Sprinkler Type").place(x = 0, y = 85)
    dropField = ttk.OptionMenu(frame3, sprinkler_type, setdat['sprinkler_type'], *["Basic","Silver","Golden","Diamond","Saturator"],style='my.TMenubutton' )
    dropField.place(width=90,x = 100, y = 85,height=24)

    tkinter.Label(frame3, text = "Slot").place(x = 205, y = 85)
    dropField = ttk.OptionMenu(frame3, sprinkler_slot, setdat['sprinkler_slot'], *[x+1 for x in range(6)],style='my.TMenubutton' )
    dropField.place(width=60,x = 245, y = 85,height=24)
    Tooltip(dropField, text = "The hotbar slot of the sprinkler")

    checkbox = tkinter.Checkbutton(frame3, text="Enable Haste Compensation", variable=haste_compensation, command = warnHasteComp)
    checkbox.place(x=0, y = 120)
    Tooltip(checkbox, text = "Requires UI Navigagtion to be enabled.\n\nConstantly reads the movespeed stat from the in-game settings to compensate for any of its changes.\nCan be inconsistent as it takes 1-3 seconds to detect.")
    
    tkinter.Label(frame3, text = "Wait").place(x = 0, y = 155)
    convertwaittextbox = tkinter.Text(frame3, width = 4, height = 1, bg= wbgc)
    convertwaittextbox.place(x = 40, y=157)
    convertwaittextbox.bind('<Return>', lambda e: "break")
    Tooltip(convertwaittextbox, text = "Time to wait after the macro is done converting. This is useful for converting small amount of excess pollen/balloon")
    tkinter.Label(frame3, text = "secs after converting").place(x = 75, y = 155)
    
    #tkinter.Checkbutton(frame3, text="Convert every", variable=convert_every_enabled).place(x=0, y = 190)
    #converttextbox = tkinter.Text(frame3, width = 4, height = 1, bg= wbgc)
    #converttextbox.insert("end", convert_every)
    #converttextbox.place(x=120,y=193)
    #tkinter.Label(frame3, text = "mins").place(x = 160, y = 190)


    #Tab 8
    checkbox = tkinter.Checkbutton(frame7, text="Enable Discord Webhook", command = disabledw,variable=enable_discord_webhook)
    checkbox.place(x=0, y = 15)
    Tooltip(checkbox, text = "Uses a discord webhook to send status messages")
    tkinter.Label(frame7, text = "Discord Webhook Link").place(x = 350, y = 15)
    urltextbox = tkinter.Text(frame7, width = 24, height = 1, yscrollcommand = True, bg= wbgc)
    urltextbox.insert("end",discord_webhook_url)
    sendss = tkinter.Checkbutton(frame7, text="Send screenshots", variable=send_screenshot)
    sendss.place(x=200, y = 15)
    Tooltip(sendss, text = "Sends screenshots along with the status messages.\nAlso enables the hourly report, which is sent at the start of every hour")
    urltextbox.place(x = 500, y=17)
    
    tkinter.Label(frame7, text = "Private Server Link (optional)").place(x = 0, y = 85)
    linktextbox = tkinter.Text(frame7, width = 24, height = 1, bg= wbgc)
    linktextbox.insert("end",private_server_link)
    linktextbox.place(x=190,y=87)
    linktextbox.bind('<Return>', lambda e: "break")
    Tooltip(linktextbox, text = "The private server link the macro will use when rejoining. If no link is provided, the macro will join a public server instead")
    
    checkbox = tkinter.Checkbutton(frame7, text="Enable Discord Bot", variable=enable_discord_bot)
    checkbox.place(x=0, y = 50)
    Tooltip(checkbox, text = "A discord bot which allows you to send commands to the macro")
    tkinter.Label(frame7, text = "Discord Bot Token").place(x = 170, y = 50)
    tokentextbox = tkinter.Text(frame7, width = 24, height = 1, bg= wbgc)
    tokentextbox.insert("end",discord_bot_token)
    tokentextbox.place(x = 300, y=52)
    tokentextbox.bind('<Return>', lambda e: "break")

    tkinter.Checkbutton(frame7, text="Rejoin every", variable=rejoin_every_enabled).place(x=0, y = 120)
    rejoinetextbox = tkinter.Text(frame7, width = 4, height = 1, bg= wbgc)
    rejoinetextbox.place(x=104,y=123)
    rejoinetextbox.bind('<Return>', lambda e: "break")
    tkinter.Label(frame7, text = "hours").place(x = 140, y = 120)

    tkinter.Label(frame7, text = "Wait for").place(x = 0, y = 155)
    rejoindelaytextbox = tkinter.Text(frame7, width = 4, height = 1, bg= wbgc)
    rejoindelaytextbox.insert("end",rejoin_delay)
    rejoindelaytextbox.place(x=55,y=158)
    rejoindelaytextbox.bind('<Return>', lambda e: "break")
    Tooltip(rejoindelaytextbox, text = "The time to wait for bee swarm to load when rejoining")
    tkinter.Label(frame7, text = "secs when rejoining").place(x = 90, y = 155)
    checkbox = tkinter.Checkbutton(frame7, text="Manually fullscreen when rejoining (Enable when roblox doesnt launch in fullscreen)", variable=manual_fullscreen)
    checkbox.place(x=0, y = 190)
    Tooltip(checkbox, text = "Fullscreens roblox when rejoining.")
    tkinter.Label(frame7, text = "Rejoin method").place(x = 250, y = 155)
    dropField = ttk.OptionMenu(frame7, rejoin_method, setdat['rejoin_method'].title(), *["New Tab","Type In Link", "Copy Paste", "Reload", "Deeplink"],style='my.TMenubutton' )
    dropField.place(width=90,x = 360, y = 155,height=24)
    Tooltip(dropField, text = "How the macro interacts with the browser when rejoining. Different rejoin methods work for different users.\n\nIt is recommended to experiment to see which one works for you.")
    checkbox = tkinter.Checkbutton(frame7, text="Backpack freeze detection", variable=backpack_freeze)
    checkbox.place(x=0, y = 225)
    Tooltip(checkbox, text = "Detects roblox as frozen when the backpack has not changed for a while.\nThis detection only occurs when the macro is gathering")
    checkbox = tkinter.Checkbutton(frame7, text="Existance so broke", variable=so_broke)
    checkbox.place(x=0, y = 260)
    Tooltip(checkbox, text = "Sends 'Existance so broke' when rejoining. This is a reference to Natro's 'Natro so broke'")

    #Tab 9
    tkinter.Label(frame9, justify=tk.LEFT, text = "Profiles store settings individually to allow you to swap between them.\nThey do not store discord bot, discord webhook, rejoin method, rejoin wait,\nvicious bonus, hive number and walkspeed settings").place(x = 0, y = 10)
    tkinter.Label(frame9, text = "Current profile").place(x = 0, y = 105)
    profileField = ttk.OptionMenu(frame9, current_profile, setdat["current_profile"], *profiles,style='my.TMenubutton', command = loadProfile)
    profileField.place(x = 115, y = 105)
    ttk.Button(frame9, text = "New profile", command = newProfile, style='small.TButton').place(x=0,y=140)
    ttk.Button(frame9, text = "Delete profile", command = deleteProfile, style='small.TButton').place(x=130,y=140)
    ttk.Button(frame9, text = "Import profile", command = importProfile, style='small.TButton').place(x=255,y=140)
    
    #Root
    ttk.Button(root, text = "Start", command = startGo, width = 7 ).place(x=10,y=420)
    ttk.Button(root, text = "Update",command = updateFiles, width = 9,).place(x=150,y=420)
    ttk.Button(root, text = "Experimental update",command = expu, width = 16,).place(x=300,y=420)
    ttk.Label(root, text = "version {}".format(macrov)).place(x = 680, y = 440)

    disablews_one()
    disablews_two()
    disablews_three()
    disabledw()
    disableeb("1")
    fieldOne(gather_field_one.get())
    fieldTwo(gather_field_two.get())
    fieldThree(gather_field_three.get())
    loadTextBoxes()
    root.mainloop()

