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
try: import cv2
except: pass
savedata = {}
ww = ""
wh = ""
ms = pag.size()
mw = ms[0]
mh = ms[1]
stop = 1
setdat = loadsettings.load()
macrov = 1.24
if __name__ == '__main__':
    print("Your python version is {}".format(sys.version_info[0]))
    print("Your macro version is {}".format(macrov))
    manager = multiprocessing.Manager()
    currentfield = manager.Value(ctypes.c_wchar_p, "")
    bpc = multiprocessing.Value('i', 0)
    gather = multiprocessing.Value('i', 0)
    disconnected = multiprocessing.Value('i', 0)
    
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
    if not s['gather_field'] in validfield:
        msg += ("Invalid gather_field")
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
    
def ebutton():
    r =  []
    savedata = loadRes()
    c = loadsettings.load()['ebthreshold']
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
 
    if setdat['ebdetect'] == "pyautogui":
        r = pag.locateOnScreen("./images/retina/eb.png",region=(0,0,ww,wh//2))
    else:
        r = imagesearch.find("eb.png",c,0,0,ww,wh//2)
    if r:return r
    return
def canon():
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
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
        move.hold("d",0.15)
        r = ebutton()
        if r:
            webhook("","Canon found","dark brown")
            return
        if time.perf_counter()  - st > 10/28*setdat["walkspeed"]:
            webhook("","Cannon not found, resetting","dark brown",1)
            break
    pag.moveTo(724,674)
    for _ in range(20):
        pag.click()
        time.sleep(0.25)
    reset.reset()   
    canon()
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
def walk_to_hive():
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    webhook("","Going back to hive: {}".format(setdat['gather_field']),"dark brown")
    exec(open("walk_{}.py".format(setdat['gather_field'])).read())
    st = time.perf_counter()
    while True:
        pag.keyDown("a")
        time.sleep(0.15)
        pag.keyUp("a")
        r = ebutton()
        if r:
            convert()
            break
        if time.perf_counter()  - st > 30/28*setdat["walkspeed"]:
            webhook("","Cant find hive, resetting","dark brown",1)
            reset.reset()
            break
    reset.reset()
def checkRespawn(m,t):
    timing = float(loadtimings()[m])
    respt = int(''.join([x for x in list(t) if x.isdigit()]))
    if t[-1] == 'h':
        respt = respt*60*60
    else:
        respt = respt*60
    collectList = [x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("collect_")]
    if setdat['gifted_vicious_bee'] and m not in collectList:
        respt = respt/100*85
    if time.time() - timing > respt:
        return 1
    return 0

def savesettings(dictionary):
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
    while True:
        r = imagesearch.find('disconnect.png',0.8,ww//3,wh//2.8,ww//2.3,wh//2.5)
        if r:
            dc.value = 1
            webhook("","Disconnected","red")
            rejoin()
            dc.value = 0
        
        #if imagesearch.find('died.png',0.43,ww//2,wh//2,ww,wh,1):
            #dc.value = 1
            #webhook("","Unexpected Death","red")
            #dc.value = 0
        
        if gat.value:
            bpcap.value = backpack.bpc()
            resetMobTimer(cf.value.lower())
            
            

def killMob(field,mob,reset):
    webhook("","Traveling: {} ({})".format(mob.title(),field.title()),"dark brown")
    convert()
    canon()
    exec(open("field_{}.py".format(field)).read())
    lootMob(field,mob,reset)
    
def lootMob(field,mob,resetCheck):
    start = time.time()
    move.apkey("space")
    webhook("","Looting: {} ({})".format(mob.title(), field.title()),"bright green")
    while True:
        moblootPattern(1.1,1.4,"none",2)
        if time.time() - start > 15:
            break
    resetMobTimer(field.replace(" ","").lower())
    if resetCheck:
        reset.reset()
        convert()

def collect(name):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    dispname = name.title()
    usename = name.replace(" ","")
    for _ in range(2):
        convert()
        canon()
        webhook("","Traveling: {}".format(dispname),"dark brown")
        exec(open("collect_{}.py".format(usename)).read())
        time.sleep(0.5)
        if ebutton():
            webhook("","Collected: {}".format(dispname),"bright green",1)
            break
        webhook("","Unable To Collect: {}".format(dispname),"dark brown",1)
        reset.reset()
    savetimings(usename)
    move.press('e')
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
        webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
        time.sleep(7)
        _,x,y,_ = imagesearch.find('playbutton.png',0.8)
        webhook("","Play Button Found","dark brown")
        if setdat['display_type'] == "built-in retina display":
            pag.click(x//2, y//2)
        else:
            pag.click(x, y)
    time.sleep(50)
    move.hold("w",5)
    move.hold("s",0.55)
    foundHive = 0
    while True:
        if imagesearch.find('sprinkler.png',0.5,0,wh//2,ww,wh//2):
            break
    
    webhook("","Finding Hive", "dark brown")
    if setdat['hive_number'] == 3:
        if ebutton():
            move.press('e')
            foundHive = 1
            webhook("","Hive Found","dark brown")
    elif setdat['hive_number'] == 2:
        move.hold('d',1.2)
        if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found","dark brown")
    elif setdat['hive_number'] == 1:
        move.hold('d',2.3)
        if ebutton():
            move.press('e')
            foundHive = 1
            webhook("","Hive Found","dark brown")
    elif setdat['hive_number'] == 4:
        move.hold('a',1.1)
        if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found","dark brown")
    elif setdat['hive_number'] == 5:
        move.hold('a',2.3)
        if ebutton():
            move.press('e')
            foundHive = 1
            webhook("","Hive Found","dark brown")
    else:
        move.hold('a',3.3)
        if ebutton():
                move.press('e')
                foundHive = 1
                webhook("","Hive Found","dark brown")
    while True:   
        if not foundHive:
            move.hold("d",12)
            webhook("","Hive already claimed, finding new hive","dark brown")
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
        pag.keyDown("d")
        while time.time()-starttime < 10:
            key.press("e")
        pag.keyUp("d")
        updateHive(6) 
    convert()

    
'''
root = tkinter.Tk()
root.withdraw()
ww,wh = root.winfo_screenwidth(), root.winfo_screenheight()
print("{},{}".format(ww,wh))
root.destroy()

updateSave("ww",ww)
updateSave("wh",wh)
'''
            
    
def startLoop(cf,bpcap,gat,dc):
    val = validateSettings()

    if val:
        pag.alert(text='Your settings are incorrect! Check the terminal to see what is wrong.', title='Invalid settings', button='OK')
        print(val)
        sys.exit()
        
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    reset.reset()
    convert()
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    while True:
        timings = loadtimings()
        setdat = loadsettings.load()
        #Stump snail check
        if setdat['stump_snail'] and checkRespawn("stump_snail","96h"):
            canon()
            webhook("","Traveling: Stump snail (stump) ","brown")
            exec(open("field_stump.py").read())
            time.sleep(0.2)
            move.press("1")
            pag.click()
            webhook("","Starting stump snail","brown")
            while True:
                time.sleep(10)
                pag.click()
                if imagesearch.find("keepold.png",0.9):break
            webhook("","Stump snail killed, keeping amulet","bright green")
            savetimings("stump_snail")
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
            webhook("","Traveling: {}".format(setdat['gather_field']),"dark brown")
            exec(open("field_{}.py".format(setdat['gather_field'])).read())
            cf.value = setdat['gather_field'].replace(" ","").lower()
            time.sleep(0.2)
            if setdat["before_gather_turn"] == "left":
                for _ in range(setdat["turn_times"]):
                    move.press(",")
            elif setdat["before_gather_turn"] == "right":
                for _ in range(setdat["turn_times"]):
                    move.press(".")
            time.sleep(0.2)
            move.press("1")
            pag.click()
            gp = setdat["gather_pattern"].lower()
            webhook("Gathering: {}".format(setdat['gather_field']),"Limit: {}.00 - {} - Backpack: {}%".format(setdat["gather_time"],setdat["gather_pattern"],setdat["pack"]),"light green")
            move.apkey("space")
            time.sleep(0.2)
            timestart = time.perf_counter()
            gat.value = 1
            fullTime = 0
            while True:
                time.sleep(0.05)
                pag.mouseDown()
                time.sleep(0.05)
                exec(open("gather_{}.py".format(gp)).read())
                time.sleep(0.05)
                pag.mouseUp()
                time.sleep(0.05)
                timespent = (time.perf_counter() - timestart)/60
                if bpcap.value > setdat["pack"]:
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
            if setdat["before_gather_turn"] == "left":
                for _ in range(setdat["turn_times"]):
                    move.press(".")
            elif setdat["before_gather_turn"] == "right":
                for _ in range(setdat["turn_times"]):
                    move.press(",")
                    
            if setdat['return_to_hive'] == "walk":
                walk_to_hive()
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
                    walk_to_hive()
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
    dt = loadsettings.load()["display_type"]
    if dt == "built-in retina display":
        wwd *=  2
        whd *= 2
    with open('save.txt', 'w') as f:
        f.write('wh:{}\nww:{}'.format(whd,wwd))
            
if __name__ == "__main__":
    setResolution()
    loadSave()
    ww = savedata["ww"]
    wh = savedata["wh"]
    root = tk.Tk()
    root.geometry('700x400')
    s = ttk.Style()
    s.theme_use("aqua")
    wbgc = '#E4E4E4'
    s.configure('frame.TFrame', background=wbgc)
    root.configure(background='#ECECEC')
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, pady = 5)
    root.title("exih_macro")
    # create frames
    frame1 = ttk.Frame(notebook, width=700, height=400,style='frame.TFrame')
    frame2 = ttk.Frame(notebook, width=700, height=400,style='frame.TFrame')
    frame3 = ttk.Frame(notebook, width=700, height=400,style='frame.TFrame')
    frame4 = ttk.Frame(notebook, width=700, height=400,style='frame.TFrame')
    frame5 = ttk.Frame(notebook, width=700, height=400,style='frame.TFrame')
    frame6 = ttk.Frame(notebook, width=700, height=400,style='frame.TFrame')

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
    gather_field = tk.StringVar(root)
    gather_field.set(setdat["gather_field"].title())
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
    discord_bot_token = setdat['discord_bot_token']
    field_drift_compensation = tk.IntVar(value=setdat["field_drift_compensation"])

    wealthclock = tk.IntVar(value=setdat["wealthclock"])
    blueberrydispenser = tk.IntVar(value=setdat["blueberrydispenser"])
    strawberrydispenser = tk.IntVar(value=setdat["strawberrydispenser"])
    royaljellydispenser  = tk.IntVar(value=setdat["royaljellydispenser"])
    treatdispenser = tk.IntVar(value=setdat["treatdispenser"])

    ebthreshold = setdat['ebthreshold']
    ebdetect = tk.StringVar(root)
    ebdetect.set(setdat["ebdetect"])
    wwa  = savedata['ww']
    wha = savedata['wh']
    
    def calibratehive():
        exec(open("calibrate_hive.py").read())
    def updateGo():
        update.update()
        exit()
    def updateExp():
        updateexperiment.update()
        exit()

    def expu():
        window = tk.Toplevel() #creates a window to confirm if the user wants to start deleting files
        window.config(bg=wbgc)
        label = tk.Label(window, text="Are you sure you want to update the macro to experimental version?\n(your settings and images will be replaced)\nYou can click the update button to go back to the main macro",bg=wbgc)
        button_yes = tk.Button(window, text="Yes", highlightbackground=wbgc,command=updateExp)
        button_no = tk.Button(window, text="No", highlightbackground=wbgc, command=window.destroy)
        label.grid(row=0, column=0, columnspan=2)
        button_yes.grid(row=1, column=0)
        button_no.grid(row=1, column=1)
        
    def updateFiles():
        window = tk.Toplevel() #creates a window to confirm if the user wants to start deleting files
        window.config(bg=wbgc)
        label = tk.Label(window, text="Are you sure you want to update the macro?\n(your settings and images will be replaced)",bg=wbgc)
        button_yes = tk.Button(window, text="Yes", highlightbackground=wbgc,command=updateGo)
        button_no = tk.Button(window, text="No", highlightbackground=wbgc, command=window.destroy)
        label.grid(row=0, column=0, columnspan=2)
        button_yes.grid(row=1, column=0)
        button_no.grid(row=1, column=1)
         
    def startGo():
        global setdat, stop
        setdat = loadsettings.load()
        setdict = {
            "hive_number": hive_number.get(),
            "walkspeed": speedtextbox.get(1.0,"end").replace("\n",""),
            "gifted_vicious_bee": gifted_vicious_bee.get(),
            "enable_discord_webhook": enable_discord_webhook.get(),
            "discord_webhook_url": urltextbox.get(1.0,"end").replace("\n",""),
            "send_screenshot": send_screenshot.get(),
            
            "gather_enable": gather_enable.get(),
            "gather_field": gather_field.get(),
            "gather_pattern": gather_pattern.get(),
            "gather_size": gather_size.get(),
            "gather_width": gather_width.get(),
            "gather_time": timetextbox.get(1.0,"end").replace("\n",""),
            "pack": packtextbox.get(1.0,"end").replace("\n",""),
            "before_gather_turn": before_gather_turn.get(),
            "turn_times": turn_times.get(),
            "return_to_hive": return_to_hive.get(),
            "whirligig_slot": whirligig_slot.get(),
            "display_type": display_type.get().lower(),
            "private_server_link":linktextbox.get(1.0,"end").replace("\n",""),
            "enable_discord_bot":enable_discord_bot.get(),
            "discord_bot_token":tokentextbox.get(1.0,"end").replace("\n",""),
            "field_drift_compensation": field_drift_compensation.get(),
            
            "stump_snail": stump_snail.get(),
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

            "hivethreshold":setdat['hivethreshold'],
            "ebthreshold":ebtextbox.get(1.0,"end").replace("\n",""),
            "ebdetect":ebdetect.get()

            }
        #ww = int(wwatextbox.get(1.0,"end").replace("\n",""))
        #wh = int(whatextbox.get(1.0,"end").replace("\n",""))
        #if setdict["display_type"] == "built-in retina display":
            #if ww<2000:
                #pag.alert(text='The resolution is invalid for a built-in retina display. Check it by going to about this mac -> displays', title='Setting error', button='OK')
                #return
        try:
            a = float(setdict["walkspeed"])
        except:
            pag.alert(text="The walkspeed of {} is not a valid number/decimal".format(setdict['walkspeed']),title="Invalid setting",button="OK")
            return
        with open('save.txt', 'w') as f:
            f.write('wh:{}\nww:{}'.format(wh,ww))
        f.close()
        savesettings(setdict)
        webhook("Macro started","exih_macro {}".format(macrov),"dark brown")
        setdat = loadsettings.load()
        startLoop_proc = multiprocessing.Process(target=startLoop,args=(currentfield,bpc,gather,disconnected))
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
                    startLoop_proc = multiprocessing.Process(target=startLoop,args=(currentfield,bpc,gather,disconnected))
                    startLoop_proc.start()
        except KeyboardInterrupt:
            startLoop_proc.terminate()
            background_proc.terminate()
            if setdat['enable_discord_bot']:
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
            
    #Tab 1
    tkinter.Checkbutton(frame1, text="Enable Gathering", variable=gather_enable, bg = wbgc).place(x=0, y = 15)
    dropField = tkinter.OptionMenu(frame1, gather_field, *[x.split("_")[1][:-3].title() for x in os.listdir("./") if x.startswith("field_")] )
    dropField.place(width=110,x = 120, y = 50)
    tkinter.Label(frame1, text = "Gathering Field", bg = wbgc).place(x = 0, y = 50)

    tkinter.Label(frame1, text = "Gathering Pattern", bg = wbgc).place(x = 0, y = 85)
    dropField = tkinter.OptionMenu(frame1, gather_pattern, *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")])
    dropField.place(width=110,x = 120, y = 85)
    tkinter.Label(frame1, text = "Size", bg = wbgc).place(x = 250, y = 85)
    dropField = tkinter.OptionMenu(frame1, gather_size, *["S","M","L"] )
    dropField.place(width=50,x = 290, y = 85)
    tkinter.Label(frame1, text = "Width", bg = wbgc).place(x = 360, y = 85)
    dropField = tkinter.OptionMenu(frame1, gather_width, *[(x+1) for x in range(10)] )
    dropField.place(width=50,x = 410, y = 85)

    tkinter.Label(frame1, text = "Before Gathering, Rotate Camera", bg = wbgc).place(x = 0, y = 120)
    dropField = tkinter.OptionMenu(frame1, before_gather_turn, *["None","Left","Right"] )
    dropField.place(width=60,x = 210, y = 120)
    dropField = tkinter.OptionMenu(frame1, turn_times, *[(x+1) for x in range(4)] )
    dropField.place(width=50,x = 275, y = 120)

    tkinter.Label(frame1, text = "Gather Until:", bg = wbgc).place(x = 0, y = 155)
    tkinter.Label(frame1, text = "Mins", bg = wbgc).place(x = 90, y = 155)
    timetextbox = tkinter.Text(frame1, width = 4, height = 1)
    timetextbox.insert("end",gather_time)
    timetextbox.place(x = 130, y=158)
    tkinter.Label(frame1, text = "Backpack%", bg = wbgc).place(x = 175, y = 155)
    packtextbox = tkinter.Text(frame1, width = 4, height = 1)
    packtextbox.insert("end",pack)
    packtextbox.place(x = 260, y=158)
    tkinter.Label(frame1, text = "To Hive By", bg = wbgc).place(x = 305, y = 155)
    dropConvert = tkinter.OptionMenu(frame1 , return_to_hive, command = disablews, *["Walk","Reset","Rejoin","Whirligig"])
    dropConvert.place(width=85,x = 380, y = 155)
    tkinter.Label(frame1, text = "Whirligig Slot", bg = wbgc).place(x = 480, y = 155)
    wslotmenu = tkinter.OptionMenu(frame1 , whirligig_slot, *[1,2,3,4,5,6,7,"none"])
    wslotmenu.place(width=70,x = 570, y = 155)

    tkinter.Checkbutton(frame1, text="Field Drift Compensation", variable=field_drift_compensation, bg = wbgc).place(x=0, y = 190)
    

    #Tab 2 
    tkinter.Checkbutton(frame2, text="Apply gifted vicious bee hive bonus", variable=gifted_vicious_bee, bg = wbgc).place(x=0, y = 15)
    tkinter.Checkbutton(frame2, text="Stump Snail", variable=stump_snail, bg = wbgc).place(x=0, y = 50)
    tkinter.Checkbutton(frame2, text="Ladybug", variable=ladybug, bg = wbgc).place(x=0, y = 85)
    tkinter.Checkbutton(frame2, text="Rhino Beetle", variable=rhinobeetle, bg = wbgc).place(x=80, y = 85)
    tkinter.Checkbutton(frame2, text="Scorpion", variable=scorpion, bg = wbgc).place(x=190, y = 85)
    tkinter.Checkbutton(frame2, text="Mantis", variable=mantis, bg = wbgc).place(x=275, y = 85)
    tkinter.Checkbutton(frame2, text="Spider", variable=spider, bg = wbgc).place(x=345, y = 85)
    tkinter.Checkbutton(frame2, text="Werewolf", variable=werewolf, bg = wbgc).place(x=415, y = 85)

    #Tab 3
    tkinter.Checkbutton(frame4, text="Wealth Clock", variable=wealthclock, bg = wbgc).place(x=0, y = 15)
    tkinter.Checkbutton(frame4, text="Blueberry Dispenser", variable=blueberrydispenser, bg = wbgc).place(x=0, y = 50)
    tkinter.Checkbutton(frame4, text="Strawberry Dispenser", variable=strawberrydispenser, bg = wbgc).place(x=160, y = 50)
    tkinter.Checkbutton(frame4, text="(Free) Royal Jelly Dispenser", variable=royaljellydispenser, bg = wbgc).place(x=320, y = 50)
    tkinter.Checkbutton(frame4, text="Treat Dispenser", variable=treatdispenser, bg = wbgc).place(x=520, y = 50)
    #Tab 4
    
    
    #Tab 5
    tkinter.Label(frame3, text = "Hive Slot (6-5-4-3-2-1)", bg = wbgc).place(x = 0, y = 15)
    dropField = tkinter.OptionMenu(frame3, hive_number, *[x+1 for x in range(6)] )
    dropField.place(width=60,x = 160, y = 15)
    tkinter.Label(frame3, text = "Move Speed (without haste)", bg = wbgc).place(x = 0, y = 50)
    speedtextbox = tkinter.Text(frame3, width = 4, height = 1)
    speedtextbox.insert("end",walkspeed)
    speedtextbox.place(x = 185, y=52)
    tkinter.Checkbutton(frame3, text="Enable Discord Webhook", command = disabledw,variable=enable_discord_webhook, bg = wbgc).place(x=0, y = 85)
    tkinter.Label(frame3, text = "Discord Webhook Link", bg = wbgc).place(x = 350, y = 85)
    urltextbox = tkinter.Text(frame3, width = 24, height = 1, xscrollcommand = True)
    urltextbox.insert("end",discord_webhook_url)
    sendss = tkinter.Checkbutton(frame3, text="Send screenshots", variable=send_screenshot, bg = wbgc)
    sendss.place(x=200, y = 85)
    urltextbox.place(x = 500, y=87)
    tkinter.Label(frame3, text = "Screen Resolution: Currently detected automatically. No need to configure", bg = wbgc).place(x = 0, y = 120)
    #tkinter.Label(frame3, text = "Width", bg = wbgc).place(x = 150, y = 120)
    #wwatextbox = tkinter.Text(frame3, width = 5, height = 1)
    #wwatextbox.insert("end",wwa)
    #wwatextbox.place(x=200,y=122)
    #tkinter.Label(frame3, text = "Height", bg = wbgc).place(x = 260, y = 120)
    #whatextbox = tkinter.Text(frame3, width = 5, height = 1)
    #whatextbox.insert("end",wha)
    #whatextbox.place(x=310,y=122)
    tkinter.Label(frame3, text = "Display type", bg = wbgc).place(x = 0, y = 155)
    dropField = tkinter.OptionMenu(frame3, display_type, command = savedisplaytype, *["Built-in retina display","Built-in display"] )
    dropField.place(width=160,x = 100, y = 155)
    tkinter.Label(frame3, text = "Private Server Link", bg = wbgc).place(x = 0, y = 190)
    linktextbox = tkinter.Text(frame3, width = 24, height = 1)
    linktextbox.insert("end",private_server_link)
    linktextbox.place(x=150,y=192)
    tkinter.Checkbutton(frame3, text="Enable Discord Bot", variable=enable_discord_bot, bg = wbgc).place(x=0, y = 225)
    tkinter.Label(frame3, text = "Discord Bot Token", bg = wbgc).place(x = 170, y = 226)
    tokentextbox = tkinter.Text(frame3, width = 24, height = 1)
    tokentextbox.insert("end",discord_bot_token)
    tokentextbox.place(x = 300, y=228)
    #Tab 6
    tkinter.Button(frame5, text = "Calibrate Hive",command = calibratehive, height = 1, width = 7 ).place(x=0,y=15)
    tkinter.Label(frame5, text = "E Button Detection Type", bg = wbgc).place(x = 0, y = 50)
    dropField = tkinter.OptionMenu(frame5, ebdetect, command = disableeb, *["cv2","pyautogui"] )
    dropField.place(width=130,x = 158, y = 51)
    tkinter.Label(frame5, text = " Threshold", bg = wbgc).place(x = 300, y = 50)
    ebtextbox = tkinter.Text(frame5, width = 4, height = 1)
    ebtextbox.insert("end",ebthreshold)
    ebtextbox.place(x=380,y=53)
    #Root
    tkinter.Button(root, text = "Start",command = startGo, height = 2, width = 7 ).place(x=10,y=350)
    tkinter.Button(root, text = "Update",command = updateFiles, height = 1, width = 5,).place(x=600,y=370)
    tkinter.Button(root, text = "Experimental update",command = expu, height = 1, width = 12,).place(x=450,y=370)
    tkinter.Label(root, text = "version {}".format(macrov), bg = wbgc).place(x = 600, y = 350)
    
    disablews("1")
    disabledw()
    disableeb("1")
    root.mainloop()
    


        




