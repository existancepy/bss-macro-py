from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import cv2
import math
import time
import ast
import numpy as np
import platform
from modules.misc.messageBox import msgBox
from modules.screen.imageSearch import locateTransparentImageOnScreen, locateTransparentImage
from modules.screen.screenshot import mssScreenshotNP, mssScreenshot
from modules.misc.imageManipulation import adjustImage
import time
import pyautogui as pag
from modules.screen.ocr import ocrRead, imToString
import copy
from datetime import datetime
from modules.screen.robloxWindow import RobloxWindowBounds
import pickle
import json

ww, wh = pag.size()

def versionTuple(v):
    return tuple(map(int, (v.split("."))))
macVer = platform.mac_ver()[0]

# try:
#     hti = Html2Image(size=(1900, 850))
#     if hasattr(hti.browser, 'use_new_headless'):
#         hti.browser.use_new_headless = None

    
# except FileNotFoundError:
#     if versionTuple(macVer) >= versionTuple("10.15"):
#         msgBox(title = "error", text = "Google Chrome could not be found. Ensure that:\
#     \n1. Google Chrome is installed\nGoogle chrome is in the applications folder (open the google chrome dmg file. From the pop up, drag the icon into the folder)")
#     else:
#         hti = None

class BuffDetector():
    def __init__(self, robloxWindow: RobloxWindowBounds):

        self.robloxWindow = robloxWindow
        self.y = 33

        self.buffSize = 76 if self.robloxWindow.isRetina else 39

        self.nectars = {
            "comforting": [[np.array([0, 150, 63]), np.array([20, 155, 70])], (-2,0)],
            "invigorating": [[np.array([0, 128, 95]), np.array([180, 132, 101])], (-2,4)],
            "motivating": [[np.array([160, 150, 63]), np.array([170, 155, 70])], (-2,-2)],
            "refreshing": [[np.array([50, 144, 70]), np.array([70, 151, 75])], (-2,2)],
            "satisfying": [[np.array([130, 163, 36]), np.array([140, 168, 40])], (-2,0)]
        }
        self.nectarKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

    def screenshotBuffArea(self):
        return mssScreenshotNP(self.robloxWindow.mx, self.robloxWindow.my+self.robloxWindow.yOffset+33, self.robloxWindow.mw, 45)

    def getBuffQuantityFromImg(self, bgrImg,transform, crop=True, buff=None, intOnly=False):
        #buff size is 76x76
        lower = np.array([0, 102, 0])
        upper = np.array([100, 255, 31])
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        mask = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2HLS)
        if crop:
            #crop the text area
            h, w, *_ = mask.shape
            mask = mask[int(h * 0.58):, :]
        if transform:
            #extract only the text (white color)
            mask = cv2.inRange(mask, lower, upper)
            mask = cv2.erode(mask, kernel)
        mask = Image.fromarray(mask)
        if transform:
            mask = ImageOps.invert(mask)
            pass
        
        mask = mask.resize((mask.width * 3, mask.height * 3), Image.LANCZOS)

        #mask.save(f"{time.time()}.png")
        #read the text
        ocrText = ''.join([x[1][0] for x in ocrRead(mask)]).replace(":", ".")
        buffCount = ''.join([x for x in ocrText if x.isdigit() or (not intOnly and x == ".")])

        # Clean up the buffCount to ensure it's a valid number format
        # Remove leading/trailing dots and handle multiple dots
        if not intOnly:
            # Remove leading dots
            buffCount = buffCount.lstrip('.')
            # Remove trailing dots
            buffCount = buffCount.rstrip('.')
            # Replace multiple consecutive dots with single dot
            import re
            buffCount = re.sub(r'\.\.+', '.', buffCount)
            
            # Validate that the result is a valid number (handle cases like "5.3.7" or ".")
            if buffCount:
                try:
                    float(buffCount)
                except ValueError:
                    # If not a valid float, try to extract just the first valid number
                    # Split by '.' and take first two parts to make a valid decimal
                    parts = buffCount.split('.')
                    if len(parts) > 2:
                        # Multiple dots: take first integer part and first decimal part
                        buffCount = f"{parts[0]}.{parts[1]}" if parts[1] else parts[0]
                    elif buffCount == '.':
                        # Just a dot, default to 1
                        buffCount = ''

        if buff:
            print(buff)
            print(ocrText)
            print(f"Filtered buffCount: '{buffCount}'")

        return buffCount if buffCount else '1'
    
    def getBuffQuantityFromImgTight(self, bgrImg, show=False):
        #more aggressive thresholding and masking
        #get only text (rgb [243, 243, 243])
        mask = cv2.inRange(bgrImg, np.array([242, 242, 242]), np.array([245, 245, 245]))
        #dilate to make the text thicker
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        mask = cv2.dilate(mask, kernel)
        img = Image.fromarray(mask)
        img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)
        #convert to black text on white background for ocr
        #img = ImageOps.invert(img)
        if show:
            img.show()
        ocrText = ''.join([x[1][0] for x in ocrRead(img)])
        hasteVal = ''.join([x for x in ocrText if x.isdigit()])
        return hasteVal if hasteVal else '1'

    def getBuffsWithImage(self, buffs, save=False, screen = None, threshold=0.7):
        buffQuantity = []
        buffs = buffs.items()

        if screen is None:
            screen = self.screenshotBuffArea()

        for buff,v in buffs:
            templatePosition, transform, stackable = v

            #find the buff
            buffTemplate = adjustImage("./images/buffs", buff, self.robloxWindow.display_type)
            finalBuffValues = []

            for _ in range(3):
                res = locateTransparentImage(buffTemplate, screen, threshold)

                if not res: 
                    finalBuffValues.append(0)
                    break

                #get a screenshot of the buff
                rx, ry = res[1]
                h,w = buffTemplate.shape[:-1]
                if templatePosition == "bottom": 
                    ry-=self.buffSize-h
                elif templatePosition == "middle":
                    rx = max(0, rx-(self.buffSize-w)/2+8)
                    ry -= 30

                cropX = int(rx)
                cropY = int(ry)

                imgHeight, imgWidth, *_ = screen.shape
                cropX = np.clip(cropX, 0, imgWidth - self.buffSize - 5)
                cropY = np.clip(cropY, 0, imgHeight - self.buffSize - 2)
                
                #buff is not stackable, no need to extract text
                if not stackable:
                    finalBuffValues.append(1)
                    if save:
                        fullBuffImgBGR = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)[cropY:cropY+self.buffSize+2, cropX:cropX+self.buffSize+5]
                        cv2.imwrite(f"{buff}-{time.time()}.png", fullBuffImgBGR)
                    break
                    
                fullBuffImgBGR = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)[cropY:cropY+self.buffSize+2, cropX:cropX+self.buffSize+5]

                if fullBuffImgBGR.size == 0:
                    print(f"Warning: Empty image for buff '{buff}' at ({cropX}, {cropY})")
                    finalBuffValues.append(1)
                    time.sleep(1)
                    continue
                
                if save:
                    cv2.imwrite(f"{buff}-{time.time()}.png", fullBuffImgBGR)

                #filter out everything but the text
                buffVal = self.getBuffQuantityFromImg(fullBuffImgBGR, transform, buff=buff)
                if buffVal == "1":
                    time.sleep(1)
                finalBuffValues.append(buffVal)
            
            maxFinalBuffValue = "0"
            for val in finalBuffValues:
                try:
                    val_float = float(val)
                    max_float = float(maxFinalBuffValue)
                    if val_float > max_float:
                        maxFinalBuffValue = val
                except (ValueError, TypeError) as e:
                    # If we can't convert to float, skip this value or use a default
                    print(f"Warning: Could not convert buff value '{val}' to float: {e}")
                    continue
            buffQuantity.append(maxFinalBuffValue)

        return buffQuantity

    def getBuffWithColor(self, buffs):
        buffQuantity = []
        buffs = buffs.items()

        screen = self.screenshotBuffArea()
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        for buff,v in buffs:
            colorRange, transform, stackable = v
            lower, upper = colorRange

            #find the buff
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                rect = cv2.boundingRect(cnt)
                x, y, w, h = rect

                #filter area to avoid noise
                if self.buffSize-5 < w < self.buffSize+5:
                     #buff is either present or not, non stackable (0 or 1)
                    if not stackable:
                        buffQuantity.append("1")
                        break

                    #crop out
                    y = min(0, y+self.buffSize-h)
                    buffImgBGR = screen[y:y+self.buffSize, x:x+self.buffSize]
                    out = self.getBuffQuantityFromImg(buffImgBGR, True)
                    buffQuantity.append(out)
                    break
                else:
                    buffQuantity.append("0")
        return buffQuantity
    
    def detectBuffColorInImage(self, screen, hex, minSize, x1=0, y1=0, x2=None, y2=None, variation=0, show=False, searchDirection=1, instances=1):
        
        #convert hex to bgr and setup the color range
        r = (hex >> 16) & 0xFF
        g = (hex >> 8) & 0xFF
        b = hex & 0xFF
        bgr = [b,g,r]
        lower = np.array([x-variation for x in bgr])
        upper = np.array([x+variation for x in bgr])

        #crop screen
        if x2 is None:
            x2 = screen.shape[1]
        if y2 is None:
            y2 = screen.shape[0]
        
        cropped = screen[int(y1):int(y2), max(int(x1),0):int(x2)]

        if cropped is None or cropped.size == 0:
            print(f"Image is blank")
            print(f"Image Size: {screen.size}")
            print(f"Crop info: {(x1,y1,x2,y2)}")
            return []

        mask = cv2.inRange(cropped, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coords = []
        for cnt in contours:
            rect = cv2.boundingRect(cnt)
            x, y, w, h = rect

            #filter area to avoid noise
            if w > minSize[0]*self.robloxWindow.multi and h > minSize[1]*self.robloxWindow.multi:
                coords.append((x + x1, y + y1, w, h))  # Offset by crop origin

        def sort_key(rect):
            x, y, w, h = rect
            center_x = x + w // 2
            center_y = y + h // 2

            if searchDirection == 1:  # top → left → right → bottom
                return (center_y, center_x)
            elif searchDirection == 2:  # bottom → left → right → top
                return (-center_y, center_x)
            elif searchDirection == 3:  # bottom → right → left → top
                return (-center_y, -center_x)
            elif searchDirection == 4:  # top → right → left → bottom
                return (center_y, -center_x)
            elif searchDirection == 5:  # left → top → bottom → right
                return (center_x, center_y)
            elif searchDirection == 6:  # left → bottom → top → right
                return (center_x, -center_y)
            elif searchDirection == 7:  # right → bottom → top → left
                return (-center_x, -center_y)
            elif searchDirection == 8:  # right → top → bottom → left
                return (-center_x, center_y)
            else:  # fallback to default (top → left)
                return (center_y, center_x)

        # Sort and return only the first match
        if coords:
            coords.sort(key=sort_key)
            out = []
            preview = screen.copy()
            for i in range(min(len(coords), instances)):
                x, y, w, h = coords[i]
                out.append(coords[i])
                if show:
                    cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if show:
                cv2.imshow("Detected Buff", preview)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            if instances == 1:
                return out[0]
            else:
                return out

        return []

        
    def getNectar(self, nectar):
        vals = self.nectars[nectar]
        col, offsetCoords = vals
        offsetX, offsetY = offsetCoords

        #find the buff
        screen = self.screenshotBuffArea()
        buffTemplate = adjustImage("./images/buffs", nectar, self.robloxWindow.display_type)
        res = locateTransparentImage(buffTemplate, screen, 0.5) #get the best match first. At high nectar levels, it becomes hard to detect the nectar icon
        if not res: 
            return 0
        #get a screenshot of the buff
        rx, ry = res[1]
        screenH, screenW, *_ = screen.shape
        cropX = max(0, int(rx+offsetX*self.robloxWindow.multi))
        cropY = max(0, int(ry+offsetY*self.robloxWindow.multi))
        cropX2 = min(screenW, cropX+40*self.robloxWindow.multi)
        cropY2 = min(screenH, cropY+40*self.robloxWindow.multi)
        fullBuffImg = screen[cropY:cropY2, cropX:cropX2]
        h,w, *_ = fullBuffImg.shape
        #get the buff level
        fullBuffImg = cv2.cvtColor(fullBuffImg, cv2.COLOR_RGBA2BGR)
        mask = cv2.cvtColor(fullBuffImg, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(mask, col[0], col[1])
        #cv2.imshow("mask", mask)
        #cv2.waitKey(0)
        #mask = cv2.erode(mask, self.nectarKernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        if not contours:
            #in this case, the nectar quantity might be so low it cant be detected or the player doesnt have the nectar at all
            #so, we get the confidence value of the match
            #if the value is high, its probably low nectar quantity
            #if its low, the player prob doesnt have the nectar
            max_val, _  = res
            return 2 if max_val > 0.8 else 0
        # return the bounding with the largest area
        _, _, _, buffH = cv2.boundingRect(max(contours, key=cv2.contourArea))
        quantity = max(min(100, (buffH/h*100)), 1)
        return quantity


    def getNectars(self):
        nectarQuantity = []
        for nectar in self.nectars:
            nectarQuantity.append(self.getNectar(nectar))
        return nectarQuantity


class HourlyReport():
    def __init__(self, buffDetector: BuffDetector = None, time_format=24):
        #key: name of buff
        #value: [template for template matching is the buff's top, bottom or middle, if buff image should be transformed, if buff is stackable]
        self.hourBuffs = {
            "tabby_love": ["top", True, True],
            "polar_power": ["top", True, True],
            "wealth_clock": ["top", True, True],
            "blessing": ["middle", True, True],
            "bloat": ["top", True, True],
        }
        self.uptimeBearBuffs = {
            "bearmorph1": ["top", True, False],
            "bearmorph2": ["top", True, False],
            "bearmorph3": ["top", True, False],
            "bearmorph4": ["top", True, False],
            "bearmorph5": ["top", True, False],
            "bearmorph6": ["top", True, False],
        }

        self.uptimeBuffsColors = {
            # "focus": [[np.array([50, 180, 180]), np.array([80, 255, 255])], True, True],
            "baby_love": [0xff8de4f3, (5, 1)],
            "haste": [0xfff0f0f0, (5, 1)],
            "melody": [0xff242424, (3,2)],
            "focus": [0xff22ff06, (5,1)],
            "bomb_combo": [0xff272727, (5,1)],
            "balloon_aura": [0xfffafd38, (5,1)],
            "boost": [0xff90ff8e, (5,1)],
            "blue_boost": [0xff56a4e4, (4,2)],
            "red_boost": [0xffe46156, (4,2)],
            "inspire": [0xfff4ef14, (5,1)]
        }

        self.buffDetector = buffDetector
        self.hourlyReportDrawer = HourlyReportDrawer(time_format)

        #setup stats
        self.hourlyReportStats = {}

    def filterOutliers(self, values, threshold=3):
        nonZeroValues = [x for x in values if x]
        
        # If no non-zero values or insufficient data, return original values
        if len(nonZeroValues) < 2:
            return values
        
        # Calculate the mean and standard deviation
        mean = np.mean(nonZeroValues)
        std_dev = np.std(nonZeroValues)

        #standard deviation is 0, no outliers, prevent division by zero
        if std_dev == 0:
            return values 
        
        # Calculate Z-scores
        z_scores = [(x - mean) / std_dev for x in values]
        
        # Filter out values with Z-scores greater than the threshold
        filtered_values = [x for x, z in zip(values, z_scores) if abs(z) < threshold or not x]
        
        return filtered_values

    def generateHourlyReport(self, setdat):
        buffQuantity = self.buffDetector.getBuffsWithImage(self.hourBuffs)
        nectarQuantity = self.buffDetector.getNectars()
        #mssScreenshot(save=True)

        #get the hourly report data

        planterData = ""
        #get planter data
        if setdat["planters_mode"] == 1:
            with open("./data/user/manualplanters.txt", "r") as f:
                planterData = f.read()
            f.close()

            if planterData:
                planterData = ast.literal_eval(planterData)
        elif setdat["planters_mode"] == 2:
            with open("./data/user/auto_planters.json", "r") as f:
                planterData = json.load(f)["planters"]
            f.close()
            planterData = {
                "planters": [p["planter"] for p in planterData],
                "harvestTimes": [p["harvest_time"] for p in planterData],
                "fields": [p["field"] for p in planterData],
            }
            if all(not p for p in planterData["planters"]):
                planterData = ""


        #get history
        with open("data/user/hourly_report_history.txt", "r") as f:
            historyData = ast.literal_eval(f.read())
        f.close()
        
        if len(self.hourlyReportStats["honey_per_min"]) < 3:
            self.hourlyReportStats["honey_per_min"] = [0]*3 + self.hourlyReportStats["honey_per_min"]
        #filter out the honey/min
        print(self.hourlyReportStats["honey_per_min"])
        #self.hourlyReportStats["honey_per_min"] = [x for x in self.hourlyReportStats["honey_per_min"] if x]
        self.hourlyReportStats["honey_per_min"] = self.filterOutliers(self.hourlyReportStats["honey_per_min"])
        #calculate honey/min
        honeyPerMin = [0]
        prevHoney = self.hourlyReportStats["honey_per_min"][0]
        for x in self.hourlyReportStats["honey_per_min"][1:]:
            if x > prevHoney:
                honeyPerMin.append((x-prevHoney)/60)
            prevHoney = x
        
        #calculate some stats
        if len(set(self.hourlyReportStats["honey_per_min"])) <= 1:
            onlyValidHourlyHoney = self.hourlyReportStats["honey_per_min"].copy()
        else:
            onlyValidHourlyHoney = [x for x in self.hourlyReportStats["honey_per_min"] if x] #removes all zeroes
        sessionHoney = max(0, onlyValidHourlyHoney[-1]- self.hourlyReportStats["start_honey"])
        sessionTime = time.time()-self.hourlyReportStats["start_time"]
        honeyThisHour = max(0, onlyValidHourlyHoney[-1] - onlyValidHourlyHoney[0])

        hourlyReportStats = copy.deepcopy(self.hourlyReportStats)

        canvas = self.hourlyReportDrawer.drawHourlyReport(hourlyReportStats, sessionTime, honeyPerMin, 
                                                          sessionHoney, honeyThisHour, onlyValidHourlyHoney, 
                                                          buffQuantity, nectarQuantity, planterData, 
                                                          self.uptimeBuffsValues, self.buffGatherIntervals)
        w, h = canvas.size
        canvas = canvas.resize((int(w*1.2), int(h*1.2))) 
        canvas.save("hourlyReport.png")

        return hourlyReportStats

    def resetHourlyStats(self):
        self.hourlyReportStats["honey_per_min"] = []
        self.hourlyReportStats["backpack_per_min"] = []
        self.hourlyReportStats["bugs"] = 0
        self.hourlyReportStats["quests_completed"] = 0
        self.hourlyReportStats["vicious_bees"] = 0
        self.hourlyReportStats["gathering_time"] = 0
        self.hourlyReportStats["converting_time"] = 0
        self.hourlyReportStats["bug_run_time"] = 0
        self.hourlyReportStats["misc_time"] = 0

        self.uptimeBuffsValues = {k:[0]*600 for k in self.uptimeBuffsColors.keys()} #*600
        for k in ["bear", "white_boost"]:
            self.uptimeBuffsValues[k] = [0]*600
        
        self.buffGatherIntervals = [0]*600

        self.saveHourlyReportData()
    
    def resetAllStats(self):
        self.hourlyReportStats["start_time"] = 0
        self.hourlyReportStats["start_honey"] = 0
        self.resetHourlyStats()
    
    def addHourlyStat(self, stat, value):
        if isinstance(self.hourlyReportStats[stat], list):
            self.hourlyReportStats[stat].append(value)
        else:
            self.hourlyReportStats[stat] += value
        self.saveHourlyReportData()
    
    def setSessionStats(self, start_honey, start_time):
        self.hourlyReportStats["start_honey"] = start_honey
        self.hourlyReportStats["start_time"] = start_time
        self.saveHourlyReportData()
    
    def saveHourlyReportData(self):
        with open("data/user/hourly_report_stats.pkl", "wb") as f:
            pickle.dump({
                "hourlyReportStats": self.hourlyReportStats,
                "uptimeBuffsValues": self.uptimeBuffsValues,
                "buffGatherIntervals": self.buffGatherIntervals,
            }, f)
    
    def loadHourlyReportData(self):
        with open("data/user/hourly_report_stats.pkl", "rb") as f:
            data = pickle.load(f)
            self.hourlyReportStats = data["hourlyReportStats"]
            self.uptimeBuffsValues = data["uptimeBuffsValues"]
            self.buffGatherIntervals = data["buffGatherIntervals"]


class HourlyReportDrawer:
    def __init__(self, time_format=24):
        self.backgroundColor = "#0E0F13"
        self.canvasSize = (6400, 8000)
        self.sidebarWidth = 1900
        self.leftPadding = 150
        self.availableSpace = self.canvasSize[0] - self.sidebarWidth - self.leftPadding*2
        self.bodyColor = "#FFFFFF"
        self.time_format = time_format
        self.hour = datetime.now().hour
        self.sideBarBackground = (23, 25, 29)
        if self.hour == 0:
            self.hour = 23
        else:
            self.hour -= 1
        self.assetPath = "hourly_report/assets"

    def transformXLabelTime(self, i, val):
        if i%10:
            return
        hour = self.hour
        if val == 60:
            hour += 1
            if hour == 24:
                hour = 0
            val = 0

        time_str = f"{str(hour).zfill(2)}:{str(val).zfill(2)}"
        if self.time_format == 12:
            # Convert to 12-hour format
            hour_12 = hour % 12
            if hour_12 == 0:
                hour_12 = 12
            am_pm = "AM" if hour < 12 else "PM"
            time_str = f"{str(hour_12).zfill(2)}:{str(val).zfill(2)} {am_pm}"

        return time_str

    def millify(self, n):
        if not n: return "0"
        millnames = ['',' K',' M',' B',' T', 'Qd']
        n = float(n)
        millidx = max(0,min(len(millnames)-1,
                            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

        return '{:.2f} {}'.format(n / 10**(3 * millidx), millnames[millidx])

    def displayTime(self, seconds, units = ['w','d','h','m','s']):
        intervals = (
            ('w', 604800),  # 60 * 60 * 24 * 7
            ('d', 86400),    # 60 * 60 * 24
            ('h', 3600),    # 60 * 60
            ('m', 60),
            ('s', 1),
        )
        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                if name in units:
                    value = int(value)
                    if value < 10:
                        value = "0"+str(value)
                    result.append("{}{}".format(value, name))
        if not result:
            return "0s"
        return ' '.join(result)
        
    def getFont(self, weight, fontSize):
        return ImageFont.truetype(f"hourly_report/Inter/static/Inter_18pt-{weight.title()}.ttf", fontSize)

    def getGradientColorAtRatio(self, ratio, gradientSpec):
        #calculates the RGBA color from gradientSpec at a given vertical ratio (0=bottom, 1=top)
        if not gradientSpec:
            return (0, 0, 0, 0) # Default transparent black if no spec

        sorted_stops = sorted(gradientSpec.items()) # list of (position_ratio, color_tuple)

        # Clamp ratio
        ratio = max(0.0, min(1.0, ratio))

        # Find which two stops this ratio is between
        for j in range(len(sorted_stops) - 1):
            pos1, col1 = sorted_stops[j]
            pos2, col2 = sorted_stops[j + 1]
            if pos1 <= ratio <= pos2:
                if pos2 - pos1 == 0:
                    local_ratio = 0
                else:
                    local_ratio = (ratio - pos1) / (pos2 - pos1)

                #interpolate RGBA values
                try:
                    r = int(col1[0] + (col2[0] - col1[0]) * local_ratio)
                    g = int(col1[1] + (col2[1] - col1[1]) * local_ratio)
                    b = int(col1[2] + (col2[2] - col1[2]) * local_ratio)
                    #handle alpha
                    a = 255 
                    if len(col1) > 3 and len(col2) > 3:
                            a = int(col1[3] + (col2[3] - col1[3]) * local_ratio)
                    elif len(col1) > 3:
                        a = col1[3]
                    elif len(col2) > 3:
                        a = col2[3]

                    return (r, g, b, a)
                except IndexError:
                    print(f"Warning: Color tuple length mismatch in gradientSpec between {col1} and {col2}")
                    return (0,0,0,255)

        # If ratio is below the first stop or above the last stop (should not happen with clamping)
        if ratio < sorted_stops[0][0]:
            return sorted_stops[0][1] # Return first color
        else:
            return sorted_stops[-1][1] # Return last color


    def drawGraph(self, graphX, graphY, width, height, xData, datasets, maxY = None, showXAxisLabels=True, showYAxisLabels=True, ticks=5, yLabelFunc=None, xLabelFunc=None):
        # Validate data lengths
        for dataset in datasets:
            data = dataset["data"]
            #pad the data
            data = [0]*(len(xData) - len(data)) + data
        
            # Prevent division by zero with minimal data
            xInterval = width / max(len(data) - 1, 1)
            if not maxY:
                maxY = max(data) if data else 1
                if not maxY:
                    maxY = 1
            else:
                data = [maxY if y > maxY else y for y in data]

            font = self.getFont("semibold", 60)
            fontColor = (175, 175, 175)
            gridColor = (65, 65, 65)
            #draw xaxis
            if showXAxisLabels:
                for i, val in enumerate(xData):
                    val = xLabelFunc(i, val) if xLabelFunc else val
                    if val:
                        val = str(val)
                        #get the text width, so the text can be centered with the x axis point
                        bbox = self.draw.textbbox((0, 0), val, font=font)
                        textWidth = bbox[2] - bbox[0]
                        self.draw.text((graphX+xInterval*i - textWidth/2, graphY+20), val, font=font, fill= fontColor)
            
            #draw y labels and y grid
            #calculating ticks
            yInterval = height/max(ticks-1, 1)
            yValInterval = maxY/max(ticks-1, 1)

            for i in range(ticks):
                y = graphY - yInterval*i
                if showYAxisLabels:
                    text = yValInterval*i
                    text = yLabelFunc(i, text) if yLabelFunc else text
                    if text:
                        text = str(text)
                        bbox = self.draw.textbbox((0, 0), text, font=font)
                        textWidth = bbox[2] - bbox[0]
                        textHeight = bbox[3] - bbox[1]
                        self.draw.text((graphX - textWidth - 100, y - textHeight/2), text, font=font, fill= fontColor)
                self.draw.line((graphX-30, y, graphX+30+width, y), fill=gridColor, width=3)


            # Collect curve points
            points = []
            for i, val in enumerate(data):
                px = graphX + i * xInterval
                py = graphY - (val / maxY * height)
                points.append((px, py))
            # Close polygon at bottom
            points.append((graphX + (len(xData) - 1) * xInterval, graphY))
            points.append((graphX, graphY))

            #make gradient
            gradientSpec = dataset.get("gradientFill", None)
            if gradientSpec:
                gradient = Image.new('RGBA', (int(width), int(height)), (0, 0, 0, 0))
                grad_draw = ImageDraw.Draw(gradient)
                sorted_stops = sorted(gradientSpec.items())  # list of (position, color)
                stop_positions = [int(pos * height) for pos, _ in sorted_stops]

                for i in range(height):
                    # Normalize position (0 to 1)
                    ratio = i / float(max(height - 1, 1))

                    # Find which two stops this ratio is between
                    for j in range(len(sorted_stops) - 1):
                        pos1, col1 = sorted_stops[j]
                        pos2, col2 = sorted_stops[j + 1]
                        if pos1 <= ratio <= pos2:
                            local_ratio = (ratio - pos1) / (pos2 - pos1)
                            r = int(col1[0] + (col2[0] - col1[0]) * local_ratio)
                            g = int(col1[1] + (col2[1] - col1[1]) * local_ratio)
                            b = int(col1[2] + (col2[2] - col1[2]) * local_ratio)
                            a = int(col1[3] + (col2[3] - col1[3]) * local_ratio)
                            grad_draw.line([(0, height - i), (width, height - i)], fill=(r, g, b, a))
                            break
                

            #composite gradient on dark background
            bg = Image.new('RGBA', (int(width), int(height)), self.backgroundColor)
            gradient = Image.alpha_composite(bg, gradient)

            #create a mask with polygon in the shape of the graph
            mask = Image.new('L', (int(width), int(height)), 0)
            mask_draw = ImageDraw.Draw(mask)
            rel_pts = [(px - graphX, py - (graphY - height)) for px, py in points]
            mask_draw.polygon(rel_pts, fill=255)

            #paste the gradient and mask onto the canvas
            self.canvas.paste(gradient, (graphX, graphY - height), mask)

            lineColor = dataset["lineColor"]
            #gradient color.
            if gradientSpec and lineColor == "gradient":
                #draw the line
                for i in range(len(points) - 3):
                    #Since line doesnt accept gradients, we will break the line down into segments, 
                    #and assign each segment a color
                    x0, y0 = points[i]
                    x1, y1 = points[i+1]

                    #calculate length of the line
                    dx = x1 - x0
                    dy = y1 - y0
                    length = math.sqrt(dx*dx + dy*dy)

                    if length == 0: continue # Skip zero-length segments

                    #get the number of segments
                    segmentCount = max(1, int(length / 10))

                    for k in range(segmentCount):
                        t0 = k / segmentCount
                        t1 = (k + 1) / segmentCount

                        sub_x0 = x0 + dx * t0
                        sub_y0 = y0 + dy * t0
                        sub_x1 = x0 + dx * t1
                        sub_y1 = y0 + dy * t1
                        mid_y = (sub_y0 + sub_y1) / 2.0
                        # Convert Y coord to ratio (0=bottom, 1=top)
                        mid_yRatio = (graphY - mid_y) / height if height > 0 else 0.0

                        # Get color for this ratio
                        r, g, b, a = self.getGradientColorAtRatio(mid_yRatio, gradientSpec)

                        self.draw.line(
                            (int(sub_x0), int(sub_y0), int(sub_x1), int(sub_y1)),
                            fill=(r, g, b), # Use opaque RGB for line
                            width=7
                        )

            else:
                # Draw the entire line with a solid color
                # Use points[:len(data)] to only draw line over actual data points, not polygon closing points
                self.draw.line(points[:len(data)], fill=lineColor, width=7)

    def drawDoughnutChart(self, x, y, size, datasets, holeRatio = 0.6):

        total = sum([x["data"] for x in datasets])
        if not total:
            total = 1
        angleStart = -90
        chartArea = (x, y, x+size, y+size)

        #draw the section
        for dataset in datasets:
            angleEnd = angleStart + (dataset["data"] / total) * 360
            self.draw.pieslice(chartArea, angleStart, angleEnd, fill=dataset["color"])
            angleStart = angleEnd

        #draw the hole
        if holeRatio > 0:
            hole_size = int(size * holeRatio)
            offset = (size - hole_size) // 2
            hole_bbox = (x+offset, y+offset, x+offset + hole_size, y+offset + hole_size)
            self.draw.ellipse(hole_bbox, fill=self.sideBarBackground)

    def drawProgressChart(self, x, y, size, percentage, color, holeRatio = 0.6,):
        chartArea = (x, y, x+size, y+size)

        #draw the section
        self.draw.pieslice(chartArea, -90, 360, fill=(*color, 140))
        self.draw.pieslice(chartArea, -90, (int(percentage) / 100) * 360 - 90, fill=color)

        #draw the hole
        if holeRatio > 0:
            hole_size = int(size * holeRatio)
            offset = (size - hole_size) // 2
            hole_bbox = (x+offset, y+offset, x+offset + hole_size, y+offset + hole_size)
            self.draw.ellipse(hole_bbox, fill=self.sideBarBackground)

        font = self.getFont("semibold", 65)
        text = f"{int(percentage)}%"
        text_bbox = self.draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        self.draw.text((x + (size - text_width) // 2, y + (size - text_height) // 2 - 10), text, fill=self.bodyColor, font=font)

    def drawStatCard(self, x, y, statImage, statValue, statTitle, fontColor = None, imageColor = None):
        leftPadding = x+100
        self.draw.rounded_rectangle((x,y, x+700, y+750), fill=(int(23*1.2), int(25*1.2), int(29*1.2)), radius=60)
        #load the image 
        img = Image.open(f"{self.assetPath}/{statImage}.png").convert("RGBA")
        width, height = img.size
        imageHeight = 200
        imageWidth = int(width*(imageHeight/height))
        img = img.resize((imageWidth, imageHeight))
        
        #recolor the image
        if imageColor:
            r,g,b = imageColor
            pixels = img.load()
            for i in range(img.width):
                for j in range(img.height):
                    _, _, _, a = pixels[i, j]
                    if a > 0:  #only recolor non-transparent pixels
                        pixels[i, j] = (r,g,b, a)

        self.canvas.paste(img, (leftPadding, y + 100), img)

        self.draw.text((leftPadding, y+380), str(statValue), font=self.getFont("semibold", 80), fill=fontColor if fontColor else self.bodyColor)
        self.draw.text((leftPadding, y+550), statTitle, font=self.getFont("medium", 55), fill=self.bodyColor)

    def drawBuffUptimeGraphStackableBuff(self, y, datasets, imageName, ):
        #draw the graph
        graphHeight = 450
        graphXStart = self.leftPadding+450
        xData = list(range(601))
        self.drawGraph(graphXStart, y, self.availableSpace-570, graphHeight, xData, datasets, maxY=10, showXAxisLabels=False, showYAxisLabels=False, ticks=3)

        #load the icon
        imageDimension = 170
        imageX = graphXStart - 200 - imageDimension
        imageY = y - graphHeight//2 - imageDimension//2 + len(datasets)*10
        img = Image.open(f"{self.assetPath}/{imageName}.png").convert("RGBA")
        img = img.resize((imageDimension, imageDimension))
        self.canvas.paste(img, (imageX, imageY), img)

        self.draw.text((imageX, imageY + imageDimension), "x0-10", font=self.getFont("semibold", 65), fill=self.bodyColor)

        for i, dataset in enumerate(datasets):
            self.draw.text((imageX, imageY - (90+60*i)), dataset["average"], font=self.getFont("semibold", 60), fill=dataset["lineColor"])

    def drawBuffUptimeGraphUnstackableBuff(self, y, datasets, imageName, renderTime = False):

        def transformXLabel(i, val):
            if i%100:
                return
            val //= 10
            hour = self.hour
            if val == 60:
                hour += 1
                if hour == 24:
                    hour = 0
                val = 0
            return f"{str(hour).zfill(2)}:{str(val).zfill(2)}"

        #draw the graph
        graphHeight = 250
        graphXStart = self.leftPadding+450
        xData = list(range(601))
        self.drawGraph(graphXStart, y, self.availableSpace-570, graphHeight, xData, datasets, maxY=1, showXAxisLabels=renderTime, showYAxisLabels=False, ticks=2, xLabelFunc=transformXLabel)

        #load the icon
        imageDimension = 170
        imageX = graphXStart - 200 - imageDimension
        imageY = y - graphHeight//2 - imageDimension//2 + len(datasets)*10
        img = Image.open(f"{self.assetPath}/{imageName}.png").convert("RGBA")
        img = img.resize((imageDimension, imageDimension))
        self.canvas.paste(img, (imageX, imageY), img)

    def drawSessionStat(self, y, imageName, label, value, valueColor):
        imgContainerDimension = 180
        self.draw.rounded_rectangle((self.sidebarX, y, self.sidebarX+imgContainerDimension, y+imgContainerDimension), radius=50, fill=(int(45*1.1), int(46*1.1), int(53*1.1)))
        img = Image.open(f"{self.assetPath}/{imageName}.png").convert("RGBA")
        width, height = img.size
        imageWidth = 120
        imageHeight = int(height*(imageWidth/width))
        img = img.resize((imageWidth, imageHeight))
        #center the image in the container
        self.canvas.paste(img, (self.sidebarX + (imgContainerDimension-imageWidth)//2 , y + (imgContainerDimension-imageHeight)//2), img)

        #draw label and value
        #make sure they are vertically centered with the image container
        font = self.getFont("semibold", 68)
        ascent, _ = font.getmetrics()
        textY = y + (imgContainerDimension - ascent)//2
        self.draw.text((self.sidebarX+imgContainerDimension+50, textY), label, self.bodyColor, font=font)
        #value is right-aligned
        bbox = self.draw.textbbox((0, 0), value, font=font)
        textWidth = bbox[2] - bbox[0]
        self.draw.text((self.canvasSize[0]-self.sidebarPadding-textWidth, textY), str(value), valueColor, font=font)

    def drawTaskTimes(self, y, datasets):
        legendIconDimension = 80
        font = self.getFont("medium", 68)
        x = self.sidebarX
        totalData = sum([x["data"] for x in datasets])
        if not totalData:
            totalData = 1

        for dataset in datasets:
            self.draw.rounded_rectangle((x, y, x+legendIconDimension, y+legendIconDimension), fill=dataset["color"], radius=10)
            bbox = self.draw.textbbox((0, 0), dataset["label"], font=font)
            textHeight = bbox[3] - bbox[1]
            textY = y #+ (legendIconDimension - textHeight) // 2 -25
            self.draw.text((x+legendIconDimension + 50, textY), f"{dataset['label']}:", self.bodyColor, font=font)
            self.draw.text((x+legendIconDimension + 600, textY), self.displayTime(dataset["data"]), self.bodyColor, font=font)
            self.draw.text((x+legendIconDimension + 1000, textY), f"{round(dataset['data']/totalData*100, 1)}%", (220,220,220), font=font)
            y+= 150

        y += 100
        doughnutChartSize = 600
        self.drawDoughnutChart(self.sidebarX + 450, y, doughnutChartSize, datasets, holeRatio=0.4)

    def drawPlanters(self, y, planterNames, planterTimes, planterFields):
        fieldNectarIcons = {
            "sunflower": "satisfying",
            "dandelion": "comforting",
            "mushroom": "motivating",
            "blue flower": "refreshing",
            "clover": "invigorating",
            "strawberry": "refreshing",
            "spider": "motivating",
            "bamboo": "comforting",
            "pineapple": "satisfying",
            "stump": "motivating",
            "cactus": "invigorating",
            "pumpkin": "satisfying",
            "pine tree": "comforting",
            "rose": "motivating",
            "mountain top": "invigorating",
            "pepper": "invigorating",
            "coconut": "refreshing"
        }

        planterX = self.sidebarX
        fieldFont = self.getFont("semibold", 68)
        timeFont = self.getFont("semibold", 55)
        for i in range(len(planterNames)):
            if not planterNames[i]:
                continue
            bbox = self.draw.textbbox((0, 0), planterFields[i].title(), font=fieldFont)
            fieldTextWidth = bbox[2] - bbox[0]

            nectarImg = Image.open(f'{self.assetPath}/{fieldNectarIcons[planterFields[i]]}.png')
            width, height = nectarImg.size
            nectarImageHeight = bbox[3] - bbox[1]
            nectarImageWidth = int(width*(nectarImageHeight/height))
            nectarImg = nectarImg.resize((nectarImageWidth, nectarImageHeight))

            fieldAndNectarWidth = fieldTextWidth + nectarImageWidth + 30

            img = Image.open(f'{self.assetPath}/{planterNames[i].replace(" ","_")}_planter.png')
            width, height = img.size
            imageHeight = 250
            imageWidth = int(width*(imageHeight/height))
            img = img.resize((imageWidth, imageHeight))

            timeText = self.displayTime(planterTimes[i], ["h", "m"]) if planterTimes[i] > 0 else "Ready!"
            bbox = self.draw.textbbox((0, 0), timeText, font=timeFont)
            timeTextWidth = bbox[2] - bbox[0]

            maxWidth = max(fieldAndNectarWidth, imageWidth, timeTextWidth)
            self.canvas.paste(img, (planterX + (maxWidth-imageWidth)//2, y), img)
            self.draw.text((planterX + (maxWidth - fieldAndNectarWidth)//2, y+300), planterFields[i].title(), font=fieldFont, fill= self.bodyColor) 
            self.canvas.paste(nectarImg, (planterX + (maxWidth - fieldAndNectarWidth)//2 + fieldTextWidth + 30, y+315), nectarImg)
            self.draw.text((planterX + (maxWidth - timeTextWidth)//2, y+400), timeText, font=timeFont, fill= tuple([205]*3)) 

            planterX += maxWidth + 200

    def drawBuffs(self, y, buffData):
        buffImages = ["tabby_love_buff", "polar_power_buff", "wealth_clock_buff", "blessing_buff", "bloat_buff"]

        font = self.getFont("bold", 68)
        for i in range(len(buffData)):
            buff = str(buffData[i]) #I cant make up my mind on if buffData should switch to ints or remain as string
            x = self.sidebarX + 340*i

            img = Image.open(f"{self.assetPath}/{buffImages[i]}.png").convert("RGBA")
            width, height = img.size
            imageWidth = 250
            imageHeight= int(width*(imageWidth/height))
            img = img.resize((imageWidth, imageHeight))

            if buff == "0":
                #dim the image
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 100))
            else:
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 20))
            img = Image.alpha_composite(img, overlay)
            self.canvas.paste(img, (x, y), img)

            if buff != "0":
                buffText = f"x{buff}"
                bbox = self.draw.textbbox((0, 0), buffText, font=font, stroke_width=4)
                textWidth = bbox[2] - bbox[0]
                textHeight = 68
                self.draw.text((x + imageWidth - textWidth - 5, y + imageHeight - textHeight - 20), buffText, fill=self.bodyColor, font=font, stroke_width=4, stroke_fill=(0,0,0))

    def drawNectars(self, y, nectarData):
        nectarColors = [(165, 207, 234), (235, 120, 108), (194, 166, 236), (162, 239, 163), (239, 205, 224)]
        nectarNames = ["comforting", "invigorating", "motivating", "refreshing", "satisfying"]
        progressChartSize = 300
        imageHeight = 120
        for i in range(len(nectarData)):
            x = self.sidebarX + i*(progressChartSize+50)
            self.drawProgressChart(x, y, progressChartSize, nectarData[i], nectarColors[i], 0.75)

            img = Image.open(f"{self.assetPath}/{nectarNames[i]}.png").convert("RGBA")
            width, height = img.size
            imageWidth = int(width*(imageHeight/height))
            img = img.resize((imageWidth, imageHeight))
            self.canvas.paste(img, (x + (progressChartSize-imageWidth)//2, y+progressChartSize + 80), img)

    def drawHourlyReport(self, hourlyReportStats, sessionTime, honeyPerMin, sessionHoney, honeyThisHour, onlyValidHourlyHoney, buffQuantity, nectarQuantity, planterData, uptimeBuffsValues, buffGatherIntervals):

        def getAverageBuff(buffValues):
            #get the buff average when gathering, rounded to 2p
            count = 0
            total = 0
            for i, e in enumerate(buffGatherIntervals):
                if e:
                    total += buffValues[i]
                    count += 1

            res = total/count if count else 0
                
            return f"x{res:.2f}"

        self.canvas = Image.new('RGBA', self.canvasSize, self.backgroundColor)
        self.draw = ImageDraw.Draw(self.canvas)

        mins = list(range(61))

        #draw aside bar
        self.draw.rectangle((self.canvasSize[0]-self.sidebarWidth, 0, self.canvasSize[0], self.canvasSize[1]), fill=self.sideBarBackground)

        #draw icon
        macroIcon = Image.open(f"{self.assetPath}/macro_icon.png")
        # macroIcon = macroIcon.resize((170, 170))
        self.canvas.paste(macroIcon, (5550, 100), macroIcon)
        self.draw.text((5750, 120), "Existance Macro", fill=self.bodyColor, font=self.getFont("semibold", 70))

        #draw title
        self.draw.text((self.leftPadding, 80), "Hourly Report", fill=self.bodyColor, font=self.getFont("bold", 120))
        self.draw.text((self.leftPadding, 260), "Your stats for this hour", fill=self.bodyColor, font=self.getFont("medium", 60))

        #section 1: hourly stats
        y = 470
        statSpacing = (self.availableSpace+self.leftPadding)//5
        avgHoneyPerHour = max(0, sessionHoney/(sessionTime/3600)) if sessionTime > 0 else 0
        self.drawStatCard(self.leftPadding, y, "average_icon", self.millify(avgHoneyPerHour), "Average Honey\nPer Hour")
        self.drawStatCard(self.leftPadding+statSpacing*1, y, "honey_icon", self.millify(honeyThisHour), "Honey Made\nThis Hour", (248,191,23))
        self.drawStatCard(self.leftPadding+statSpacing*2, y, "kill_icon", hourlyReportStats["bugs"], "Bugs Killed\nThis Hour", (254,101,99), (254,101,99))
        self.drawStatCard(self.leftPadding+statSpacing*3, y, "quest_icon", hourlyReportStats["quests_completed"], "Quests Completed\nThis Hour", (103,253,153), (103,253,153))
        self.drawStatCard(self.leftPadding+statSpacing*4, y, "vicious_bee_icon", hourlyReportStats["vicious_bees"], "Vicious Bees\nThis Hour", (132,233,254), (132,233,254))

        #section 2: honey/min
        y += 900
        self.draw.text((self.leftPadding, y), "Honey/Sec", fill=self.bodyColor, font=self.getFont("semibold", 85))
        y += 950
        dataset = [{
            "data": honeyPerMin,
            "lineColor": (174, 22, 250),
            "gradientFill": {
                0: (174,22,250,38),
                1: (174,22,250,153)
            }
        }]
        self.drawGraph(self.leftPadding+450, y, self.availableSpace-570, 700, mins, dataset, xLabelFunc= self.transformXLabelTime, yLabelFunc=lambda i,x : self.millify(x))

        #section 3: backpack
        y += 200
        self.draw.text((self.leftPadding, y), "Backpack", fill=self.bodyColor, font=self.getFont("semibold", 85))
        y += 950
        dataset = [{
            "data": hourlyReportStats["backpack_per_min"],
            "lineColor": "gradient",
            "gradientFill": {
                0: (65, 255, 128, 90),
                0.6: (201, 163, 36, 90),
                0.9: (255, 65, 84, 90),
                1: (255, 65, 84, 90),
            }
        }]
        self.drawGraph(self.leftPadding+450, y, self.availableSpace-570, 700, mins, dataset, maxY=100, xLabelFunc= self.transformXLabelTime, yLabelFunc=lambda i,x: f"{int(x)}%")

        #section 4: buff uptime
        y += 200
        self.draw.text((self.leftPadding, y), "Buff Uptime", fill=self.bodyColor, font=self.getFont("semibold", 85))
        y += 750
        dataset = [
        {
            "data": uptimeBuffsValues["blue_boost"],
            "lineColor": (77,147,193),
            "average": getAverageBuff(uptimeBuffsValues["blue_boost"]),
            "gradientFill": {
                0: (77,147,193,10),
                1: (77,147,193,120),
            }
        },
        {
            "data": uptimeBuffsValues["red_boost"],
            "lineColor": (200,90,80),
            "average": getAverageBuff(uptimeBuffsValues["red_boost"]),
            "gradientFill": {
                0: (200,90,80,10),
                1: (200,90,80,120),
            }
        },
        {
            "data": uptimeBuffsValues["white_boost"],
            "lineColor": (220,220,220),
            "average": getAverageBuff(uptimeBuffsValues["white_boost"]),
            "gradientFill": {
                0: (220,220,220,10),
                1: (220,220,220,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "boost_buff")

        y += 460
        dataset = [
        {
            "data": uptimeBuffsValues["haste"],
            "lineColor": (210,210,210),
            "average": getAverageBuff(uptimeBuffsValues["haste"]),
            "gradientFill": {
                0: (210,210,210,10),
                1: (210,210,210,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "haste_buff")

        y += 460
        dataset = [
        {
            "data": uptimeBuffsValues["focus"],
            "lineColor": (30,191,5),
            "average": getAverageBuff(uptimeBuffsValues["focus"]),
            "gradientFill": {
                0: (30,191,5,10),
                1: (30,191,5,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "focus_buff")

        y += 460
        dataset = [
        {
            "data": uptimeBuffsValues["bomb_combo"],
            "lineColor": (160,160,160),
            "average": getAverageBuff(uptimeBuffsValues["bomb_combo"]),
            "gradientFill": {
                0: (160,160,160,10),
                1: (160,160,160,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "bomb_combo_buff")

        y += 460
        dataset = [
        {
            "data": uptimeBuffsValues["balloon_aura"],
            "lineColor": (50,80,200),
            "average": getAverageBuff(uptimeBuffsValues["balloon_aura"]),
            "gradientFill": {
                0: (50,80,200,10),
                1: (50,80,200,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "balloon_aura_buff")

        y += 460
        dataset = [
        {
            "data": uptimeBuffsValues["inspire"],
            "lineColor": (195,191,18),
            "average": getAverageBuff(uptimeBuffsValues["inspire"]),
            "gradientFill": {
                0: (195,191,18,10),
                1: (195,191,18,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "inspire_buff")

        y += 260
        dataset = [
        {
            "data": uptimeBuffsValues["melody"],
            "lineColor": (200,200,200),
            "gradientFill": {
                0: (200,200,200,255),
                1: (200,200,200,255),
            }
        }
        ]
        self.drawBuffUptimeGraphUnstackableBuff(y, dataset, "melody_buff")

        y += 260
        dataset = [
        {
            "data": uptimeBuffsValues["bear"],
            "lineColor": (115,71,40),
            "gradientFill": {
                0: (115,71,40,255),
                1: (115,71,40,255),
            }
        }
        ]
        self.drawBuffUptimeGraphUnstackableBuff(y, dataset, "bear_buff")

        y += 260
        dataset = [
        {
            "data": uptimeBuffsValues["baby_love"],
            "lineColor": (112,181,195),
            "gradientFill": {
                0: (112,181,195,255),
                1: (112,181,195,255),
            }
        }
        ]
        self.drawBuffUptimeGraphUnstackableBuff(y, dataset, "baby_love_buff", renderTime=True)

        #side bar 

        #session stats

        y2 = 470
        self.sidebarPadding = 110
        self.sidebarX = self.canvasSize[0] - self.sidebarWidth + self.sidebarPadding
        self.draw.text((self.sidebarX, y2), "Session", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawSessionStat(y2, "time_icon", "Session Time", self.displayTime(sessionTime, ['d','h','m']), self.bodyColor)
        y2 += 300
        self.drawSessionStat(y2, "honey_icon", "Current Honey", self.millify(onlyValidHourlyHoney[-1]), "#F8BF17")
        y2 += 300
        self.drawSessionStat(y2, "session_honey_icon", "Session Honey", self.millify(sessionHoney), "#FDE395")

        #task times
        y2 += 500
        self.draw.text((self.sidebarX, y2), "Task Times", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawTaskTimes(y2, [
            {
                "label": "Gathering",
                "data": hourlyReportStats["gathering_time"],
                "color": "#6A0DAD"
            },
            {
                "label": "Converting",
                "data": hourlyReportStats["converting_time"],
                "color": "#9966FF"
            },
            {
                "label": "Bug Run",
                "data": hourlyReportStats["bug_run_time"],
                "color": "#C3A6FF"
            },
            {
                "label": "Other",
                "data": hourlyReportStats["misc_time"],
                "color": "#E6D6FF"
            },
            

        ])

        #planters
        y2 += 1500
        #check if there are planters
        planterNames = [] #planterData["planters"]
        planterTimes = [] #[x-time.time() for x in planterData["harvestTimes"]]
        planterFields = [] #planterData["fields"]
        if planterData:
            for i in range(len(planterData["planters"])):
                if planterData["planters"][i]:
                    planterNames.append(planterData["planters"][i])
                    planterTimes.append(planterData["harvestTimes"][i] - time.time())
                    planterFields.append(planterData["fields"][i])
        if planterNames:
            self.draw.text((self.sidebarX, y2), "Planters", font=self.getFont("semibold", 85), fill=self.bodyColor)
            y2 += 250
            self.drawPlanters(y2, planterNames, planterTimes, planterFields)
            y2 += 650
        
        #buffs
        self.draw.text((self.sidebarX, y2), "Buffs", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawBuffs(y2, buffQuantity)

        #nectars
        y2 += 500
        self.draw.text((self.sidebarX, y2), "Nectars", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawNectars(y2, nectarQuantity)

        return self.canvas
