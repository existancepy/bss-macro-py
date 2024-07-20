import loadsettings
import move
import time
from ocrpy import imToString,customOCR,ocrRead
import pyautogui as pag
from pixelcolour import getPixelColor

def pagmove(k,t):
    pag.keyDown(k)
    time.sleep(t)
    pag.keyUp(k)

def pagPress(key, delay = 0.02):
    pag.keyDown(key, _pause = False)
    time.sleep(delay)
    pag.keyUp(key, _pause = False)
    
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
        elif "planter" in text and "yes" in text:
            webhook("","Detected planter pop up present","brown",1)
            clickYes()
        elif lowBattery():
            setStatus("disconnect")
            webhook("","Low battery detected","red",1)
            return True
    elif m == "dialog":
        if "bear" in text:
            return True
    return False

def getBesideE():
    text = imToString("bee bear").lower()
    log(text)
    return text

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
    while True:
        try:
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
        except Exception as e:
            log(f"loadRes failed: {e}")
            
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
    
    for i in range(5):
        webhook("","Resetting character, Attempt: {}".format(i+1),"dark brown")
        mouse.position = (mw/(xsm*4.11)+40,(mh/(9*ysm))+yOffset)
        time.sleep(0.5)
        pagPress('esc')
        time.sleep(0.1)
        pagPress('r')
        time.sleep(0.2)
        pagPress('enter')
        if not i:
            if checkwithOCR("disconnect"): return
            time.sleep(7)
        else:
            time.sleep(8.5)
        besideE = getBesideE()
        if "make" in besideE or "honey" in besideE or "flower" in besideE or "field" in besideE:
            break
    else:
        webhook("Notice","Unable to detect that player has respawned at hive, continuing","red",1)
        return False

    for _ in range(4):
        pix = getPixelColor((ww//2)+15,wh-2)
        r = [int(x) for x in pix]
        log(r)
        log(abs(r[2]-r[1]))
        log(abs(r[2]-r[0]))
        log(abs(r[1]-r[0]))
        log("real")
        avgDiff = (abs(r[2]-r[1])+abs(r[2]-r[0])+abs(r[1]-r[0]))/3
        log(avgDiff)
        if avgDiff < 20:
            for _ in range(8):
                pagPress("o")
            return True
        
        for _ in range(4):
            pagPress(".")
            time.sleep(0.1)
    time.sleep(0.3)
    if hiveCheck:
        webhook("Notice","Hive not found.","red",1)
    else:
        webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)
    return False


def feed(name, quantity):
    setdat = loadsettings.load()
    ww = savedata['ww']
    wh = savedata['wh']
    while not reset():
        pass
    
    pag.typewrite("\\")
    for _ in range(5):
        keyboard.press(Key.up)
        time.sleep(0.05)
        keyboard.release(Key.up)
        time.sleep(0.1)   
    keyboard.press(Key.down)
    time.sleep(0.05)
    keyboard.release(Key.down)
    
    for _ in range(4):
        keyboard.press(Key.left)
        time.sleep(0.05)
        keyboard.release(Key.left)
        time.sleep(0.1)

    move.press("enter")
    time.sleep(1)
    keyboard.press("s")
    time.sleep(0.05)
    keyboard.release("s")
    time.sleep(0.5)
    for _ in range(20):
        keyboard.press(Key.page_up)
        time.sleep(0.02)
        keyboard.release(Key.page_up)
        time.sleep(0.01)

    foundItem = ""
    for _ in range(40):
        ocr = customOCR(0,wh/7,ww/(4.3),wh/2,0)
        for x in ocr:
            text = x[1][0].lower()
            log(text)
            if name in text:
                foundItem = x
                break
        if foundItem: break
        for _ in range(4):
            keyboard.press(Key.page_down)
            time.sleep(0.02)
            keyboard.release(Key.page_down)
    pag.typewrite("\\")
    if foundItem:
       webhook("",f"Found {name} item in inventory", "brown")
    else:
        webhook("",f"Couldnt find {name} item in inventory", "red")
        reset()
        if setdat["haste_compensation"]: openSettings()
        return
    
    print(foundItem)
    multi = 1
    if setdat['display_type'] == "built-in retina display":
        multi = 2
    startY = ((wh/7 + foundItem[0][0][1])//multi)+30
    #re-adjust camera
    for _ in range(10):
        keyboard.press(Key.page_up)
        time.sleep(0.01)
        keyboard.release(Key.page_up)
        time.sleep(0.01)
    for _ in range(4):
        keyboard.press(Key.page_down)
        time.sleep(0.01)
        keyboard.release(Key.page_down)
        time.sleep(0.01)
 
    for _ in range(2):
        pag.moveTo(40,startY)
        time.sleep(0.3)
        pag.dragTo(mw//2, mh//2,0.7, button='left')
        
    time.sleep(0.5)
    pag.typewrite("\\")
    time.sleep(0.5)
    for _ in range(10):
        keyboard.press(Key.up)
        time.sleep(0.05)
        keyboard.release(Key.up)
        time.sleep(0.1)
        
    keyboard.press(Key.down)
    time.sleep(0.05)
    keyboard.release(Key.down)

    for _ in range(8):
        keyboard.press(Key.right)
        time.sleep(0.05)
        keyboard.release(Key.right)
        time.sleep(0.1)
        
    keyboard.press(Key.down)
    time.sleep(0.05)
    keyboard.release(Key.down)
    
    keyboard.press(Key.left)
    time.sleep(0.05)
    keyboard.release(Key.left)
    time.sleep(0.1)
    
    move.press("enter")
    time.sleep(0.2)
    pag.write(str(quantity), interval = 0.25)
    time.sleep(0.2)

    move.press("enter")
    keyboard.press(Key.left)
    time.sleep(0.05)
    keyboard.release(Key.left)
    move.press("enter")
    pag.typewrite("\\")
    webhook("",f"Fed {quantity} {name}", "bright green")
    #if setdat["haste_compensation"]: openSettings()

time.sleep(4)
feed("blueberry",10)
