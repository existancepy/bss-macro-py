import pyautogui as pag
import time
import os
import tkinter
import move
import loadsettings
import reset
import gather_e_lol
import gather_squares
import backpack
import sys
import imagesearch
from webhook import webhook

stumpsnail = 0
re = "walk"
savedata = {}

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
        templist.append("{}:{}".format(m,tempdict[m]))
    with open('timings.txt') as f:
        f.writelines(templist)
    f.close()
    
loadSave()
ww = savedata["ww"]
wh = savedata["wh"]

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
    os.system(cmd)
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
def walk_to_hive():
    webhook("","Going back to hive","dark brown")
    exec(open("walk_{}.py".format(setdat['gather_field'])).read())
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
        respt = respt*1000*60*60
    else:
        respt = respt*1000*60
        
    if setdat['gifted_vicious_bee']:
        respt = respt/100*85
    if time.time() - timing > respt:
        return 1
    return 0
    
'''
root = tkinter.Tk()
root.withdraw()
ww,wh = root.winfo_screenwidth(), root.winfo_screenheight()
print("{},{}".format(ww,wh))
root.destroy()

updateSave("ww",ww)
updateSave("wh",wh)
'''

val = validateSettings()

if val:
    pag.alert(text='Your settings are incorrect! Check the terminal to see what is wrong.', title='Invalid settings', button='OK')
    print(val)
    sys.exit()
    

setdat = loadsettings.load()
cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)

reset.reset()
convert()
while True:
    timings = loadtimings()
    if setdat['stump_snail'] and checkRespawn("stump_snail","96h"):
        canon()
        webhook("","Traveling: Stump snail (stump) ","brown")
        exec(open("field_stump.py").read())
        time.sleep(0.2)
        move.press("1")
        pag.click()
        while True:
            webhook("","Starting stump snail","brown")
            time.sleep(10)
            pag.click()
            if imagesearch.find("./images/keepold.png",0.9):
                break
        webhook("","Stump snail killed, keeping amulet","bright green")
        savetimings("stump_snail")
        pag.moveTo(mw//2-30,mh//100*60)
        pag.click()
    elif setdat['gather_enable']:
        canon()
        webhook("","Traveling: {}".format(setdat['gather_field']),"dark brown")
        exec(open("field_{}.py".format(setdat['gather_field'])).read())
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
        gp = setdat["gather_pattern"]
        os.system(cmd)
        webhook("Gathering: {}".format(setdat['gather_field']),"Limit: {}.00 - {} - Backpack: {}%".format(setdat["gather_time"],setdat["gather_pattern"],setdat["pack"]),"light green")
        move.apkey("space")
        timestart = time.perf_counter()
        while True:
            pag.mouseDown()
            if gp == "squares":
                gather_squares.gather()
            elif gp == "e_lol":
                gather_e_lol.gather()
                
            pag.mouseUp()
            timespent = (time.perf_counter() - timestart)/60
            if backpack.bpc() > setdat["pack"]:
                webhook("Gathering: ended","Time: {:.2f} - Backpack - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
                break
            if timespent > setdat["gather_time"]:
                webhook("Gathering: ended","Time: {:.2f} - Time Limit - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
                break
        
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
        elif setdat['return_to_hive'] == "whirligig":
            webhook("","Activating whirligig","dark brown")
            move.press(str(setdat['whirligig_slot']))
            time.sleep(1)
            r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
            if not r:
                webhook("","Whirligig failed to activate, walking back","red")
                walk_to_hive()
            else:
                convert()
            
            
            


        




