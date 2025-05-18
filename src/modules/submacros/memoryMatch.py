import time
import modules.controls.mouse as mouse
import imagehash
from modules.screen.screenshot import mssScreenshot
import pyautogui as pag
import random
from modules.screen.ocr import ocrRead
from PIL import Image
from modules.misc.imageManipulation import adjustImage
from modules.screen.imageSearch import locateImageOnScreen

#V1's memory match, slightly modified for lag compensation
#TODO: clean up the code, really messy, lots of copy paste
mw, mh = pag.size()
def solveMemoryMatch(mmType, displayType):
    blankTile = imagehash.average_hash(Image.open("./images/menu/mmempty.png"))
    def mmclick(x,y):
        mouse.moveTo(x, y, 0.2)
        time.sleep(0.3)
        mouse.click()

    #wait for the tile to flip over
    #compensates for lag
    def waitForTileShow(x, y):
        st = time.time()
        while time.time()-st < 3: #max 3s of waiting
            tile = screenshotItem(x,y)
            if not similarImages(tile, blankTile): #if the tile is not the same as the reference, it has flipped
                time.sleep(0.2) #wait for the tile flip animation
                tile = screenshotItem(x,y) #get a new screenshot
                break
        return tile
    
    #return true if img1 and img2 are similar
    #img1, img2 are hash values of the images
    def similarImages(img1,img2):
        return img1 - img2 < 2

    #return a image hash of the item at the tile
    def screenshotItem(x,y):
        screenshot = mssScreenshot(x-30, y-20, 50, 30)
        return imagehash.average_hash(screenshot)

    #get coordinates of grid
    gridSize = [4,4]
    checkedCoords = set() #store the coords the macro has checked
    claimedCoords = set() #store the index that has been claimed
    middleX = mw//2
    middleY = mh//2
    offsetX = 0
    offsetY = 0
    if mmType.lower() in ["extreme","winter"]:
        offsetX = 40
        gridSize = [5,4]
    gridCoords = []
    mmData = [None]*(gridSize[0]*gridSize[1]) #store the hashed images of each mm tile
    for i in range(1,gridSize[0]+1):
        x = middleX-200+80*i
        for j in range(1,gridSize[1]+1):
            y = middleY-200+80*j
            gridCoords.append([x,y])
    #randomise the grid positions
    random.shuffle(gridCoords)

    #get number of attempts (defaults to 10)
    attempts = 10
    try:
        cap = mssScreenshot(middleX-275-offsetX, middleY-146, 100, 100)
        #read the attempt screen
        #get only numbers from the ocr result
        attemptsOCR = int(''.join([x[1][0] for x in ocrRead(cap) if x[1][0].isdigit()]))
        #min 3, max 10
        if 3 <= attemptsOCR <= 10:
            attempts = attemptsOCR
            print(f"Number of attempts: {attempts}")
    except Exception as e:
        print(e)
            
    matchFound = None #store the value of the match
    skipAttempt = False
    currAttempt = 0
    while currAttempt <= attempts:
        print(currAttempt)
        if skipAttempt:
            skipAttempt = False
            continue
        if currAttempt > attempts:
            mmImg = adjustImage("./images/menu", "mmopen", displayType) #memory match
            if not locateImageOnScreen(mmImg, mw/4, mh/4, mw/4, mh/3.5, 0.8):
                #print("Terminated early")
                #break
                pass
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
            mouse.moveTo(x = middleX, y = middleY-190) #move the mouse out of the way of the img
            tileImg = waitForTileShow(x,y)
            checkedCoords.add((xr,yr))
            #check if the image matches with anything
            for j,img in enumerate(mmData):
                if not img: continue
                if j in claimedCoords: continue
                if similarImages(tileImg,img):
                    matchFound = j
                    claimedCoords.add(i)
                    claimedCoords.add(j)
                    break
            mmData[i] = tileImg #add the img
            firstTile = i
            break
        
        time.sleep(0.8) 
        #second tile

        if matchFound:
            print("match found, 1st tile")
            x,y  = gridCoords[matchFound]
            mmclick(x-offsetX, y-offsetY)
        else:
            for i,e in enumerate(gridCoords):
                xr,yr = e
                if (xr,yr) in checkedCoords: continue
                x = xr-offsetX
                y = yr-offsetY
                mmclick(x,y)
                time.sleep(0.1)
                mouse.moveTo(x = middleX, y = middleY-190) #move the mouse out of the way of the img
                tileImg = waitForTileShow(x,y)
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
                            claimedCoords.add(j)
                            break
                        print("match found, 2nd tile")
                        #since its the 2nd tile, its a new "turn"
                        time.sleep(2)
                        mmclick(x,y) #first tile, click the prev 2nd tile
                        time.sleep(1)
                        xr2,yr2 = gridCoords[j]
                        x2 = xr2-offsetX
                        y2 = yr2-offsetY
                        mmclick(x2,y2) #click the tile that matches
                        currAttempt += 1
                        claimedCoords.add(i)
                        claimedCoords.add(j)
                        break
                mmData[i] = tileImg #add the img 
                break
        currAttempt += 1
        time.sleep(0.8)