import pyautogui as pag
import loadsettings
import os
import time
import mss
import mss.tools
import imagehash
from PIL import Image

def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(3)

def terminal():
    cmd = """
    osascript -e 'activate application "Terminal"' 
    """
    os.system(cmd)
    
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

roblox()

def mmclick(x,y):
    pag.moveTo(x = x, y = y)
    time.sleep(0.4)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()
    
#return true if img1 and img2 are similar
#img1, img2 are hash values of the images
def similarImages(img1,img2):
    return img1 - img2 < 2

#return a pillow obj of the item at the tile
def screenshotItem(x,y):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": x-35, "top": y-20, "width": 50, "height": 30}
        # Grab the data and convert to pillow img
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        #save it as a img
        output = "{}.png".format(time.time())
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    #then convert it to a hash
    return imagehash.average_hash(img)


savedata = loadRes()
mw, mh = pag.size()

#get coordinates of grid
gridCoords = []
mmData = [None]*20 #store the hashed images of each mm tile
checkedCoords = set() #store the coords the macro has checked
claimedCoords = set() #store the index that has been claimed
middleX = mw//2
middleY = mh//2
offsetX = 16
offsetY = 0
for i in range(1,6):
    x = middleX-200+80*i
    for j in range(1,5):
        y = middleY-200+80*j
        gridCoords.append([x,y])
        
matchFound = None #store the value of the match
skipAttempt = False
for _ in range(8):
    if skipAttempt:
        skipAttempt = False
        continue

    firstTile = None
    matchFound = None
    #open first tile
    for i,e in enumerate(gridCoords):
        xr,yr = e
        if (xr,yr) in checkedCoords: continue
        x = xr-offsetX
        y = yr-offsetY
        mmclick(x,y)
        time.sleep(0.1)
        pag.moveTo(x = middleX, y = middleY-190) #move the mouse out of the way of the img
        time.sleep(0.6)
        tileImg = screenshotItem(x,y)
        checkedCoords.add((xr,yr))
        #check if the image matches with anything
        for j,img in enumerate(mmData):
            if not img: continue
            if j in claimedCoords: continue
            if similarImages(tileImg,img):
                matchFound = j
                claimedCoords.add(i)
                claimCoords.add(j)
                break
        mmData[i] = tileImg #add the img
        firstTile = i
        break
    
    time.sleep(0.8)
    #second tile

    if matchFound:
        print("match found, 1st tile")
        mmclick(*gridCoords[matchFound])
    else:
        for i,e in enumerate(gridCoords):
            xr,yr = e
            if (xr,yr) in checkedCoords: continue
            x = xr-offsetX
            y = yr-offsetY
            mmclick(x,y)
            time.sleep(0.1)
            pag.moveTo(x = middleX, y = middleY-190) #move the mouse out of the way of the img
            time.sleep(0.3)
            tileImg = screenshotItem(x,y)
            checkedCoords.add((xr,yr))
            #check if the image matches with anything
            for j,img in enumerate(mmData):
                if not img: continue
                if j in claimedCoords: continue
                if similarImages(tileImg,img):
                    #check if the 1st tile = 2nd tile, got lucky
                    if (j == firstTile):
                        print("match found, same attempt")
                        claimedCoords.add(i)
                        claimCoords.add(j)
                        break
                    print("match found, 2nd tile")
                    #since its the 2nd tile, its a new "turn"
                    time.sleep(2)
                    mmclick(x,y) #first tile, click the prev 2nd tile
                    time.sleep(1)
                    mmclick(*gridCoords[j]) #click the tile that matches
                    skipAttempt = True
                    claimedCoords.add(i)
                    claimCoords.add(j)
                    break
            mmData[i] = tileImg #add the img 
            break
    time.sleep(0.8)
        

terminal()


