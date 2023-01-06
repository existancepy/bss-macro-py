import pyautogui as pag
import time
import os
import tkinter
import move
import loadsettings
import reset
import gather_elol
import gather_squares
import backpack
import sys

stumpsnail = 0
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
loadSave()
ww = savedata["ww"]
wh = savedata["wh"]

ms = pag.size()
mw = ms[0]
mh = ms[1]
def canon():
    #Move to canon:
    print("Moving to canon")
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
            print("canon found")
            move.press("e")
            return
        if time.perf_counter()  - st > 10/28*setdat["walkspeed"]:
            print('no cannon')
            break
        
    reset.reset()   
    canon()
def convert():
    for _ in range(2):
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            print('starting convert')
            move.press("e")
            st = time.perf_counter()
            while True:
                c = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
            
                if not c:
                    print("convert done")
                    time.sleep(3)
                    break
                if time.perf_counter()  - st > 600:
                    print("converting took too long, moving on")
                    break
            
            break
        else:
            time.sleep(0.25)
    return
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
    print(val)
    sys.exit()
    

setdat = loadsettings.load()
cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)


if stumpsnail:
    reset.reset()
    convert()
    canon()
    exec("field_stump.py")
    time.sleep(0.2)
    move.press("1")
    pag.click()
    while True:
        time.sleep(10)
        pag.click()
elif setdat['gather_enable']:
    reset.reset()
    convert()
    canon()
    exec("field_{}.py".format(setdat['gather_field']))
    time.sleep(0.2)
    move.press(".")
    move.press(".")
    time.sleep(0.2)
    move.press("1")
    pag.click()
    gp = setdat["gather_pattern"]
    timestart = time.perf_counter()
    for _ in range(100):
        pag.mouseDown()
        if gp == "squares":
            gather_squares.gather()
        elif gp == "elol":
            gather_elol.gather()

            
        pag.mouseUp()
        if backpack.bpc() > setdat["pack"]:
            print('backpack')
            break
        if (time.perf_counter() - timestart)/60 > setdat["gather_time"]:
            print('time')
            break
    


    




