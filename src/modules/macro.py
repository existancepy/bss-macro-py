import modules.screen.ocr as ocr
import modules.misc.appManager as appManager
import modules.misc.settingsManager as settingsManager
import time
import pyautogui as pag

# We'll use a wrapper for time.sleep that respects pause state
# This will be initialized when the macro class is created
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP, benchmarkMSS, mssScreenshotPillowRGBA
from modules.controls.keyboard import keyboard
from modules.controls.sleep import sleep, set_run_state, pauseable_sleep, wait_while_paused, is_paused
import modules.controls.mouse as mouse
from modules.screen.screenData import getScreenData
import modules.logging.log as logModule
from modules.submacros.fieldDriftCompensation import fieldDriftCompensation as fieldDriftCompensationClass
from modules.screen.robloxWindow import RobloxWindowBounds
from operator import itemgetter
import sys
import platform
import os
import numpy as np
import threading
from modules.submacros.backpack import bpc
from modules.screen.imageSearch import *
import webbrowser
from pynput.keyboard import Key, Controller
import cv2
from datetime import timedelta, datetime
from modules.misc.imageManipulation import *
from PIL import Image
from modules.misc import messageBox
from modules.submacros.memoryMatch import MemoryMatch
import math
import re
import ast
from modules.submacros.hourlyReport import HourlyReport, BuffDetector
from difflib import SequenceMatcher
import fuzzywuzzy.process
import fuzzywuzzy
import traceback
import pygetwindow as gw
from modules.submacros.hasteCompensation import HasteCompensationRevamped
from modules import bitmap_matcher
import json

pynputKeyboard = Controller()
#data for collectable objectives
#[besideE text, movement key, max cooldowns]
collectData = { 
    "wealth_clock": [["use"], "w", 1*60*60], #1hr
    "blueberry_dispenser": [["use", "dispenser"], "a", 4*60*60], #4hr
    "strawberry_dispenser": [["use", "dispenser"], None, 4*60*60], #4hr
    "coconut_dispenser": [["use", "dispenser"], "s", 4*60*60], #4hr
    "royal_jelly_dispenser": [["claim", "royal"], "a",22*60*60], #22hr
    "treat_dispenser": [["use", "treat"], "w", 1*60*60], #1hr
    "ant_pass_dispenser": [["use", "free"], "w", 2*60*60], #2hr
    "glue_dispenser": [["use", "glue"], None, 22*60*60], #22hr
    "stockings": [["check", "inside", "stocking"], "a", 1*60*60], #1hr
    "wreath": [["admire", "honey"], "a", 30*60], #30mins
    "feast": [["dig", "beesmas"], "s", 1.5*60*60], #1.5hr
    "samovar": [["heat", "samovar", "strange"], "w", 6*60*60], #6hr
    "snow_machine": [["activ", "machine"], None, 2*60*60], #2hr
    "lid_art": [["gander", "onett", "art"], "s", 8*60*60], #8hr
    "candles": [["admire", "candle", "honey"], "w", 4*60*60], #4hr
    "memory_match": [["spend", "play"], "a", 2*60*60], #2hr
    "mega_memory_match": [["spend", "play"], "w", 4*60*60], #4hr
    #"night_memory_match": [["spend", "play"], "w", 8*60*60], #8hr
    "extreme_memory_match": [["spend", "play"], "w", 8*60*60], #8hr
    "winter_memory_match": [["spend", "play"], "a", 4*60*60], #4hr
    "honeystorm": [["sum", "honey", "mmon", "storm"], "s", 4*60*60], #4hr
}

#these collects are added seperately as they need to be handled seperately instead of being iterated through by the main loop
fieldBoosterData = {
    "blue_booster": [["use", "booster"], "w", 45*60], #45mins
    "red_booster": [["use", "booster"], "s", 45*60], #45mins
    "mountain_booster": [["use", "booster"], None, 45*60], #45mins
}

mergedCollectData = {**collectData, **fieldBoosterData}
mergedCollectData["sticker_stack"] = [["add", "sticker"], None, 0]

#werewolf is a unique one. There is only one, but it can be triggered from pine, pumpkin or cactus
regularMobQuantitiesInFields = {
    "rose": {
        "scorpion": 2
    },
    "pumpkin": {
        "werewolf": 1
    },
    "cactus": {
        "werewolf": 1
    },
    "spider": {
        "spider": 1
    },
    "clover": {
        "ladybug": 1,
        "rhinobeetle": 1
    },
    "strawberry": {
        "ladybug": 2,
    },
    "bamboo": {
        "rhinobeetle": 2
    },
    "mushroom": {
        "ladybug": 1
    },
    "blue flower": {
        "rhinobeetle": 1
    },
    "pineapple": {
        "mantis": 1,
        "rhinobeetle": 1
    },
    "pine tree": {
        "mantis": 2,
        "werewolf": 1
    },
}
regularMobTypesInFields = {k: [x[0] for x in v] for k, v in {k:list(v.items()) for k,v in regularMobQuantitiesInFields.items()}.items()}

mobRespawnTimes = {
    "ladybug": 5*60, #5mins
    "rhinobeetle": 5*60, #5mins
    "spider": 30*60, #30mins
    "mantis": 20*60, #20mins
    "scorpion": 20*60, #20mins
    "werewolf": 60*60 #1hr
}

# Define the color range for reset detection (in HSL color space)
#white color respawn pad
resetLower1 = np.array([0, 102, 0])  # Lower bound of the color (H, L, S)
resetUpper1 = np.array([40, 255, 30])  # Upper bound of the color (H, L, S)
#balloon color
resetLower2 = np.array([105, 140, 210])  # Lower bound of the color (H, L, S)
resetUpper2 = np.array([120, 220, 255])  # Upper bound of the color (H, L, S)
resetKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(16,10))


nightFloorDetectThresholds = [
    [np.array([99, 45, 102]), np.array([105, 51, 112])], #starter fields, spawn
    [np.array([80, 15, 114]), np.array([100, 20, 130])], #clover, 15 bee gate, 10 bee gate, 35 bee gate
    []
]
locationToNightFloorType = {
    "spawn": 0,
    "sunflower": 0,
    "dandelion": 0,
    "mushroom": 0,
    "blue_flower": 0,
    "clover": 1,
    "strawberry": 2,
    "spider": 2,
    "bamboo": 2,
    "pineapple": 1,
    "stump": 1,
    "cactus": 1,
    "pumpkin": 1,
    "pine_tree": 1,
    "rose": 2,
    "mountain top": 3,
    "pepper": 1,
    "coconut": 1
}

#store planter's growth data
#[growth time in secs, (list of bonus fields), bonus growth from fields]
planterGrowthData = {
    "paper": [1*60*60, (), 0], #1hr
    "ticket": [2*60*60, (), 0], #2hr
    "festive": [4*60*60, (), 0], #4hr
    "sticker": [3*60*60, (), 0], #3hr
    "plastic": [2*60*60, (), 0], #2hr
    "candy": [4*60*60, ("strawberry", "pineapple", "coconut"), 0.25], #4hr
    "red clay": [6*60*60, ("sunflower", "dandelion", "mushroom", "clover", "strawberry", "pineapple", "stump", "cactus", "pumpkin", "rose", "mountain top", "pepper", "coconut"), 0.25], #6hr
    "blue clay": [6*60*60, ("sunflower", "dandelion", "blue flower", "clover", "bamboo", "pineapple", "stump", "cactus", "pumpkin", "pine tree", "mountain top", "coconut"), 0.25], #6hr
    "tacky": [8*60*60, ("sunflower", "dandelion", "mushroom", "blue flower", "clover"), 0.25], #8hr
    "pesticide": [10*60*60, ("bamboo", "spider", "strawberry"), 0.3], #10hr
    "heat-treated": [12*60*60, ("sunflower", "dandelion", "mushroom", "clover", "strawberry", "pineapple", "stump", "cactus", "pumpkin", "rose", "mountain top", "pepper", "coconut"), 0.5], #12hr
    "hydroponic": [12*60*60, ("sunflower", "dandelion", "blue flower", "clover", "bamboo", "pineapple", "stump", "cactus", "pumpkin", "pine tree", "mountain top", "coconut"), 0.5], #12hr
    "petal": [14*60*60, ("sunflower", "dandelion", "blue flower", "mushroom" "clover", "bamboo", "strawberry", "pineapple", "stump", "cactus", "pumpkin", "pine tree", "rose", "mountain top", "coconut", "pepper"), 0.5], #14hrs
    "planter of plenty": [16*60*60, ("pepper", "stump", "coconut", "mountain top"), 0.5] #16hr
}

#a list of all items that can be crafted by the blender in order
blenderItems = ["red extract", "blue extract", "enzymes", "oil", "glue", "tropical drink", "gumdrops", "moon charm",
    "glitter",
    "star jelly",
    "purple potion",
    "soft wax",
    "hard wax",
    "swirled wax",
    "caustic wax",
    "field dice",
    "smooth dice",
    "loaded dice",
    "super smoothie",
    "turpentine"]

#a list of keys to press to face north after running the cannon_to_field path
fieldFaceNorthKeys = {
    "sunflower": ["."]*2,
    "dandelion": [","]*2,
    "mushroom": None,
    "blue flower": [","]*2,
    "clover": ["."]*4,
    "strawberry": ["."]*2,
    "spider": None,
    "bamboo": [","]*2,
    "pineapple": None,
    "stump": [","]*2,
    "cactus": ["."]*4,
    "pumpkin": None,
    "pine tree": None,
    "rose": ["."]*2,
    "mountain top": ["."]*4,
    "pepper": ["."]*2,
    "coconut": ["."]*4
}

fieldFaceNorthKeys = {
    "sunflower": ["."]*2,
    "dandelion": [","]*2,
    "mushroom": None,
    "blue flower": [","]*2,
    "clover": ["."]*4,
    "strawberry": ["."]*2,
    "spider": None,
    "bamboo": [","]*2,
    "pineapple": None,
    "stump": [","]*2,
    "cactus": ["."]*4,
    "pumpkin": None,
    "pine tree": None,
    "rose": ["."]*2,
    "mountain top": ["."]*4,
    "pepper": ["."]*2,
    "coconut": ["."]*4
}

#the field dimensions taken from natro
#[length, width]
startLocationDimensions = {
    "sunflower": [1250, 2000],
    "dandelion": [2500, 1000],
    "mushroom": [1250, 1750],
    "blue flower": [2750, 750],
    "clover": [2000, 1500],
    "strawberry": [1500, 2000],
    "spider": [2000, 2000],
    "bamboo": [3000, 1250],
    "pineapple": [1750, 3000],
    "stump": [1500, 1500],
    "cactus": [1500, 2500],
    "pumpkin": [1500, 2500],
    "pine tree": [2500, 1700],
    "rose": [2500, 1500],
    "mountain top": [2250, 1500],
    "pepper": [1500, 2250],
    "coconut": [1500, 2250]
}

#for the ocr
#sometimes, it reads the bss font as crillic characters, so it'll need to be converted back to latin
#This isn't an actual translation, the characters are mapped visually
cyrillicToLatin = {
    'А': 'A', 
    'В': 'B', 
    'Е': 'E', 
    'К': 'K', 
    'М': 'M', 
    'Н': 'H',
    'О': 'O', 
    'Р': 'P', 
    'С': 'C', 
    'Т': 'T', 
    'У': 'Y', 
    'Х': 'X',
    'а': 'a', 
    'в': 'B', 
    'е': 'e', 
    'к': 'k', 
    'м': 'm', 
    'н': 'h',
    'о': 'o', 
    'р': 'p', 
    'с': 'c', 
    'т': 't', 
    'у': 'y', 
    'х': 'x'
}

#Load quest data from quest_data.txt
quest_data = {}
quest_bear = ""
quest_title = ""
quest_info = []

with open("./data/bss/quest_data.txt", "r") as f:
    qdata = [x for x in f.read().split("\n") if x]

for line in qdata:
    if line.startswith("==") and line.endswith("=="): #bear
        if quest_title:
            quest_data[quest_bear][quest_title] = quest_info  
        quest_bear = line.strip("=")
        quest_data[quest_bear] = {}
        quest_title, quest_info = "", []
    
    elif line.startswith("-"): #new quest title
        if quest_title:  
            quest_data[quest_bear][quest_title] = quest_info
        quest_title = line.lstrip("-").strip()
        quest_info = []
    
    else:  #quest objectives
        quest_info.append(line)
quest_data[quest_bear][quest_title] = quest_info 

#planter-related info
nectarNames=["comforting", "refreshing", "satisfying", "motivating", "invigorating"]
nectarFields = {
  "comforting": ["dandelion", "bamboo", "pine tree"],
  "refreshing": ["coconut", "strawberry", "blue flower"],
  "satisfying": ["pineapple", "sunflower", "pumpkin"],
  "motivating": ["stump", "spider", "mushroom", "rose"],
  "invigorating": ["pepper", "mountain top", "clover", "cactus"]
}
allPlanters = ["paper", "ticket", "festive", "sticker", "plastic", "candy", "red_clay", "blue_clay", "tacky", "pesticide", "heat-treated", "hydroponic", "petal", "planter_of_plenty"]
with open("./data/bss/auto_planter_ranking.json", "r") as f:
    autoPlanterRankings = json.load(f) 

class macro:
    def __init__(self, status, logQueue, updateGUI, run=None, skipTask=None):
        self.status = status
        self.updateGUI = updateGUI
        self.run = run
        self.skipTask = skipTask
        
        # Set the run state for pause-aware sleep functions
        if run is not None:
            set_run_state(run)
        
        self.setdat = settingsManager.loadAllSettings()
        self.fieldSettings = settingsManager.loadFields()
        # Track profile changes to reload settings when profile is switched
        self._last_profile_change_counter = settingsManager.getProfileChangeCounter()

        self.robloxWindow = RobloxWindowBounds()
        
        self.hasteCompensation = HasteCompensationRevamped(self.robloxWindow, self.setdat["movespeed"])
        self.fieldDriftCompensation = fieldDriftCompensationClass(self.robloxWindow)
        self.keyboard = keyboard(self.setdat["movespeed"], self.setdat["haste_compensation"], self.hasteCompensation)
        # Prepare ping settings
        pingSettings = {
            "ping_critical_errors": self.setdat.get("ping_critical_errors", False),
            "ping_disconnects": self.setdat.get("ping_disconnects", False),
            "ping_character_deaths": self.setdat.get("ping_character_deaths", False),
            "ping_vicious_bee": self.setdat.get("ping_vicious_bee", False),
            "ping_mondo_buff": self.setdat.get("ping_mondo_buff", False),
            "ping_ant_challenge": self.setdat.get("ping_ant_challenge", False),
            "ping_sticker_events": self.setdat.get("ping_sticker_events", False),
            "ping_mob_events": self.setdat.get("ping_mob_events", False),
            "ping_conversion_events": self.setdat.get("ping_conversion_events", False),
            "ping_hourly_reports": self.setdat.get("ping_hourly_reports", False)
        }
        
        self.logger = logModule.log(logQueue, self.setdat.get("enable_webhook", False), self.setdat.get("webhook_link", ""), self.setdat.get("send_screenshot", True), blocking=self.setdat.get("low_performance", False), hourlyReportOnly=self.setdat.get("only_send_hourly_report", False), robloxWindow=self.robloxWindow, enableDiscordPing=self.setdat.get("enable_discord_ping", False), discordUserID=self.setdat.get("discord_user_id", ""), pingSettings=pingSettings, webhookTimeFormat=self.setdat.get("webhook_time_format", 24))
        self.buffDetector = BuffDetector(self.robloxWindow)
        self.hourlyReport = HourlyReport(self.buffDetector, self.setdat.get("hourly_report_time_format", 24))
        self.memoryMatch = MemoryMatch(self.robloxWindow)

        #setup an internal cooldown tracker. The cooldowns can be modified
        self.collectCooldowns = dict([(k, v[2]) for k,v in mergedCollectData.items()])
        self.collectCooldowns["sticker_printer"] = 1*60*60

        #night detection variables
        self.enableNightDetection = True if self.setdat["stinger_hunt"] else False
        self.canDetectNight = True
        self.night = False
        self.location = "spawn"
        #all fields that vic can appear in
        self.vicFields = ["pepper", "mountain top", "rose", "cactus", "spider", "clover"]
        #filter it to only include fields the player has enabled
        self.vicFields = [x for x in self.vicFields if self.setdat["stinger_{}".format(x.replace(" ","_"))]]

        self.newUI = False

        self.planterCooldowns = {}

        #memory match
        self.latestMM = "normal"

        self.isGathering = False
        self.converting = False
        self.alreadyConverted = False
        self.cannonFromHive = False

        #auto field boost
        self.failed = False
        self.AFBLIMIT = False
        self.AFBglitter = False
        self.cAFBglitter = False
        self.cAFBDice = False
        self.afb = False
        self.stop = False

        self.hiveDistance = 1.32 #distance between hives (in seconds)


        self.setRobloxWindowInfo(setYOffset=False)

    def checkAndReloadSettings(self):
        """Check if profile has changed and reload settings if needed"""
        current_counter = settingsManager.getProfileChangeCounter()
        if current_counter != self._last_profile_change_counter:
            self._last_profile_change_counter = current_counter
            # Reload settings
            old_profile = settingsManager.getCurrentProfile()
            self.setdat = settingsManager.loadAllSettings()
            self.fieldSettings = settingsManager.loadFields()
            # Update logger with new webhook settings
            pingSettings = {
                "ping_critical_errors": self.setdat.get("ping_critical_errors", False),
                "ping_disconnects": self.setdat.get("ping_disconnects", False),
                "ping_character_deaths": self.setdat.get("ping_character_deaths", False),
                "ping_vicious_bee": self.setdat.get("ping_vicious_bee", False),
                "ping_mondo_buff": self.setdat.get("ping_mondo_buff", False),
                "ping_ant_challenge": self.setdat.get("ping_ant_challenge", False),
                "ping_sticker_events": self.setdat.get("ping_sticker_events", False),
                "ping_mob_events": self.setdat.get("ping_mob_events", False),
                "ping_conversion_events": self.setdat.get("ping_conversion_events", False),
                "ping_hourly_reports": self.setdat.get("ping_hourly_reports", False)
            }
            self.logger.enableWebhook = self.setdat.get("enable_webhook", False)
            self.logger.webhookURL = self.setdat.get("webhook_link", "")
            self.logger.sendScreenshots = self.setdat.get("send_screenshot", True)
            self.logger.enableDiscordPing = self.setdat.get("enable_discord_ping", False)
            self.logger.discordUserID = self.setdat.get("discord_user_id", "")
            self.logger.pingSettings = pingSettings
            self.logger.webhookTimeFormat = self.setdat.get("webhook_time_format", 24)
            self.logger.hourlyReportOnly = self.setdat["only_send_hourly_report"]
            # Update keyboard movespeed
            self.keyboard.movespeed = self.setdat["movespeed"]
            # Update haste compensation
            self.hasteCompensation = HasteCompensationRevamped(self.robloxWindow, self.setdat["movespeed"])
            self.keyboard.hasteCompensation = self.setdat["haste_compensation"]
            self.keyboard.hasteCompensationObj = self.hasteCompensation
            # Update hourly report time format
            self.hourlyReport.timeFormat = self.setdat.get("hourly_report_time_format", 24)
            # Update collect cooldowns
            self.collectCooldowns = dict([(k, v[2]) for k,v in mergedCollectData.items()])
            self.collectCooldowns["sticker_printer"] = 1*60*60
            # Update night detection
            self.enableNightDetection = True if self.setdat["stinger_hunt"] else False
            # Update vic fields
            self.vicFields = ["pepper", "mountain top", "rose", "cactus", "spider", "clover"]
            self.vicFields = [x for x in self.vicFields if self.setdat["stinger_{}".format(x.replace(" ","_"))]]
            # Log the profile change
            self.logger.webhook("Profile Changed", f"Switched to profile: {old_profile}", "blue")

    #get the size of the roblox window and update the relevant variables
    def setRobloxWindowInfo(self, setYOffset=True):
        self.robloxWindow.setRobloxWindowBounds(setYOffset=setYOffset)
        if setYOffset:
            self.logger.webhook("", f"Detect Y Offset: {self.robloxWindow.contentYOffset}", "dark brown")
    
    def checkPauseAndWait(self):
        """Check if macro is paused and wait until resumed. Returns True if stop was requested."""
        if self.run is None:
            return False
        # Check for pause request (state 5) - transition to paused (state 6)
        if self.run.value == 5:
            # Release all movement keys and mouse
            self.keyboard.releaseMovement()
            mouse.mouseUp()
            # Transition to paused state - this signals the main loop that we've stopped
            self.run.value = 6
        # Wait while paused (state 6)
        while self.run.value == 6:
            # Keep inputs released while paused
            self.keyboard.releaseMovement()
            mouse.mouseUp()
            time.sleep(0.1)
        # Check if stop was requested (state 0)
        return self.run.value == 0
    
    #thread to detect night
    #night detection is done by converting the screenshot to hsv and checking the average brightness
    #TODO:
    # MAYBE this doesnt actually need to be a thread? Check for night after each reset, when converting and when gathering
    def detectNight(self):
        #detects the average brightness of the screen. This isn't very reliable since things like lights can mess it up
        #the threshold isnt accurate
        def isNightBrightness(hsv):
            hsv = hsv[int(hsv.shape[0]/3):hsv.shape[0]]
            vValues = np.sum(hsv[:, :, 2])
            area = hsv.shape[0] * hsv.shape[1]
            avg_brightness = vValues/area
            #threshold for night. It must be > 10 to deal with cases where the player is inside a fruit or stuck against a wall 
            return 10 < avg_brightness < 80 

        #Detect the color of the floor at spawn
        #Useful when resetting/converting
        def isSpawnFloorNight(hsv):
            hsv = hsv[int(hsv.shape[0]/2):hsv.shape[0]]
            lower = np.array([99, 45, 102])
            upper = np.array([105, 51, 112])

            #might increase kernel size on retina
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))

            mask = cv2.inRange(hsv, lower, upper)   
            mask = cv2.erode(mask, kernel, 2)

            #if np.mean = 0, no color ranges are detected, is day, hence return false
            return np.mean(mask)
        
        def isNightSky(bgr):
            y = 30*self.robloxWindow.multi
            #crop the image to only the area above buff
            bgr = bgr[0:y, 180*self.robloxWindow.multi:int(self.robloxWindow.mw)]
            w,h = bgr.shape[:2]
            #check if a 15x15 area that is entirely black
            for x in range(w-15):
                for y in range(h-15):
                    area = bgr[x:x+15, y:y+15]
                    if np.all(area == [0, 0, 0]):
                        return True
            return False
        
        #detect the color of the grass in fields
        #useful when gathering
        def isGrassNight(bgr):       
            dayColors = [
                [(47, 117, 57), cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))], #ground
                [(46, 117, 58), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #dande
                [(60, 156, 74), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #stump
                [(38, 114, 51), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #pa
                [(66, 123, 40), cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))], #clov
                [(32, 211, 22), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #ant
            ]

            nightColors = [
                [(23, 72, 30), cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))], #a
                [(17, 71, 28), cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))], #dande
            ]

            bgr = bgr[0:bgr.shape[0]- (100*self.robloxWindow.multi)]
            dayScreen = bgr[int(bgr.shape[0]*2/5):bgr.shape[0]].copy()
            #detect day
            for color, kernel in dayColors:
                if findColorObjectRGB(dayScreen, color, variance=6, kernel=kernel, mode="box"):
                    return False
            #day not found, detect Night
            nightScreen = bgr[int(bgr.shape[0]/2):bgr.shape[0]].copy()
            for color, kernel in nightColors:
                if findColorObjectRGB(nightScreen, color, variance=6, kernel=kernel, mode="box"):
                    return True
                
            return False

        def isNight():
            screen = mssScreenshotNP(self.robloxWindow.mx,self.robloxWindow.my, self.robloxWindow.mw, self.robloxWindow.mh)
            # Convert the image from BGRA to HSV
            bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

            if self.converting:
                nightDetected = isNightSky(bgr)
            else:
                nightDetected = isGrassNight(bgr)

            #night detected
            if nightDetected:
                self.nightDetectStreaks += 1
                #self.logger.webhook("", f"Night Detected? ({self.nightDetectStreaks})", "red", "screen")
                #im = Image.fromarray(cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
                #im.save(f"night-{time.time()}.png")
            else: 
                #failed to detect night, reset streak counter
                self.nightDetectStreaks = 0

            #detected night consecutively for 5 times or more
            if self.nightDetectStreaks >= 5:
                return True
            
            return False
        
        if self.canDetectNight and isNight():
            self.night = True
            self.logger.webhook("","Night detected","dark brown", "screen")
            time.sleep(200) #wait for night to end
            self.night = False
            self.nightDetectStreaks = 0

    def isFullScreen(self):
        if sys.platform == "darwin":
            windows = gw.getAllTitles()
            for win in windows:
                if "roblox roblox" in win.lower():
                    x,y,w,h = gw.getWindowGeometry(win)
                    return x==0 and y==0 and w==self.robloxWindow.mw and h==self.robloxWindow.mh
            #can't find the roblox window, most likely fullscreen? Assumes that it exists
            return True
                    
        else:
            menubarRaw = ocr.customOCR(0, 0, 300, 60, 0) #get menu bar on mac, window bar on windows
            menubar = ""
            try:
                for x in menubarRaw:
                    menubar += x[1][0]
            except:
                pass
            menubar = menubar.lower()
            return not ("rob" in menubar or "lox" in menubar) #check if roblox can be found in menu bar

    def toggleFullScreen(self):
        if sys.platform == "darwin":
            self.keyboard.keyDown("command")
            time.sleep(0.05)
            self.keyboard.keyDown("ctrl")
            time.sleep(0.05)
            self.keyboard.keyDown("f")
            time.sleep(0.1)
            self.keyboard.keyUp("command")
            self.keyboard.keyUp("ctrl")
            self.keyboard.keyUp("f")
        elif sys.platform == "win32":
            for _ in range(3):
                self.keyboard.press("f11")
                time.sleep(0.4)

    def adjustImage(self, path, imageName):
        return adjustImage(path, imageName, self.robloxWindow.display_type)
        
    #run a path. Choose automater over python if it exists (except on windows)
    #file must exist: if set to False, will not attempt to run the file if it doesnt exist
    def runPath(self, name, fileMustExist = True):
        ws = self.setdat["movespeed"]
        path = f"../paths/{name}"
        #try running a automator workflow
        #if it doesnt exist, run the .py file instead

        if os.path.exists(path+".workflow") and sys.platform == "darwin":
            os.system(f"/usr/bin/automator {path}.workflow")
        else:
            pyPath = f"{path}.py"
            #ensure that path exists
            if not fileMustExist and not os.path.isfile(pyPath): return
            exec(open(pyPath).read())

    def getBackpack(self):
        return bpc(self.robloxWindow.mx+(self.robloxWindow.mw//2+59+3), self.robloxWindow.my+self.robloxWindow.yOffset+6)
    
    def faceDirection(self, field, dir):
        keys = fieldFaceNorthKeys[field]
        if dir == "south": #invert the keys
            if keys is None:
                keys = ["."]*4
            elif len(keys) == 4:
                keys = None
            else:
                keys = ["." if x == "," else "," for x in keys]
        
        if keys is not None:
            for k in keys:
                self.keyboard.press(k)

    #run the path to go to a field
    #faceDir what direction to face after landing in a field (default, north, south)
    def goToField(self, field, faceDir = "default"):
        # Normalize field name to handle both space and underscore formats
        normalized_field = field.replace('_', ' ')
        self.location = normalized_field
        self.runPath(f"cannon_to_field/{normalized_field}")
        if faceDir == "default": return
        self.faceDirection(normalized_field, faceDir)

    def convertCyrillic(self, original):
        out = ""
        for x in original:
            if x in cyrillicToLatin:
                x = cyrillicToLatin[x]
            out += x
        return out 
    
    def isInOCR(self, name, includeList, excludeList, log=False):
        #get text
        textRaw = ocr.imToString(name).lower()
        if log: print(f"Raw text: {textRaw}")
        #correct the text
        text = self.convertCyrillic(textRaw)

        #check if text is to be rejected
        if log: print(f"output text: {text}")
        for i in excludeList:
            if i in text: return False
        #check if its to be accepted
        for i in includeList:
            if i in text:  return text
        return False
    
    def getTextBesideE(self):
        img = mssScreenshot(self.robloxWindow.mx+(self.robloxWindow.mw//2-200), self.robloxWindow.my+self.robloxWindow.yOffset+34, 400, 140)
        textRaw = ''.join([x[1][0] for x in ocr.ocrRead(img)]).lower()
        return self.convertCyrillic(textRaw)
    
    def isBesideE(self, includeList = [], excludeList = [], log=False):
        #get text
        text = self.getTextBesideE()

        #check if text is to be rejected
        if log: print(f"output text: {text}")
        for i in excludeList:
            if i in text: return False
        #check if its to be accepted
        for i in includeList:
            if i in text:  return text
        return False
    
    def isBesideEImage(self, name):
        template = self.adjustImage("./images/menu",name)
        return locateTransparentImageOnScreen(template, self.robloxWindow.mx+(self.robloxWindow.mw//2-200), self.robloxWindow.my+self.robloxWindow.yOffset+34, 400, 140, 0.75)

    def getTiming(self,name = None):
        for _ in range(3):
            data = settingsManager.readSettingsFile("./data/user/timings.txt")
            if data: break #most likely another process is writing to the file
            time.sleep(0.1)
        if name is not None:
            if not name in data:
                print(f"could not find timing for {name}, setting a new one")
                self.saveTiming(name)
                return time.time()
            return data[name]
        return data
    
    def saveTiming(self, name):
        return settingsManager.saveSettingFile(name, time.time(), "./data/user/timings.txt")
    #returns true if the cooldown is up
    #note that cooldown is in seconds
    def hasRespawned(self, name, cooldown, applyMobRespawnBonus = False, timing = None):
        if timing is None: timing = self.getTiming(name)
        if not isinstance(timing, float) and not isinstance(timing, int):
            print(f"Timing is not a valid number? {timing}")
        mobRespawnBonus = 1
        if applyMobRespawnBonus:
            mobRespawnBonus -= 0.15 if self.setdat["gifted_vicious"] else 0
            mobRespawnBonus -= self.setdat["stick_bug_amulet"]/100 
            mobRespawnBonus -= self.setdat["icicles_beequip"]/100 
    
        return time.time() - timing >= cooldown*mobRespawnBonus

    def isInBlueTexts(self, includeList = [], excludeList = []):
        return self.isInOCR("blue", includeList, excludeList)
    
    #detect the honey/pollen bar to determine if its new or old ui
    # def getTop(self,y):
    #     height = 30
    #     if self.display_type == "retina":
    #         height*=2
    #         y*=2
    #     res = ocr.customOCR(self.wx+self.ww/3.5, self.wy+y, self.ww/2.5, height,0)
    #     if not res: return False
    #     text = ''.join([x[1][0].lower() for x in res])
    #     return "honey" in text or "pollen" in text
    
    #place sprinklers by jumping up and down and placing them middair
    def placeSprinkler(self):
        sprinklerCount = {
            "basic":1,
            "silver":2,
            "golden":3,
            "diamond":4,
            "saturator":1
        }
        sprinklerSlot = str(self.setdat['sprinkler_slot'])
        times = sprinklerCount[self.setdat["sprinkler_type"]]
        #place one sprinkler and check if its in field
        self.keyboard.press(sprinklerSlot)
        time.sleep(1)
        if self.blueTextImageSearch("notinfield"):
            return False
        #place the remaining sprinklers
        #hold jump and spam place sprinklers
        if times > 2:
            self.keyboard.keyDown("space")
            st = time.time()
            while time.time() - st < times*2:
                self.keyboard.press(sprinklerSlot)
            self.keyboard.keyUp("space")
        return True
    
    def waitForBees(self):
        if self.alreadyConverted:
            return
        bees = self.setdat["bees"]
        if bees > 45:
            time.sleep(4)
        elif bees > 40:
            time.sleep(8)
        elif bees > 35:
            time.sleep(13)
        else:
            time.sleep(20)
    #click the yes popup
    #if detect is set to true, the macro will check if the yes button is there
    #if detectOnly is set to true, the macro will not click 
    def clickYes(self, detect = False, detectOnly = False, clickOnce=False):
        yesImg = self.adjustImage("./images/menu", "yes")
        x = self.robloxWindow.mx+self.robloxWindow.mw//2-270
        y = self.robloxWindow.my+self.robloxWindow.mh//2-60
        time.sleep(0.4)
        threshold = 0
        if detect or detectOnly: threshold = 0.75
        res = locateImageOnScreen(yesImg, x, y, 580, 265, threshold)
        if res is None: return False
        if detectOnly: return True
        bestX, bestY = [x//self.robloxWindow.multi for x in res[1]]
        mouse.moveTo(bestX+x, bestY+y)
        time.sleep(0.2)
        mouse.moveBy(5, 5)
        time.sleep(0.1)
        for _ in range(1 if clickOnce else 2):
            mouse.click()
        return True
    
    def toggleInventory(self, mode):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        screen = mssScreenshotNP(self.robloxWindow.mx+4, self.robloxWindow.my+100, 50, 60)
        open = findColorObjectRGB(screen, (254, 254, 254), kernel=kernel, variance=3)
        
        def clickInv():
            mouse.moveTo(self.robloxWindow.mx+30, self.robloxWindow.my+113)
            time.sleep(0.1)
            mouse.moveBy(0,3)
            time.sleep(0.1)
            mouse.click()
            time.sleep(0.1)

        if mode == "open": #already open
            #click the system settings
            mouse.moveTo(self.robloxWindow.mx+245, self.robloxWindow.my+113)
            time.sleep(0.1)
            mouse.moveBy(0,3)
            time.sleep(0.1)
            mouse.click()
            clickInv()
            time.sleep(0.1)
        else:
            clickInv()
        self.moveMouseToDefault()
        time.sleep(0.3)
        '''
        self.keyboard.press("\\")
        #align with first buff
        for _ in range(7):
            self.keyboard.press("w")
        for _ in range(20):
            self.keyboard.press("a")
        #open inventory
        if sys.platform == "darwin":
            for _ in range(5):
                self.keyboard.press("w")
                time.sleep(0.1)
            self.keyboard.press("s")
            self.keyboard.press("a")
            time.sleep(0.1)
            self.keyboard.press("enter")
        else:
            self.keyboard.press("s")
            self.keyboard.press("enter")
        '''

    #scroll to an item in the inventory and return the x,y coordinates
    def getStringSimilarity(self, str1, str2):
        return SequenceMatcher(None, str1, str2).ratio()
    
    def findItemInInventory(self, itemName):
        
        def scrollToTop():
            prevHash = None
            for i in range(9):
                mouse.scroll(100)
                sleep(0.05)
                if i > 10:
                    screen = cv2.cvtColor(mssScreenshotNP(self.robloxWindow.mx, self.robloxWindow.my+120, 100, 200), cv2.COLOR_BGRA2RGB)
                    hash = imagehash.average_hash(Image.fromarray(screen))
                    if not prevHash is None and prevHash == hash:
                        break
                    prevHash = hash
        #for retina, just a regular image search
        #for built-in, a transparency search
        itemImg = self.adjustImage("./images/inventory/old", itemName)
        #itemImg = cv2.cvtColor(itemImg, cv2.COLOR_RGB2GRAY)

        itemOCRName = itemName.lower().replace("planter", "") #the name of the item used to check with the ocr to verify its correct
        itemH, itemW, *_ = itemImg.shape
        itemW //= self.robloxWindow.multi
        itemH //= self.robloxWindow.multi

        #open inventory
        self.toggleInventory("open")
        time.sleep(0.3)
        mouse.moveTo(self.robloxWindow.mx+312, self.robloxWindow.my+200)
        mouse.click()
        #scroll to top
        scrollToTop()
        #scroll down, note the best match
        bestResults = []
        bestY = None
        foundEarly = False #if the max_val > 0.9, end searching early to save time

        prevHash = None
        time.sleep(0.3)
        for i in range(180):
            #screen = cv2.cvtColor(mssScreenshotNP(90, 90, 300-90, self.robloxWindow.mh-180), cv2.COLOR_RGBA2GRAY)
            #max_loc = fastFeatureMatching(screen, itemImg)
            #max_val = 1 if max_loc else 0
            max_val, max_loc = locateImageOnScreen(itemImg, self.robloxWindow.mx, self.robloxWindow.my+90, 100, self.robloxWindow.mh-180)
            data = (max_val, max_loc, i)
            #most likely the correct item, stop searching
            if max_val > 0.7:
                itemScreenshot = mssScreenshot(self.robloxWindow.mx+90, self.robloxWindow.my+(max_loc[1]//self.robloxWindow.multi)+60, 220, 60)
                itemOCRText = ''.join([x[1][0] for x in ocr.ocrRead(itemScreenshot)]).replace(" ","").replace("-","").lower()
                if itemOCRName in itemOCRText or self.getStringSimilarity(itemOCRName, itemOCRText) > 0.7:
                    print(itemOCRText)
                    bestY = max_loc[1]
                    foundEarly = True
                    break
            
            #store the top 5 results
            if len(bestResults) < 5 or max_val > bestResults[-1][0]:
                bestResults.append(data) 
                bestResults.sort(reverse=True, key=lambda x: x[0]) #sort by confidence value
                if len(bestResults) > 5: 
                    bestResults.pop()
                    
            mouse.scroll(-2, True)
            time.sleep(0.06)

            screen = cv2.cvtColor(mssScreenshotNP(self.robloxWindow.mx, self.robloxWindow.my+100, 100, 200), cv2.COLOR_BGRA2RGB)
            hash = imagehash.average_hash(Image.fromarray(screen))
            if not prevHash is None and prevHash == hash:
                break
            prevHash = hash

            # self.logger.webhook("", f"Could not find {itemName} in inventory", "dark brown")
            # self.toggleInventory("close")
            # return None

        if not foundEarly:
            pass
            # #scroll through the top items and find them
            # scrollToTop()
            # time.sleep(0.3)
            # currentScrollCount = 0
            # #sort by scroll count (start with highest item first)
            # bestResults.sort(key=lambda x: x[2])
            # print(bestResults)
            # for val, loc, scrollCount in bestResults:
            #     #scroll to item
            #     for _ in range(scrollCount-currentScrollCount):
            #         mouse.scroll(-40, True)
            #         time.sleep(0.03)
            #     currentScrollCount = scrollCount
            #     time.sleep(0.7)
            #     #use ocr to check that the item has been found
            #     itemScreenshot = mssScreenshot(90, (loc[1]//2 if self.display_type == "retina" else loc[1])+60, 220, 60, True)
            #     itemOCRText = ''.join([x[1][0] for x in ocr.ocrRead(itemScreenshot)]).replace(" ","").replace("-","").lower()
            #     if itemOCRName in itemOCRText or self.getStringSimilarity(itemOCRName, itemOCRText) > 0.6:
            #         bestY = loc[1]
            #         break
        
        #use ocr to check that the item has been found
        '''
        itemScreenshot = mssScreenshot(90+bestX, 90+bestY-itemH/2, itemW, itemH, True)
        itemOCRText = ''.join([x[1][0] for x in ocr.ocrRead(itemScreenshot)]).replace(" ","").replace("-","").lower()
        if not (itemOCRName in itemOCRText or self.getStringSimilarity(itemOCRName, itemOCRText) > 0.6):
            self.logger.webhook("", f"Could not find {itemName} in inventory", "dark brown")
            return None
        ''' 
        if not bestY:   
            self.logger.webhook("", f"Could not find {itemName} in inventory", "dark brown")
            return
        #return (bestX+20, bestY+80+20)
        bestY //= self.robloxWindow.multi
        return (40, bestY+80)
        
    
    #click at the specified coordinates to use an item in the inventory
    #if x/y is not provided, find the item in inventory
    def useItemInInventory(self, itemName = None, x = None, y = None, closeInventoryAfter=True):
        if x is None or y is None:
            if itemName is None: raise Exception("tried searching for item but no item name is provided")
            res = self.findItemInInventory(itemName)
            if res is None:
                return False
            x, y = res

        mouse.moveTo(self.robloxWindow.mx+x, self.robloxWindow.my+y)
        mouse.moveBy(10,15)
        for _ in range(3):
            mouse.click()
            mouse.moveBy(0,15, pause=False)
            time.sleep(0.03)
        self.clickYes()
        #close inventory
        if closeInventoryAfter:
            self.toggleInventory("close")
        return True


    def convert(self, bypass = False):
        self.location = "spawn"
        if not bypass:
            if not self.isBesideEImage("makehoney"): 
                self.alreadyConverted = False
                return False
        #start convert
        #check that the game has started converting
        for _ in range(3):  #must always be an odd number
            self.keyboard.press("e")
            time.sleep(1)
            if self.isBesideE(["stop", "making"], ["make"], log=True): 
                break

        self.status.value = "converting"
        st = time.time()
        self.logger.webhook("", "Converting", "brown", "screen")
        self.alreadyConverted = True
        self.converting = True

        #check if convert balloon
        convertBalloon = (self.setdat["convert_balloon"] == "always") or \
                        (self.setdat["convert_balloon"] == "every" and self.hasRespawned("convert_balloon", self.setdat["convert_balloon_every"]*60))
        
        convertedBackpack = False

        if self.enableNightDetection:
            self.keyboard.press(",")
        
        while True:
            # Check if paused and wait
            if self.checkPauseAndWait():
                # Stop was requested while paused
                self.status.value = ""
                self.converting = False
                return False
            
            #check if the macro is done converting/not converting
            text = self.getTextBesideE()
            #done converting
            doneConverting = False
            if not "stop" in text and not "making" in text:
                for i in ["pollen", "flower", "field"]:
                    if i in text:
                        doneConverting = True
                        break
            if doneConverting: 
                break
            #not converting
            if "make" in text and not "stop" in text:
                self.keyboard.press("e")
                time.sleep(2)

            mouse.click()

            if self.night and self.setdat["stinger_hunt"]:
                self.hourlyReport.addHourlyStat("converting_time", time.time()-st)
                self.keyboard.press(".")
                self.converting = False
                self.stingerHunt()
                return
            
            #check if backpack is done
            if not convertedBackpack:
                for _ in range(4):
                    backpack = self.getBackpack()
                    if backpack: break #continue converting
                else:
                    #backpack is done converting, now convert balloon
                    convertedBackpack = True
                    if not convertBalloon: break
                    self.logger.webhook("", "Converting Balloon", "light blue")

            if time.time()-st > 30*60: #30mins max
                self.logger.webhook("","Converting timeout (30mins max)", "brown", "screen")
                break

            #check for afb
            if self.setdat["Auto_Field_Boost"] and not self.AFBLIMIT and not self.afb:
                #glitter is not up, but dice is
                if self.hasAFBRespawned("AFB_dice_cd", self.setdat["AFB_rebuff"]*60) and not self.AFBglitter and not self.failed: 
                    self.afb = True
                    self.stop = True
                    self.cAFBDice = True
                    self.logger.webhook("Rebuffing","AFB", "brown")
                    time.sleep(1)
                    self.AFB()
                    self.cAFBDice = False
                    self.logger.webhook("", "Still converting", "brown")
                #glitter is up, g
                elif self.setdat["AFB_glitter"] and self.hasAFBRespawned("AFB_glitter_cd", self.setdat["AFB_rebuff"]*60+30) and self.AFBglitter and not self.failed and not self.afb: #if used dice before
                    self.status.value = ""
                    self.afb = True
                    self.stop = True
                    self.cAFBglitter = True
                    self.logger.webhook("Converting: interrupted","AFB", "brown")
                    time.sleep(1)
                    self.AFB()
                    self.AFBglitter = False
                    self.cAFBglitter = False
                    self.logger.webhook("", "Continuing conversion", "brown")
                    self.status.value = "converting"
                if not self.converting: break

        if convertBalloon: self.saveTiming("convert_balloon")
        self.status.value = ""
        #deal with the extra delay
        self.logger.webhook("", f"Finished converting (Time: {self.convertSecsToMinsAndSecs(time.time()-st)})", "brown", "screen", ping_category="ping_conversion_events")
        wait = self.setdat["convert_wait"]
        if (wait):
            self.logger.webhook("", f'Waiting for an additional {wait} seconds', "light green")
        time.sleep(wait)

        if self.enableNightDetection:
            self.keyboard.press(".")
        self.converting = False
        self.hourlyReport.addHourlyStat("converting_time", time.time()-st)
        return True

    def moveMouseToDefault(self):
        mouse.moveTo(self.robloxWindow.mx+370, self.robloxWindow.my+self.robloxWindow.yOffset+110)

    def reset(self, hiveCheck = False, convert = True, AFB = False):
        self.alreadyConverted = False
        self.keyboard.releaseMovement()

        #reset until player is at hive
        for i in range(5):
            self.logger.webhook("", f"Resetting character, Attempt: {i+1}", "dark brown")
            #set mouse and execute hotkeys
            #mouse.teleport(self.robloxWindow.mw/(self.xsm*4.11)+40,(self.robloxWindow.mh/(9*self.ysm))+yOffset)
            self.canDetectNight = False
            st = time.time()
            #close any menus if they exist
            self.clickPermissionPopup()
            print(f"checked permission popup: {time.time()-st}")
            
            closeImg = self.adjustImage("./images/menu", "close") #sticker printer
            print(f"adjusted sticker printer image: {time.time()-st}")
            if locateImageOnScreen(closeImg, self.robloxWindow.mx+(self.robloxWindow.mw/4), self.robloxWindow.my+(100), self.robloxWindow.mw/4, self.robloxWindow.mh/3.5, 0.7):
                self.keyboard.press("e")
            print(f"check sticker printer popup: {time.time()-st}")
            
            mmImg = self.adjustImage("./images/menu", "mmopen") #memory match
            if locateImageOnScreen(mmImg, self.robloxWindow.mx+(self.robloxWindow.mw/4), self.robloxWindow.my+(self.robloxWindow.mh/4), self.robloxWindow.mw/4, self.robloxWindow.mh/3.5, 0.8):
                self.canDetectNight = False
                self.memoryMatch.solveMemoryMatch(self.latestMM)
                self.canDetectNight = True
            print(f"checked memory match popup: {time.time()-st}")

            blenderImg = self.adjustImage("./images/menu", "blenderclose") #blender
            if locateImageOnScreen(blenderImg, self.robloxWindow.mx+(self.robloxWindow.mw/4), self.robloxWindow.my+(self.robloxWindow.mh/5), self.robloxWindow.mw/7, self.robloxWindow.mh/4, 0.8):
                self.closeBlenderGUI()
            print(f"checked blender popup: {time.time()-st}")
            
            self.clickdialog(mustFindDialog=True)
            print(f"checked dialog: {time.time()-st}")

            performanceStatsImg = self.adjustImage("./images/menu", "performancestats")
            if locateTransparentImageOnScreen(performanceStatsImg, self.robloxWindow.mx, self.robloxWindow.my, self.robloxWindow.mw/3.5, 70, 0.7):
                if sys.platform == "darwin":
                    '''
                    #self.keyboard.keyDown("fn", False)
                    self.keyboard.keyDown("command", False)
                    self.keyboard.keyDown("option", False)
                    self.keyboard.keyDown("f7")
                    #self.keyboard.keyUp("fn")
                    self.keyboard.keyUp("command", False)
                    self.keyboard.keyUp("option", False)
                    self.keyboard.keyUp("f7", False)
                    '''
                    pass
                else:
                    pass
            print(f"checked performance stats: {time.time()-st}")

            keepOld = self.keepOldCheck()
            if keepOld is not None:
                time.sleep(0.1)
                mouse.moveTo(*keepOld)
                time.sleep(0.2)
                mouse.click()

            noImg = self.adjustImage("./images/menu", "no") #yes/no popup
            x = self.robloxWindow.mx + self.robloxWindow.mw/2-300
            y = self.robloxWindow.my
            res = locateImageOnScreen(noImg, x, y, 650, self.robloxWindow.mh, 0.8)
            print(f"checked yes/no popup: {time.time()-st}")
            #mssScreenshot(x,y,self.robloxWindow.mw/2.5,self.robloxWindow.mh/3.4, True)
            if res:
                x2, y2 = [j//self.robloxWindow.multi for j in res[1]]
                mouse.moveTo(x+x2, y+y2)
                time.sleep(0.08)
                mouse.moveBy(1,1)
                time.sleep(0.1)
                mouse.click()

            stickerBookImg = self.adjustImage("./images/menu", "stickerbookclose") #sticker book
            x = self.robloxWindow.mx+250
            y = self.robloxWindow.my+110
            res = locateImageOnScreen(stickerBookImg, x, y, 100, 80, 0.8)
            if res:
                x2, y2 = res[1]
                mouse.moveTo(x+x2, y+y2)
                time.sleep(0.08)
                mouse.moveBy(1,3)
                time.sleep(0.1)
                mouse.click()
            print(f"checked sticker book popup: {time.time()-st}")

            # robloxMenu = self.adjustImage("./images/menu", "robloxmenu")
            # if not locateImageOnScreen(robloxMenu, self.robloxWindow.mx, self.robloxWindow.my, 75, 60, 0.8):
            #     self.keyboard.press('esc')
            #     time.sleep(0.5)
            # mouse.moveTo(self.robloxWindow.mx+37, self.robloxWindow.my+34)
            # time.sleep(0.1)
            # mouse.click()
            for _ in range(2):
                self.keyboard.press('esc')
                time.sleep(0.3)
                self.keyboard.press('r')
                time.sleep(0.25)
                self.keyboard.press('w')
                time.sleep(0.25)
                self.keyboard.press('enter')
                time.sleep(0.4)
            self.moveMouseToDefault()
            print(f"pressed reset keys: {time.time()-st}")
            
            if self.newUI:
                emptyHealth = self.adjustImage("./images/menu", "emptyhealth_new")
            else:
                emptyHealth = self.adjustImage("./images/menu", "emptyhealth")
            healthBar = False #check if the health bar appears when the player resets. For some reason, the empty health bar doesnt always appear
            st = time.time()
            #wait for empty health bar to appear
            while time.time() - st < 3: 
                if locateImageOnScreen(emptyHealth, self.robloxWindow.mx+(self.robloxWindow.mw-150), self.robloxWindow.my, 150, 60, 0.8):
                    healthBar = True
                    break
            if healthBar: #check if the health bar has b detected. If it hasnt, just wait for a flat time
                #if the empty health bar disappears, player has respawned
                st = time.time()
                while time.time() - st < 8:
                    if not locateImageOnScreen(emptyHealth, self.robloxWindow.mx+(self.robloxWindow.mw-150), self.robloxWindow.my, 150, 60, 0.6):
                        time.sleep(0.5)
                        break
            else:
                time.sleep(8-3)

            print(f"respawn complete: {time.time()-st}")

            if AFB: 
                self.logger.webhook("", f"AFB: Cooldown: {self.setdat['AFB_wait']} seconds", "brown")
                time.sleep(self.setdat["AFB_wait"])
                self.died = False

            if self.robloxWindow.contentYOffset == 0:
                self.robloxWindow.setRobloxWindowBounds()

            self.canDetectNight = True
            self.location = "spawn"
            #detect if player is at hive. Spin a max of 4 times
            atHive = False
            for i in range(4):
                screen = pillowToCv2(mssScreenshot(self.robloxWindow.mx+(self.robloxWindow.mw//2-100), self.robloxWindow.my+(self.robloxWindow.mh-10), 200, 10))
                # Convert the image from BGR to HLS color space
                hsl = cv2.cvtColor(screen, cv2.COLOR_BGR2HLS)
                # Create a mask for the color range
                mask1 = cv2.inRange(hsl, resetLower1, resetUpper1)  
                mask2 = cv2.inRange(hsl, resetLower2, resetUpper2)    
                mask = cv2.bitwise_or(mask1, mask2)
                mask = cv2.erode(mask, resetKernel)
                #get contours. If contours exist, direction is correct
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                print(f"spin {i+1}: {time.time()-st}")
                if contours:
                    atHive = True
                    break
                #failed to detect, spin
                for _ in range(4):
                    self.keyboard.press(".")
                time.sleep(0.1)

            for _ in range(8):
                self.keyboard.press("o")
            if atHive:
                self.cannonFromHive = True
                if convert: 
                    self.convert()
                return True
            else:
                self.keyboard.walk("w", 5)
                if convert:
                    self.cannonFromHive = True
                    self.keyboard.walk("s", 0.55)
                    if self.setdat["hive_number"] < 3:
                        dir = "d"
                    else:
                        dir = "a"
                    self.keyboard.walk(dir, self.hiveDistance*abs(self.setdat["hive_number"]-3))
                    self.convert()
                else:
                    self.keyboard.walk("s", 0.15)
                    self.cannonFromHive = False
            return True
        
        else:
            self.logger.webhook("", "Unable to detect that player respawned at hive", "dark brown", "screen")

    def cannon(self, fast = False):
        for i in range(3):
            #Move to canon:
            fieldDist = 0.9
            if self.cannonFromHive:
                self.keyboard.walk("w",0.8)
                hiveNumber = self.setdat["hive_number"]
            else:
                hiveNumber = 3
            self.keyboard.walk("d",1.2*hiveNumber+i)
            if not self.cannonFromHive:
                self.keyboard.walk("w", 0.2)
            self.keyboard.keyDown("d")
            time.sleep(0.5)
            self.keyboard.slowPress("space")
            #os.system('osascript -e \'tell application "System Events" to key code 49\'')
            time.sleep(0.2)
            self.keyboard.keyDown("d")
            self.keyboard.walk("w",0.2)
            
            if fast:
                self.keyboard.walk("d",0.95)
                time.sleep(0.1)
                return
            self.keyboard.walk("d",0.2)
            self.keyboard.walk("s",0.07)
            st = time.time()
            self.keyboard.keyDown("d")
            foundCannon = False
            while time.time()-st < 0.15*6:
                if self.isBesideEImage("cannon"):
                    foundCannon = True
                    break
            self.keyboard.keyUp("d")
            if foundCannon:
                #check if overrun cannon
                for _ in range(3):
                    time.sleep(0.4)
                    if self.isBesideEImage("cannon"):
                        return
                    self.keyboard.walk("a",0.2)
            self.logger.webhook("Notice", f"Could not find cannon", "dark brown", "screen")
            self.reset(convert=False)
        else:
            self.logger.webhook("Notice", f"Failed to reach cannon too many times", "red", ping_category="ping_critical_errors")
            self.rejoin()
    
    def rejoin(self, rejoinMsg = "Rejoining"):
        self.canDetectNight = False
        psLink = self.setdat.get("private_server_link", "")
        self.logger.webhook("",rejoinMsg, "dark brown")
        self.status.value = "rejoining"
        mouse.mouseUp()
        keyboard.releaseMovement()
        for i in range(3):
            joinPS = bool(psLink and psLink.strip()) #join private server?
            rejoinMethod = self.setdat.get("rejoin_method", "deeplink")
            browserLink = "https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129"
            if i == 2 and joinPS: 
                self.logger.webhook("", "Failed rejoining too many times, falling back to a public server", "red", "screen", ping_category="ping_disconnects")
                joinPS = False
            appManager.closeApp("Roblox") # close roblox
            time.sleep(8)
            #execute rejoin method
            if joinPS:
                browserLink = psLink
            if rejoinMethod == "deeplink":
                deeplink = "roblox://placeID=1537690962"
                if joinPS:
                    try:
                        if "code=" in psLink.lower():
                            deeplink += f"&linkCode={psLink.lower().split('code=')[1]}"
                        else:
                            self.logger.webhook("", "Invalid private server link format. Expected 'code=' in link. Falling back to public server.", "red", ping_category="ping_critical_errors")
                            joinPS = False
                    except (IndexError, AttributeError) as e:
                        self.logger.webhook("", f"Error parsing private server link: {e}. Falling back to public server.", "red", ping_category="ping_critical_errors")
                        joinPS = False
                appManager.openDeeplink(deeplink)
            elif rejoinMethod == "new tab":
                webbrowser.open(browserLink, new = 2)
            elif rejoinMethod == "reload":
                webbrowser.open(browserLink, new = 2)
                time.sleep(2)
                if sys.platform == "darwin":
                    self.keyboard.keyDown("command")
                else:
                    self.keyboard.keyDown("ctrl")
                self.keyboard.press("r")
                if sys.platform == "darwin":
                    self.keyboard.keyUp("command")
                else:
                    self.keyboard.keyUp("ctrl")
            #wait for bss to load
            #if sprinkler image is found, bss is loaded
            #max 80s of waiting
            sprinklerImg = self.adjustImage("./images/menu", "sprinkler")
            loadStartTime = time.time()
            signUpImage = self.adjustImage("./images/menu", "signup")
            robloxHomeImage = self.adjustImage("./images/menu", "robloxhome")
            rejoinSuccess = True
            robloxOpenTime = 0
            while not locateImageOnScreen(sprinklerImg, self.robloxWindow.mx, self.robloxWindow.my+(self.robloxWindow.mh*3/4), self.robloxWindow.mw, self.robloxWindow.mh*1/4, 0.75) and time.time() - loadStartTime < 240:
                if appManager.isAppOpen("roblox"):
                    robloxOpenTime = time.time()
                if self.setdat["rejoin_method"] == "deeplink":
                    #check if the user is stuck on the sign up screen
                    if robloxOpenTime and locateImageOnScreen(signUpImage, self.robloxWindow.mx+(self.robloxWindow.mw/4), self.robloxWindow.my+(self.robloxWindow.mh/3), self.robloxWindow.mw/2, self.robloxWindow.mh*2/3, 0.7):
                        self.logger.webhook("","Not logged into the roblox app. Rejoining via the browser. For a smoother experience, please ensure you are logged into the Roblox app beforehand.","red","screen", ping_category="ping_disconnects")
                        self.setdat["rejoin_method"] = "new tab"
                        continue
                    #check if home page is opened instead of the app
                    # if locateImageOnScreen(robloxHomeImage, self.robloxWindow.mx, self.robloxWindow.my, self.robloxWindow.mw/10, self.robloxWindow.mh/6, 0.7) and time.time() - loadStartTime > 10:
                    if robloxOpenTime and time.time() - robloxOpenTime > 5:
                        robloxScreen = mssScreenshot(self.robloxWindow.mx, self.robloxWindow.my, self.robloxWindow.mw/2, self.robloxWindow.mh/2.5)
                        robloxScreenText = '\n'.join([x[1][0].lower() for x in ocr.ocrRead(robloxScreen)])
                        if "connect" in robloxScreenText:
                            print(robloxScreenText)
                            self.logger.webhook("","Roblox Home Page is open","brown","screen")
                            rejoinSuccess = False
                            break

                    self.setRobloxWindowInfo(setYOffset=False)

            appManager.openApp("Roblox")
            if not rejoinSuccess:
                continue
            #run fullscreen check
            # if self.isFullScreen(): #check if roblox can be found in menu bar
            #     self.logger.webhook("","Roblox is already in fullscreen, not activating fullscreen", "dark brown")
            # else:
            #     self.logger.webhook("","Roblox is not in fullscreen, activating fullscreen", "dark brown")
            #     self.toggleFullScreen()

            #if use browser to rejoin, close the browser
            if self.setdat["rejoin_method"] != "deeplink":
                time.sleep(2)
                webbrowser.open("https://docs.python.org/3/library/webbrowser.html", autoraise=True)
                time.sleep(0.5)
                for _ in range(2):
                    if sys.platform == "darwin":
                        self.keyboard.keyDown("command")
                    else:
                        self.keyboard.keyDown("ctrl")
                    self.keyboard.press("w")
                    if sys.platform == "darwin":
                        self.keyboard.keyUp("command")
                    else:
                        self.keyboard.keyUp("ctrl")
                    time.sleep(0.5)
                appManager.openApp("Roblox")
            
            self.startDetect()
            #find hive
            time.sleep(7) #wait for the joined friend popup to disappear
            mouse.click()
            # self.keyboard.press("space")
            # time.sleep(0.5)
            # self.keyboard.walk("w",5+(i*0.5),0)
            # self.keyboard.walk("s",0.3,0)
            # self.keyboard.walk("d",5,0)
            # self.keyboard.walk("s",0.3,0)
            hiveNumber = self.setdat["hive_number"]
            rejoinSuccess = False
            availableSlots = [] #store hive slots that are claimable
            newHiveNumber = 0
        
            # self.keyboard.keyDown("d", False)
            # self.keyboard.tileWait(4)
            # self.keyboard.keyDown("w", False)
            # self.keyboard.tileWait(20)
            # self.keyboard.keyUp("d", False)
            # self.keyboard.keyUp("w", False)
            self.setRobloxWindowInfo()
            self.keyboard.keyDown("d", False)
            self.keyboard.timeWaitNoHasteCompensation(0.548)
            self.keyboard.keyDown("w", False)
            self.keyboard.timeWaitNoHasteCompensation(2.9)
            self.keyboard.keyUp("d", False)
            self.keyboard.keyUp("w", False)
            for _ in range(3):
                time.sleep(0.4)
                if self.isBesideE(["claim", "hive", "send", "trad", "has"]):
                    break
                self.keyboard.walk("w", 0.1)

            def isHiveAvailable():
                return self.isBesideE(["claim", "hive"], ["send", "trade"], log=True)

            #go to the selected hive. Note down any available hives on the way
            self.logger.webhook("",f'Claiming hive {hiveNumber}', "dark brown")
            for j in range(1, hiveNumber+1):
                if j > 1:
                    #self.keyboard.tileWalk("a", 9.2)
                    self.keyboard.walk("a", self.hiveDistance)
                time.sleep(0.4)
                if isHiveAvailable():
                    availableSlots.append(j)
            
            #selected hive claimed
            if hiveNumber in availableSlots:
                newHiveNumber = hiveNumber
                rejoinSuccess = True
            
            else:
                self.logger.webhook("",f'Hive {hiveNumber} is already claimed, finding new hive','dark brown', "screen")
                #backtrack and claim the hive closest to cannon
                if availableSlots:
                    targetSlot = min(availableSlots)
                    #self.keyboard.tileWalk("d", 9.2*(hiveNumber - targetSlot))
                    self.keyboard.walk("d", self.hiveDistance*(hiveNumber - targetSlot))
                    time.sleep(0.4)
                    if isHiveAvailable():
                        newHiveNumber = targetSlot
                        rejoinSuccess = True

                #no available hive slots found previously, continue finding new ones ahead
                else:
                    for j in range(hiveNumber+1, 7):
                        self.keyboard.walk("a", self.hiveDistance)
                        time.sleep(0.4)
                        if isHiveAvailable():
                            newHiveNumber = j
                            rejoinSuccess = True
                            break

            # #find the hive in hive number
            # self.logger.webhook("",f'Claiming hive {hiveNumber} (guessing hive location)', "dark brown")
            # steps = round(hiveNumber*2.5) if hiveNumber != 1 else 0
            # for _ in range(steps):
            #     self.keyboard.walk("a",0.4, 0)

            # def findHive():
            #     self.keyboard.walk("a",0.4)
            #     #$time.sleep(0.15)
            #     if self.isBesideEImage("claimhive"):
            #         #check for overrun
            #         for _ in range(7):
            #             time.sleep(0.4)
            #             if self.isBesideEImage("claimhive"): break
            #             self.keyboard.walk("d",0.2)
            #         self.clickPermissionPopup()
            #         self.keyboard.press("e")
            #         return True
            #     return False
            
            # for _ in range(3):
            #     if findHive():
            #         self.logger.webhook("",f'Claimed hive {hiveNumber}', "bright green", "screen")
            #         rejoinSuccess = True
            #         break 
            # #find a new hive
            # else:
            #     self.logger.webhook("",f'Hive {hiveNumber} is already claimed, finding new hive','dark brown', "screen")
            #     #walk closer to the hives so the player wont walk up the ramp
            #     self.keyboard.walk("w",0.3,0)
            #     self.keyboard.walk("d",0.9*(hiveNumber)+2,0)
            #     self.keyboard.walk("s",0.3,0)
            #     for j in range(40):

            #         if findHive():
            #             guessedSlot = max(1,min(6, round(j//2.5)))
            #             hiveClaim = guessedSlot
            #             #if 3 < guessedSlot < 6:
            #                 #hiveClaim += 1
            #             self.logger.webhook("",f"Claimed hive {hiveClaim}", "bright green", "screen")
            #             rejoinSuccess = True
            #             self.setdat["hive_number"] = hiveClaim
            #             break
            #claim hive and convert
            if rejoinSuccess and isHiveAvailable():
                self.clickPermissionPopup()
                self.keyboard.press("e")
                time.sleep(1)
                self.logger.webhook("",f'Claimed hive {newHiveNumber}', "bright green", "screen", ping_category="ping_critical_errors")
                self.setdat["hive_number"] = newHiveNumber
                settingsManager.saveGeneralSetting("hive_number", newHiveNumber)
                for _ in range(8):
                    self.keyboard.press("o")
                self.moveMouseToDefault()
                time.sleep(1)
                #say existance so broke
                if self.setdat["existance_broke"]:
                    self.keyboard.press("/")
                    self.keyboard.write(f'Existance so broke :weary: {datetime.now().strftime("%H:%M")}', 0.1)
                    self.keyboard.press("enter")
                self.convert()
                #no need to reset
                self.canDetectNight = True
                self.status.value = ""
                return
            self.logger.webhook("",f'Rejoin unsuccessful, attempt {i+2}','dark brown', "screen")
        self.status.value = ""
    
    def blueTextImageSearch(self, text, threshold=0.7):
        target = self.adjustImage("./images/blue", text)
        return locateImageOnScreen(target, self.robloxWindow.mx+(self.robloxWindow.mw*3/4), self.robloxWindow.my+(self.robloxWindow.mh*3/5), self.robloxWindow.mw/4, self.robloxWindow.mh-self.robloxWindow.mh*3/5, threshold)
    #background thread for gather
    #check if mobs have been killed and reset their timings
    #check if player died

    def gatherBackgroundOnce(self, field):
        #death check
        st = time.time()
        if self.blueTextImageSearch("died", 0.8):
            self.died = True

    def gatherBackground(self):
        field = self.status.value.split("_")[1]
        while self.isGathering:
            self.gatherBackgroundOnce(field)
            time.sleep(1)

    #use the accurate sleep and sleep for ms
    def sleepMSMove(self, key, time):
        self.keyboard.keyDown(key, False)
        sleep(time/1000)
        self.keyboard.keyUp(key, False)

    def convertSecsToMinsAndSecs(self, n):
        m = n // 60
        s = n % 60
        return f"{int(m)}m {int(s):02d}s"
    
    def gather(self, field, settingsOverride = {}, questGumdrops=False):
        # Normalize field name to handle both space and underscore formats
        # Convert underscores to spaces for fieldSettings lookup
        normalized_field = field.replace('_', ' ')
        fieldSetting = {**self.fieldSettings[normalized_field], **settingsOverride}
        for i in range(3):
            self.waitForBees()
            #go to field
            self.cannon()
            self.logger.webhook("",f"Travelling: {field.title()}, Attempt {i+1}", "dark brown")
            self.goToField(field)
            #go to start location (match natro's)
            startLocation = fieldSetting["start_location"]
            moveSpeedFactor = 18/self.setdat["movespeed"]
            flen, fwid = [x*fieldSetting["distance"]/10 for x in startLocationDimensions[normalized_field]]
            if "upper" in startLocation or "top" in startLocation:
                self.sleepMSMove("w", flen*moveSpeedFactor)
            elif "lower" in startLocation or "bottom" in startLocation:
                 self.sleepMSMove("s", flen*moveSpeedFactor)

            if "left" in startLocation:
                 self.sleepMSMove("a", fwid*moveSpeedFactor)
            elif "right" in startLocation:
                 self.sleepMSMove("d", fwid*moveSpeedFactor)

            time.sleep(0.4)
            #place sprinkler + check if in field
            if self.placeSprinkler(): 
                break
            self.logger.webhook("", f"Failed to land in field", "red", "screen", ping_category="ping_critical_errors")
            self.reset()
        else: #failed too many times
            return
        #rotate camera
        if fieldSetting["turn"] == "left":
            for _ in range(fieldSetting["turn_times"]):
                self.keyboard.press(",")
        elif fieldSetting["turn"] == "right":
            for _ in range(fieldSetting["turn_times"]):
                self.keyboard.press(".")
        #key variables
        #check invert L/R and invert B/R
        fwdkey = "w"
        leftkey = "a" 
        backkey = "s" 
        rightkey = "d"
        rotleft = ","
        rotright = "."
        rotup = "pageup"
        rotdown = "pagedown"
        zoomin = "i"
        zoomout = "o"
        sc_space = "space"
        tcfbkey = fwdkey
        afcfbkey = backkey
        tclrkey = leftkey
        afclrkey = rightkey
        if fieldSetting["invert_lr"]:
            tclrkey = rightkey
            afclrkey = leftkey
        if fieldSetting["invert_fb"]:
            tcfbkey = backkey
            afcfbkey = fwdkey
        facingcorner = 0
        sizeData = {
            "xs": 0.25,
            "s": 0.5,
            "m": 1,
            "l": 1.5,
            "xl": 2
        }
        sizeword = fieldSetting["size"]
        size = sizeData[sizeword]
        width = fieldSetting["width"]
        maxGatherTime = fieldSetting["mins"]*60
        gatherTimeLimit = self.convertSecsToMinsAndSecs(maxGatherTime)
        returnType = fieldSetting["return"]
        pattern = fieldSetting['shape']
        st = time.time()
        keepGathering = True
        self.died = False
        #time to gather
        gatherNameSpace = {**locals(), **globals()}
        self.status.value = f"gather_{field}"
        self.isGathering = True
        firstPattern = True
        lastGooTime = 0  # Track when goo was last used
        gooTimerActive = True  # Flag to control goo timer thread
        
        # Add goo status to webhook message
        gooStatus = " - Goo Enabled" if fieldSetting["goo"] else ""
        self.logger.webhook(f"Gathering: {field.title()}", f"Limit: {gatherTimeLimit} - {fieldSetting['shape']} - Backpack: {fieldSetting['backpack']}%{gooStatus}", "light green")
        
        # Start goo timer thread
        import threading
        def gooTimerThread():
            nonlocal lastGooTime, gooTimerActive
            while gooTimerActive:
                currentTime = time.time()
                gooInterval = int(fieldSetting["goo_interval"])
                if fieldSetting["goo"] and (currentTime - lastGooTime) >= gooInterval:
                    self.keyboard.press(str(self.setdat["goo_slot"]))
                    time.sleep(0.05)
                    lastGooTime = currentTime
                time.sleep(0.5)  # Check every 0.5 seconds
        
        gooTimerThread = threading.Thread(target=gooTimerThread, daemon=True)
        gooTimerThread.start()
        mouse.moveBy(10,5)
        self.keyboard.releaseMovement()

        def getGatherTime():
            return time.time() - st
        
        def stopGather():
            nonlocal gooTimerActive
            gooTimerActive = False  # Stop the goo timer thread
            if fieldSetting["shift_lock"]: 
                self.keyboard.press('shift')
            self.moveMouseToDefault()
            self.status.value = ""
            self.isGathering = False
            if "onGatherEnd" in gatherNameSpace and callable(gatherNameSpace["onGatherEnd"]):
                gatherNameSpace["onGatherEnd"]()

        if fieldSetting["shift_lock"]: 
            self.keyboard.press('shift')
        
        while keepGathering:
            # Check if paused and wait
            if self.checkPauseAndWait():
                # Stop was requested while paused
                stopGather()
                return
            
            # Check if skip was requested
            if self.skipTask is not None and self.skipTask.value == 1:
                self.skipTask.value = 0  # Reset skip flag
                stopGather()
                self.logger.webhook("Task Skipped", f"Skipped gathering in {field.title()}", "orange")
                self.reset(convert=False)
                return
            
            #goo timer is now handled by background thread

            patternStartTime = time.time()
            mouse.mouseDown()

            #quest gumdrops
            if questGumdrops:
                for _ in range(2):
                    self.keyboard.press(str(self.setdat["quest_gumdrop_slot"]))
                    time.sleep(0.05)

            #ensure that the pattern works
            try:
                exec(open(f"../settings/patterns/{pattern}.py").read(), gatherNameSpace)
            except Exception as e:
                print(traceback.format_exc())
                if firstPattern:
                    self.logger.webhook("Incompatible pattern", f"The pattern {pattern} is incompatible with the macro. Defaulting to e_lol instead.\
                                        Avoid using this pattern in the future. If you are the creator of this pattern, the error can be found in terminal", "red")
                    pattern = "e_lol"
            firstPattern = False

            #mob respawn check
            self.setMobTimer(field)

            #field drift compensation
            if fieldSetting["field_drift_compensation"]:
                self.fieldDriftCompensation.run()

            #cycle ends
            mouse.mouseUp()
            self.clickPermissionPopup()
            #add gather time stat
            self.hourlyReport.addHourlyStat("gathering_time", time.time()-patternStartTime)
            gatherTime = self.convertSecsToMinsAndSecs(getGatherTime())

            #check for AFB
            if self.setdat["Auto_Field_Boost"] and not self.AFBLIMIT and self.AFB(gatherInterrupt=True, turnOffShiftLock = fieldSetting["shift_lock"]):
                return
            #check for gather interrupts
            elif self.night and self.setdat["stinger_hunt"]:
                #rely on task function in main to execute the stinger hunt
                stopGather()
                self.logger.webhook("Gathering: interrupted","Stinger Hunt","dark brown")
                self.reset(convert=False)
                break
            elif self.setdat["mondo_buff"] and self.hasMondoRespawned() and self.setdat["mondo_buff_interrupt_gathering"]:
                stopGather()
                self.logger.webhook("Gathering: interrupted","Mondo Buff","dark brown")
                self.reset(convert=False)
                self.collectMondoBuff()
                break
            elif self.died:
                self.status.value = ""
                stopGather()
                self.logger.webhook("","Player died", "dark brown","screen", ping_category="ping_character_deaths")
                time.sleep(0.4)
                self.reset()
                break
            elif getGatherTime() > maxGatherTime:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Time Limit - Return: {returnType.title()}", "light green", "screen")
                keepGathering = False
            #check backpack
            elif self.getBackpack() >= fieldSetting["backpack"]:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Backpack - Return: {returnType.title()}", "light green", "screen")
                keepGathering = False

        #gathering was interrupted
        if keepGathering:
            return
        else:
            stopGather()

        #goo timer continues via background thread during return process

        #go back to hive
        def walkToHive():
            nonlocal self
            #walk to hive
            #face correct direction (towards hive)
            if fieldSetting["turn"] == "left":
                for _ in range(fieldSetting["turn_times"]):
                    self.keyboard.press(".")
            elif fieldSetting["turn"] == "right":
                for _ in range(fieldSetting["turn_times"]):
                    self.keyboard.press(",")
            self.faceDirection(field, "south")
            #start walk
            self.canDetectNight = False
            self.logger.webhook("",f"Walking back to hive: {field.title()}", "dark brown")
            self.runPath(f"field_to_hive/{field}")
            #find hive and convert
            #self.keyboard.walk("a", (self.setdat["hive_number"]-1)*0.8)
            self.keyboard.keyDown("a")
            st = time.time()
            self.canDetectNight = True
            while time.time()-st < 10:
                #goo timer continues via background thread during hive search
                if self.isBesideEImage("makehoney"):
                    break
            self.keyboard.keyUp("a")
            #in case we overrun
            time.sleep(0.4)
            for _ in range(7):
                #goo timer continues via background thread during conversion attempts
                if self.convert():
                    break
                self.keyboard.walk("d",0.1)
                time.sleep(0.2) #add a delay so that the E can popup
            else:
                self.logger.webhook("","Can't find hive, resetting", "dark brown", "screen")
                self.reset()

        if returnType == "reset":
            #goo timer continues via background thread during reset
            self.reset()
        elif returnType == "rejoin":
            #goo timer continues via background thread during rejoin
            self.rejoin()
        elif returnType == "whirligig":
            #goo timer continues via background thread during whirligig usage
            self.useItemInInventory("whirligig")
            time.sleep(1)
            if not self.convert():
                self.logger.webhook("","Whirligigs failed, walking to hive", "dark brown", "screen")
                walkToHive()
                return
            #whirligig sucessful
            #goo timer continues via background thread after whirligig success
            self.reset(convert=False)
        elif returnType == "walk":
            #goo timer continues via background thread during walk to hive
            walkToHive()
        
        # Stop the goo timer thread when gathering is completely finished
        gooTimerActive = False

    #returns the coordinates of the keep old text
    def keepOldCheck(self):
        noImg = self.adjustImage("./images/menu", "keep") #yes/no popup
        x = self.robloxWindow.mx + self.robloxWindow.mw/2-300
        y = self.robloxWindow.my
        res = locateImageOnScreen(noImg, x, y, 650, self.robloxWindow.mh, 0.8)
        if res:
            ix, iy = [j//self.robloxWindow.multi for j in res[1]]
            return x+ix+5, y+iy+5
        # region = (self.ww/3.15,self.wh/2.15,self.ww/2.7,self.wh/4.2)
        # res = ocr.customOCR(*region,0)
        # for i in res:
        #     if "keep" in i[1][0].lower() and "o" in i[1][0].lower():
        #         return ((i[0][0][0]+region[0])//self.robloxWindow.multi, (i[0][0][1]+region[1])//self.robloxWindow.multi)
        

    def antChallenge(self):
        self.logger.webhook("","Travelling: Ant Challenge","dark brown")
        left = 15 / self.setdat["hive_number"]
        self.keyboard.walk("w", 1, False)
        self.keyboard.walk("a", left, False)
        self.keyboard.keyDown("w")
        time.sleep(2)
        self.keyboard.press("space")
        time.sleep(3.5)
        self.keyboard.keyUp("w")
        self.keyboard.walk("a", 0.45, False)
        self.keyboard.keyDown("w")
        self.keyboard.press("space")
        time.sleep(1.5)
        self.keyboard.press("space")
        time.sleep(3)
        self.keyboard.keyUp("w")
        self.keyboard.walk("a", 2.5, False)
        self.keyboard.keyDown("w")
        time.sleep(6)
        self.keyboard.keyUp("w")
        self.keyboard.walk("s", 0.4)
        time.sleep(0.5)

        if self.isBesideE(["spen","play"], ["need"]):
            self.logger.webhook("","Start Ant Challenge","bright green", "screen")
            self.keyboard.press("e")
            time.sleep(1)
            self.placeSprinkler()
            mouse.click()
            time.sleep(1)
            self.keyboard.walk("s",1.5)
            self.keyboard.walk("w",0.15)
            self.keyboard.walk("d",0.3)
            mouse.mouseDown()
            while True:
                keepOld = self.keepOldCheck()
                if keepOld is not None:
                    mouse.mouseUp()
                    self.logger.webhook("","Ant Challenge Complete","bright green", "screen", ping_category="ping_ant_challenge")
                    time.sleep(0.1)
                    mouse.moveTo(*keepOld)
                    time.sleep(0.2)
                    mouse.click()
                    break
            return
        self.logger.webhook("", "Cant start ant challenge", "red", "screen", ping_category="ping_critical_errors")

    def getCurrentMinute(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        _,m,_ = [int(x) for x in current_time.split(":")]
        return m
    
    def hasMondoRespawned(self):
        #check if mondo can be collected (first 10mins)
        minute = self.getCurrentMinute()
        #set respawn time to 20mins
        #mostly just to prevent the macro from going to mondo over and over again for the 10mins
        return minute <= 10 and self.hasRespawned("mondo", 20*60)

    def collectMondoBuff(self, gatherInterrupt = False):
        self.status.value = ""
        st = time.perf_counter()
        self.logger.webhook("","Travelling: Mondo Buff","dark brown")
        #go to mondo buff
        self.cannon()
        self.keyboard.press("e")
        sleep(2.5)
        self.logger.webhook("","Collecting: Mondo Buff","yellow", "screen")
        self.keyboard.walk("w",1)
        self.keyboard.walk("d",3) 
        if self.setdat["mondo_buff_loot"]: # If looting is enabled, wait until mondo is defeated
            self.logger.webhook("", "Waiting for Mondo to be defeated", "light green")
            self.keyboard.press("shift") #moves slightly up (or down) when hitting wall, so this reduces that
            while True:
                #defeat
                if self.blueTextImageSearch("defeated") and self.blueTextImageSearch("mondo"): 
                    self.saveTiming("mondo") 
                    break
                #died
                if self.blueTextImageSearch("died"):
                    self.died = True
                    self.keyboard.press("shift")
                    self.logger.webhook("", "Player Died", "red", "screen", ping_category="ping_character_deaths")
                    self.reset(convert=False)
                    #sev recursion here is pretty weird
                    #TODO: not make it recursive
                    self.collectMondoBuff()
                    return
                #time limit
                if self.getCurrentMinute() >= 15: #mondo despawns after 15 minutes if not defeated in time
                    self.keyboard.walk("s",1, False)
                    self.keyboard.press(",")
                    time.sleep(0.5)
                    self.logger.webhook("", "Time Limit (15 minutes)\n Mondo may have despawned. Resetting", "light green", "screen")
                    self.keyboard.press("shift")
                    self.saveTiming("mondo") 
                    self.reset(convert=True)
                    return False
                #collect tokens by bees
                if self.setdat["mondo_collect_token"]: 
                    self.keyboard.walk("a", 0.45)
                    for slowmove in range(9):
                        self.keyboard.walk("d", 0.048, False) #move JUST EVER SO SLIGHTLY, maybe bumps in to wall less
                        time.sleep(0.035)
                mouse.click()
                time.sleep(1.5)

            #loot
            mondo_loot_times = self.setdat["mondo_loot_times"] #how many loops based on what the user inputted
            time.sleep(0.1)
            self.keyboard.walk("d",1,False)
            time.sleep(0.1)
            self.keyboard.press("shift")
            self.keyboard.walk("s",3.15,False)
            self.logger.webhook("", "Looting: Mondo Chick", "yellow", "screen")
            if mondo_loot_times == 1:
                self.logger.webhook("", "Looping 1 time", "light green")
            else:
                self.logger.webhook("", f"Looping {mondo_loot_times} times", "light green")
            self.keyboard.walk("a",3.55)
            for loops in range(mondo_loot_times): 
                for looting in range(6):
                    self.keyboard.walk("w",0.20)
                    self.keyboard.walk("d",2.65)
                    self.keyboard.walk("w",0.20)
                    self.keyboard.walk("a",2.65)
                for looting in range(6):
                    self.keyboard.walk("s",0.20)
                    self.keyboard.walk("d",2.65)
                    self.keyboard.walk("s",0.20)
                    self.keyboard.walk("a",2.65)
        else: #if loot off, just idle
            end_time = time.perf_counter() + self.setdat["mondo_buff_wait"] * 60  
            self.logger.webhook("", f"Collecting for: {self.setdat['mondo_buff_wait']} minutes", "yellow")
            # if collecting tokens produced by bees
            if self.setdat["mondo_collect_token"]:
                # enable shiftlock
                self.keyboard.press("shift")
                while time.perf_counter() < end_time: 
                    self.keyboard.walk("a", 0.45)
                    for slowmove in range(9):
                        self.keyboard.walk("d", 0.048, False) #move JUST EVER SO SLIGHTLY, maybe bumps in to wall less
                        time.sleep(0.035) 
                    time.sleep(3) #longer since we are not detecting anything
            else:
                time.sleep(self.setdat['mondo_buff_wait'] * 60)
            self.saveTiming("mondo") 
            self.logger.webhook("","Collected: Mondo Buff","light green", ping_category="ping_mondo_buff")
        #done
        self.reset(convert=True)
        return True

    def collectStickerPrinter(self):
        reached = False
        for _ in range(2):
            self.logger.webhook("",f"Travelling: Sticker Printer","dark brown")
            self.cannon()
            self.runPath("collect/sticker_printer")
            for _ in range(6):
                self.keyboard.walk("w", 0.2)
                reached = self.isBesideE(["inspect", "stick", "print"])
                if reached: break
            if reached: break
            self.logger.webhook("", f"Failed to reach sticker printer", "dark brown", "screen")
            self.reset(convert=False)
        else: return

        self.keyboard.press("e")
        #claim sticker
        eggPosData = {
            "basic": -95, 
            "silver": -40,
            "gold": 15,
            "diamond": 70,
            "mythic": 125
        }
        #click egg
        time.sleep(2)
        eggPos = eggPosData[self.setdat["sticker_printer_egg"]]
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw//2+eggPos), self.robloxWindow.my+(4*self.robloxWindow.mh//10-20))
        time.sleep(0.2)
        mouse.click()
        time.sleep(1)
        confirmImg = self.adjustImage("./images/menu", "confirm")
        if not locateImageOnScreen(confirmImg, self.robloxWindow.mx+(self.robloxWindow.mw//2+150), self.robloxWindow.my+(4*self.robloxWindow.mh//10+160), 120, 60, 0.7):
            self.logger.webhook(f"", "Sticker printer on cooldown", "dark brown", "screen")
            self.keyboard.press("e")
            self.saveTiming("sticker_printer")
            return
        #confirm
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw//2+225), self.robloxWindow.my+(4*self.robloxWindow.mh//10+195))
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.2)
        mouse.moveBy(0, 3)
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.2)
        #click yes
        if not self.clickYes(detect=True):
            egg = self.setdat["sticker_printer_egg"]
            self.logger.webhook("", f"No {egg} eggs left, Sticker Printer has been disabled", "red", "screen", ping_category="ping_critical_errors")
            self.updateGUI.value = 1
            self.setdat["sticker_printer"] = False
            settingsManager.saveProfileSetting(f"sticker_printer", False)
            self.keyboard.press("e")
            return
        #wait for sticker to generate
        time.sleep(7)
        self.logger.webhook(f"", "Claimed sticker", "bright green", "sticker", ping_category="ping_sticker_events")
        self.saveTiming("sticker_printer")
        #close the inventory
        time.sleep(1)
        self.toggleInventory("close")

    #convert bss' cooldown text into seconds
    #brackets: account for brackets in the text, where the cooldown value is between said brackets
    def cdTextToSecs(self, rawText, brackets, defaultTime=0):
        if brackets:
            closePos = rawText.rfind(")")
            #get cooldown if close bracket is present or not
            if closePos >= 0:
                cooldownRaw = rawText[rawText.rfind("(")+1:closePos]
            elif "(" in rawText:
                cooldownRaw = rawText.split("(")[1]
            else:
                cooldownRaw = rawText
        else:
            cooldownRaw = rawText
        #clean it up, extract only valid characters
        cooldownRaw = ''.join([x for x in cooldownRaw if x.isdigit() or x == ":" or x == "s"])
        cooldownSeconds = None #cooldown in seconds

        def extractNumFromText(text):
            return ''.join(filter(str.isdigit, text))
        
        #convert time to seconds
        validTime = True
        if ":" in cooldownRaw:
            times = cooldownRaw.split(":")
            cooldownSeconds = 0
            #convert
            for i,e in enumerate(times[::-1]):
                num = extractNumFromText(e)
                if not num:
                    validTime = False
                    break
                cooldownSeconds += int(num) * 60**i

        elif cooldownRaw.count("s") == 1: #only seconds
            num = extractNumFromText(e)
            if not num:
                validTime = False
            cooldownSeconds = num
        else:
            validTime = False
        
        if not validTime or (defaultTime and cooldownSeconds > defaultTime):
            cooldownSeconds = defaultTime

        return cooldownSeconds
    
    def collect(self, objective):
        reached = None
        objectiveData = mergedCollectData[objective]
        displayName = objective.replace("_"," ").title()
        self.location = "collect"
        st = time.time()
        def updateHourlyTime():
            self.hourlyReport.addHourlyStat("misc_time", time.time()-st)
        #go to collect and check that player has reached
        for i in range(3):
            self.logger.webhook("",f"Travelling: {displayName}","dark brown")
            self.cannon()
            self.runPath(f"collect/{objective}")
            if objectiveData[1] is None:
                reached = self.isBesideE(objectiveData[0])
            else:
                for _ in range(6):
                    self.keyboard.walk(objectiveData[1], 0.2)
                    reached = self.isBesideE(objectiveData[0])
                    if reached: break
            if reached: break
            self.logger.webhook("", f"Failed to reach {displayName}", "dark brown", "screen")
            if objective == "ant_pass_dispenser":
                self.logger.webhook("", "Maybe you have maxed out ant passes?", "dark brown")
            if i != 2: self.reset(convert=False)
        
        if not reached: 
            updateHourlyTime()
            return #player failed to reach objective
        #player has reached, get cooldown info
        #check if on cooldown
        cooldownSeconds = objectiveData[2]
        returnVal = None #a return value
        if "(" and ":" in reached:
            cd = self.cdTextToSecs(reached, True, self.collectCooldowns[objective])
            if cd: cooldownSeconds = cd
            cooldownFormat = timedelta(seconds=cooldownSeconds)
            self.logger.webhook("", f"{displayName} is on cooldown ({cooldownFormat} remaining)", "dark brown", "screen")
        else: #not on cooldown
            for _ in range(1 if objective == "sticker_stack" else 2):
                self.keyboard.press("e")
            #run the claim path (if it exists)
            self.runPath(f"collect/claim/{objective}", fileMustExist=False)
            #memory match
            if "memory_match" in objective:
                if objective == "memory_match":
                    mmType = "normal"
                else:
                    mmType = objective.split("_")[0]
                self.latestMM = mmType
                time.sleep(2)
                self.logger.webhook("", f"Solving: {displayName}", "dark brown", "screen")
                self.canDetectNight = False
                self.memoryMatch.solveMemoryMatch(mmType)
                self.canDetectNight = True
                time.sleep(2)
                self.logger.webhook("", f"Completed: {displayName}", "bright green", "blue")
            elif objective in fieldBoosterData:
                sleep(3)
                bluetexts = ""
                #get the blue texts 4 times to avoid missing the field
                for _ in range(4):
                    bluetexts += ocr.imToString("blue").lower()
                #find which field is in blue texts
                #note: fields is set in the collect path of the boosters
                boostedField = ""
                for f in fields:
                    sub_name = f.split(" ")
                    for sn in sub_name:
                        if sn in bluetexts:
                            boostedField = f
                            break
                    if boostedField: break
                returnVal = boostedField
                self.logger.webhook("", f"Collected: {displayName}, Boosted Field: {boostedField.title()}", "bright green", "screen")
                self.saveTiming("last_booster")
            elif objective == "sticker_stack":
                if "your" in reached or "activated" in reached:
                    self.logger.webhook("", "Sticker Stack on cooldown", "dark brown", "screen")
                    return
                self.claimStickerStack()
            else:
                time.sleep(0.1)
                self.logger.webhook("", f"Collected: {displayName}", "bright green", "screen")
        #update the internal cooldown
        self.saveTiming(objective)
        self.collectCooldowns[objective] = cooldownSeconds
        updateHourlyTime()
        return returnVal

    #accept mob and field and return them in the format used for timings.txt file
    #mob_field, eg ladybug_strawberry
    #werewolf is an exception, just return "werewolf"
    def formatMobTimingName(self, mob, field):
        if mob == "werewolf": return mob
        return f"{mob}_{field}"
    
    def hasMobRespawned(self, mob, field, timing = None):
        return self.hasRespawned(self.formatMobTimingName(mob, field), mobRespawnTimes[mob], True, timing)
    
    #to be used by the mob run walk paths
    #returns true if there are mobs in the field to be killed (enabled + respawned)
    #returns a list of mobs that have respawned
    def getRespawnedMobs(self, field):
        mobs = regularMobTypesInFields[field]
        out = []
        for m in mobs:
            if self.setdat[m] and self.hasMobRespawned(m, field):
                out.append(m)
        return out
    
    #check which mobs have respawned in the field and reset their timings
    def setMobTimer(self, field):
        if not field in regularMobTypesInFields: return
        timings = self.getTiming()
        mobs = regularMobTypesInFields[field]
        for m in mobs:
            timingName = self.formatMobTimingName(m, field)
            if not timingName in timings:
                continue
            #check respawn
            if self.hasMobRespawned(m, field, timings[timingName]):
                timings[timingName] = time.time()
                self.hourlyReport.addHourlyStat("bugs", regularMobQuantitiesInFields[field][m])
        settingsManager.saveDict("./data/user/timings.txt", timings)

    #background thread function to determine if player has defeated the mob
    #time limit of 20s
    def mobRunAttackingBackground(self):
        st = time.time()
        if self.setdat["bees"] > 40:
            timeout = 20
        elif self.setdat["bees"] > 30:
            timeout = 30
        else:
            timeout = 40

        while True:
            if self.blueTextImageSearch("died"):
                self.mobRunStatus = "dead"
                break
            elif self.blueTextImageSearch("defeated"):
                self.mobRunStatus = "looting"
                break
            elif time.time() - st > timeout:
                self.mobRunStatus = "timeout"
                break
    #background thread to check if token link is collected or the macro runs out of time (max 15s)
    def mobRunLootingBackground(self):
        st = time.time()
        while time.time() - st < 20:
           if self.blueTextImageSearch("tokenlink", 0.8):
            time.sleep(0.5) 
            self.logger.webhook("","Collected Token Link", "white", "blue")
            break
        self.mobRunStatus = "done"

    def killMob(self, mob, field, walkPath = None):
        mobName = mob
        if mob == "rhinobeetle": mobName = "rhino beetle"
        self.status.value = "bugrun"
        self.logger.webhook("","{}: {} ({})".format("Travelling" if walkPath is None else "Walking", mobName.title(),field.title()),"dark brown")
        self.mobRunStatus = "attacking"
        attackThread = threading.Thread(target=self.mobRunAttackingBackground)
        attackThread.daemon = True
        if walkPath is None:
            self.waitForBees()
            self.cannon()
            self.goToField(field, "north")
            #attack the mob
            attackThread.start()
        else:
            #attack the mob
            #attack thread will start in the path
            self.canDetectNight = False
            exec(walkPath)
            self.canDetectNight = True
        self.location = field
        self.logger.webhook("","Attacking: {} ({})".format(mobName.title(),field.title()),"dark brown")
        
        st = time.time()
        def updateHourlyTime():
            self.hourlyReport.addHourlyStat("bug_run_time", time.time()-st)
        #move in squares to evade attacks
        #save the last entered side and front keys. This will be used for the looting pattern
        distance = 0.7
        lastSideKey = "d"
        lastFrontKey = "s"
        def dodgeWalk(k,t):
            nonlocal lastSideKey, lastFrontKey
            if k in ["w", "s"]: lastFrontKey = k
            elif k in ["a","d"]: lastSideKey = k
            self.keyboard.walk(k, t)
        while True:
            # Check if paused and wait
            if self.checkPauseAndWait():
                # Stop was requested while paused
                self.mobRunStatus = "done"
                break
            dodgeWalk("s", distance*1.2)
            if self.mobRunStatus != "attacking": break
            dodgeWalk("a", distance*1.8)
            if self.mobRunStatus != "attacking": break
            dodgeWalk("w", distance*1.2)
            if self.mobRunStatus != "attacking": break
            dodgeWalk("d", distance*1.8)
            if self.mobRunStatus != "attacking": break

        attackThread.join()
        if self.mobRunStatus == "dead":
            self.logger.webhook("","Player died", "dark brown","screen", ping_category="ping_character_deaths")
            updateHourlyTime()
            return
        elif self.mobRunStatus == "timeout":
            self.setMobTimer(field)
            self.logger.webhook("","Could not kill {} in time. Maybe it hasn't respawned?".format(mobName.title()), "dark brown", "screen")
            updateHourlyTime()
            return
        time.sleep(1.5)
        #loot
        self.logger.webhook("", "Looting: {}".format(mobName.title()), "bright green", "screen")
        #start another background thread to check for token link/time limit
        lootThread = threading.Thread(target=self.mobRunLootingBackground)
        lootThread.daemon = True
        lootThread.start()
        def lootPattern(f, s):
            if lastSideKey == "a":
                startSideKey = "d"
            elif lastSideKey == "d":
                startSideKey = "a"

            if lastFrontKey == "w":
                startFrontKey = "s"
            elif lastFrontKey == "s":
                startFrontKey = "w"

            while True:
                # Check if paused and wait
                if self.checkPauseAndWait():
                    return  # Stop was requested
                for _ in range(2):
                    self.keyboard.walk(startFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(startSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(startSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
                for _ in range(2):
                    self.keyboard.walk(startFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
        lootPattern(1.35, 2.5)
        self.setMobTimer(field)
        self.status.value = ""
        lootThread.join()
        #check if there are paths for the macro to walk to other fields for mob runs
        #run a path in the field format
        updateHourlyTime()
        self.runPath(f"mob_runs/{field}", fileMustExist=False)

    def stingerHuntBackground(self):
        #find vic
        while not self.stopVic:
            #detect which field the vic is in
            if self.vicField is None:
                for field in self.vicFields:
                    if self.blueTextImageSearch(f"vic{field}", 0.75):
                        self.vicField = field
                        break
            else:
                if self.blueTextImageSearch("died"): self.died = True
            
            if self.blueTextImageSearch("vicdefeat"):
                self.vicStatus = "defeated"
                
    def stingerHunt(self):

        class VicStopPathException(Exception):
            pass

        def vicSearchWalk(key, t):
            if self.vicField and currField != self.vicField:
                raise VicStopPathException()
            self.keyboard.walk(key, t)

        self.vicStatus = None
        self.vicField = None
        self.stopVic = False
        currField = None
        self.status.value = ""

        stingerHuntThread = threading.Thread(target=self.stingerHuntBackground)
        stingerHuntThread.daemon = True
        stingerHuntThread.start()
        vicStartTime = time.time()
        def updateHourlyTime():
            self.hourlyReport.addHourlyStat("bug_run_time", time.time()-vicStartTime)

        for currField in self.vicFields:
            #go to field
            self.cannon()
            self.logger.webhook("",f"Travelling to {currField} (stinger hunt)","dark brown")
            self.goToField(currField, "south")
            time.sleep(0.8)
            try:
                exec(open(f"../paths/vic/find_vic/{currField}.py").read())
            except VicStopPathException:
                pass
            if self.vicField:
                self.logger.webhook("",f"Vicious Bee detected ({self.vicField})", "light blue", "screen") 
                break
            print(self.vicField)
            self.reset(convert=False)
        else: #unable to find vic
            self.stopVic = True
            stingerHuntThread.join()
            self.convert()
            updateHourlyTime()
            self.night = False
            return
        
        #kill vic
        def goToVicField(wait=False):
            self.reset(convert=False)
            if wait:
                time.sleep(10)
            self.logger.webhook("",f"Travelling to {self.vicField} (vicious bee)","dark brown")
            self.cannon()
            self.goToField(self.vicField, "south")

        #first, check if vic is found in the same field as the player
        if currField != self.vicField: 
            goToVicField()
        
        #run the dodge pattern
        #similar to the search pattern, between each line of code, check if vic has been defeated/player died
        pathLines = open(f"../paths/vic/kill_vic/{self.vicField}.py").read().split("\n")
        loop = True
        self.died = False
        st = time.time() 
        while loop:
            # Check if paused and wait
            if self.checkPauseAndWait():
                # Stop was requested while paused
                self.night = False
                self.stopVic = True
                updateHourlyTime()
                return
            for code in pathLines:
                exec(code)
                #run checks
                if self.died or self.vicStatus is not None: break
            if self.vicStatus == "defeated":
                self.logger.webhook("","Vicious Bee Defeated","light green", "screen", ping_category="ping_vicious_bee")
                self.hourlyReport.addHourlyStat("vicious_bees", 1)
                break
            elif self.died:
                self.logger.webhook("","Player Died","dark brown", "screen", ping_category="ping_character_deaths")
                goToVicField(wait=True)
                self.died = False
            elif time.time()-st > 180: #max 3 mins to kill vic
                self.logger.webhook("","Took too long to kill Vicious Bee","red", "screen", ping_category="ping_critical_errors")
                break
        self.night = False
        updateHourlyTime()
        self.stopVic = True
        stingerHuntThread.join()
        self.reset()

    def stumpSnail(self):
        for _ in range(3):
            self.cannon()
            self.logger.webhook("","Travelling: Stump Snail", "dark brown")
            self.goToField("stump")
            if self.placeSprinkler():
                break
            self.logger.webhook("", "Failed to land in stump field", "red", "screen", ping_category="ping_critical_errors")
            self.reset()
        while True:
            # Check if paused and wait
            if self.checkPauseAndWait():
                # Stop was requested while paused
                return
            mouse.click()
            keepOldData = self.keepOldCheck()
            if keepOldData is not None:
                mouse.mouseUp()
                break
        #handle the other stump snail
        self.logger.webhook("","Stump Snail Killed","bright green", "screen", ping_category="ping_mob_events")
        self.saveTiming("stump_snail")
        def keepOld():
            time.sleep(0.5)
            mouse.moveTo(*keepOldData)
            mouse.click()

        def replace():
            replaceImg = self.adjustImage("./images/menu", "replace")
            x = self.robloxWindow.mx + self.robloxWindow.mw/2-300
            y = self.robloxWindow.my
            res = locateImageOnScreen(replaceImg, x, y, 650, self.robloxWindow.mh, 0.8)
            if res is not None:
                mouse.moveTo(*[j//self.robloxWindow.multi for j in res[1]])
                mouse.click()
        amulet = self.setdat["stump_snail_amulet"]
        if amulet == "keep":
            keepOld()
        elif amulet == "replace":
            replace()
        elif amulet == "stop":
            while self.keepOldCheck(): mouse.click()
        elif amulet == "wait for command":
            self.status.value = "amulet_wait"
            #wait for user to send command to bot
            while self.status.value == "amulet_wait": mouse.click()
            if self.status.value == "amulet_keep":
                keepOld()
            elif self.status.value == "amulet_replace":
                replace()

    #sleep in ms, useful for implementing ahk code
    def msSleep(self, t):
        if t <= 0: return
        time.sleep(t/1000)

    #implementation of natro's nm_loot function
    def nmLoot(self, length, reps, dirKey):
        for _ in range(reps):
            self.keyboard.tileWalk("w", length)
            self.keyboard.tileWalk(dirKey, 1.5)
            self.keyboard.tileWalk("s", length)
            self.keyboard.tileWalk(dirKey, 1.5)

    def coconutCrabBackground(self):
        while self.bossStatus is None:
            if self.blueTextImageSearch("died"):
                self.died = True
            if self.blueTextImageSearch("coconutcrab_defeat", 0.8):
                self.bossStatus = "defeated"
        

    def coconutCrab(self):
        self.bossStatus = None
        cocoThread = threading.Thread(target=self.coconutCrabBackground)
        cocoThread.daemon = True
        cocoThread.start()
        st = time.time()
        for _ in range(2):
            self.cannon()
            self.logger.webhook("","Travelling: Coconut Crab","dark brown")
            self.goToField("coconut")
            self.keyboard.walk("s", 1)
            self.keyboard.walk("d", 3)
            self.died = False
            self.bossStatus = None
            st = time.time()
            while True:
                mouse.mouseDown()
                #simplified version of natro's coco crab pattern
                for i in range(2):
                    self.keyboard.walk("a",6, False)
                    self.keyboard.walk("d",6-i*1.8, False)
                self.keyboard.walk("s",2)
                time.sleep(4.5)
                self.keyboard.walk("w",1)
                mouse.mouseUp()
                if time.time()-st > 900: #15min time limit
                    self.bossStatus = "timelimit"
                if self.died or self.bossStatus is not None: break
            
            if self.died:
                self.logger.webhook("", "Died to Coconut Crab", "dark brown", ping_category="ping_character_deaths")
                self.reset(convert=False)
                self.died = False
            elif self.bossStatus is not None:
                break
            
        if self.bossStatus == "timelimit":
            self.logger.webhook("", "Time Limit: Coconut Crab", "dark brown", ping_category="ping_critical_errors")
        elif self.bossStatus == "defeated":
            self.keyboard.walk("a", 2)
            self.logger.webhook("", "Defeated: Coconut Crab", "bright green", "screen", ping_category="ping_mob_events")
            self.nmLoot(9, 4, "d")
            self.nmLoot(9, 4, "a")
            self.nmLoot(9, 4, "d")
            self.nmLoot(9, 4, "a")
            self.nmLoot(9, 4, "d")
            self.nmLoot(9, 4, "a")
        cocoThread.join()
        self.hourlyReport.addHourlyStat("bug_run_time", time.time()-st)
        self.saveTiming("coconut_crab")
        self.reset()

    
    def goToPlanter(self, planter, field, method):
        global finalKey
        self.cannon()
        self.logger.webhook("", f"Travelling: {planter.title()} Planter ({field.title()}), {method.title()}", "dark brown")
        self.goToField(field, "north")
        #move from center of field to planter spot
        finalKey = None
        path = f"../paths/planters/{field}.py"
        if os.path.isfile(path): #not all fields have a planter path
            exec(open(path).read())
        #go to the planter
        if method == "collect": #return true if the planter can be found
            time.sleep(1)
            if finalKey is not None:
                st = time.time()
                while time.time()-st < (finalKey[1]+1):
                    self.keyboard.walk(finalKey[0],0.25)
                    if self.isBesideEImage("ebutton"): 
                        return True
            else:
                time.sleep(1)
                if self.isBesideEImage("ebutton"): 
                    return True
            #can't find it, try detecting and moving to it
            self.moveToPlanter()
            if self.isBesideE(["harvest", "planter"]):
                return True
            return False
                
        else: #place, just walk there
            if finalKey is not None: self.keyboard.walk(finalKey[0], finalKey[1])
            return True
    
    def findPlanterInInventory(self, name):
        for _ in range(2):
            res = self.findItemInInventory(f"{name}planter")
            if res:
                self.planterCoords = res
                return
            time.sleep(1)
            
    #place the planter and return true if successfully placed
    def placePlanter(self, planter, field, glitter):
        st = time.time()
        name = planter.lower().replace(" ","").replace("-","")

        def updateHourlyTime():
            self.hourlyReport.addHourlyStat("misc_time", time.time()-st)

        for _ in range(2):
            #try to place planter
            #start finding planter
            self.planterCoords = None
            findPlanterInventoryThread = threading.Thread(target=self.findPlanterInInventory, args=(name,))
            findPlanterInventoryThread.daemon = True
            findPlanterInventoryThread.start()

            self.goToPlanter(planter, field, "place")
            #wait for thread to finish
            findPlanterInventoryThread.join()
            #Couldn't find planter
            if self.planterCoords is None:
                updateHourlyTime()
                return 
            #place planter
            self.useItemInInventory(x=self.planterCoords[0], y=self.planterCoords[1])
            
            #check if planter is placed
            time.sleep(0.5)
            placedPlanter = True
            for _ in range(7):
                if self.blueTextImageSearch("notinfield") or self.blueTextImageSearch("maxplanters"):
                    placedPlanter = False
                    break
                time.sleep(0.3)
                
            if placedPlanter: 
                self.logger.webhook("",f"Placed Planter: {planter.title()}", "dark brown", "screen")          
                #use glitter
                if glitter: 
                    self.useItemInInventory("glitter")
                updateHourlyTime()
                return True
            self.logger.webhook("",f"Failed to Place Planter: {planter.title()}", "red", "screen", ping_category="ping_critical_errors")
            self.reset()
            
        updateHourlyTime()
        return False

    #locate the planter's growth bar and move there
    def moveToPlanter(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
        def getPlanterLocation():
            screen = mssScreenshotNP(self.robloxWindow.mx,self.robloxWindow.my,self.robloxWindow.mw,self.robloxWindow.mh)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
            # #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2HLS)
            #screen = cv2.imread("b.png")
            point = findColorObjectRGB(screen, (134, 213, 112), kernel=kernel, variance=2, draw=False)
            if not point:
                point = findColorObjectRGB(screen, (31, 231, 68), kernel=kernel, variance=2)
            
            if point:
                point = [x//self.robloxWindow.multi for x in point] 
            return point

        winUp, winDown = self.robloxWindow.mh/3.1, self.robloxWindow.mh/2.9
        winLeft, winRight = self.robloxWindow.mw/2.14, self.robloxWindow.mw/1.88

        hmove, vmove = "", ""
        for _ in range(10):
            location = getPlanterLocation()
            if location:
                break
        else:
            return
        
        x,y = location

        #move towards saturator
        if x >= winLeft and x <= winRight and y >= winUp and y <= winDown: 
            return
        if x < winLeft:
            keyboard.keyDown("a", False)
            hmove = "a"
        elif x > winRight:
            keyboard.keyDown("d", False)
            hmove = "d"
        if y < winUp:
            keyboard.keyDown("w", False)
            vmove = "w"
        elif y > winDown:
            keyboard.keyDown("s", False)
            vmove = "s"

        i = 0
        while hmove or vmove:
            #check if reached saturator
            if (hmove == "a" and x >= winLeft) or (hmove == "d" and x <= winRight):
                keyboard.keyUp(hmove, False)
                hmove = ""
                
            if (vmove == "w" and y >= winUp) or (vmove == "s" and y <= winDown):
                keyboard.keyUp(vmove, False)
                vmove = ""
            
            time.sleep(0.02)
            #taking too long, just give up
            if i >= 100:
                print("give up")
                keyboard.releaseMovement()
                break
            #update planter location
            location = getPlanterLocation()
            if location:
                x,y = location

            else: #cant find planter, pause
                keyboard.releaseMovement()
                #try to find planter
                for _ in range(10):
                    time.sleep(0.02)
                    location = getPlanterLocation()
                    #planter found
                    if location:
                        #move towards planter
                        if hmove:
                            keyboard.keyDown(hmove)
                        if vmove:
                            keyboard.keyDown(vmove)
                        x,y = location
                        break
                else: #still cant find it, give up
                    return
            i += 1
            
    def collectPlanter(self, planter, field):
        st = time.time()
        def updateHourlyTime():
            self.hourlyReport.addHourlyStat("misc_time", time.time()-st)
        

        for _ in range(2):
            if self.goToPlanter(planter, field, "collect"): 
                break
            self.logger.webhook("",f"Unable to find Planter: {planter.title()}", "dark brown", "screen")
            self.reset()
        else:
            updateHourlyTime()
            return False
        
        self.keyboard.press("e")
        self.clickYes()
        self.logger.webhook("",f"Looting: {planter.title()} planter","bright green", "screen", ping_category="ping_conversion_events")
        self.keyboard.multiWalk(["s","d"], 0.87)
        self.nmLoot(9, 5, "a")
        self.setMobTimer(field)
        updateHourlyTime()
        return True
        
    
    def placePlanterInCycle(self, slot, cycle):
        '''
        Returns planter, field, time planter is finish, if gather in field
        Returns none if placing it failed
        '''
        planter = self.setdat[f"cycle{cycle}_{slot+1}_planter"]
        field = self.setdat[f"cycle{cycle}_{slot+1}_field"]
        glitter = self.setdat[f"cycle{cycle}_{slot+1}_glitter"]
        gather = self.setdat[f"cycle{cycle}_{slot+1}_gather"]
        #set the cooldown for planters and place them
        if not self.placePlanter(planter,field, glitter): #make sure the planter was placed
            return
        
        if self.setdat["manual_planters_collect_full"]:
            baseGrowthTime, bonusFields, fieldGrowthBonus = planterGrowthData[planter]
            bonusTime = 0
            if glitter: bonusTime += 0.25
            if field in bonusFields: bonusTime += fieldGrowthBonus
            planterGrowthTime = (baseGrowthTime/(1+bonusTime))

        else:
            planterGrowthTime = self.setdat["manual_planters_collect_every"]*60*60 
        
        planterReady = time.strftime("%H:%M:%S", time.gmtime(planterGrowthTime))
        self.logger.webhook("", f"Planter will be ready in: {planterReady}", "light blue")

        planterCompleteTime = time.time() + planterGrowthTime

        self.reset()

        return (planter, field, planterCompleteTime, gather)
    
    def closeBlenderGUI(self):
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw/2-250), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48))-200)
        time.sleep(0.1)
        mouse.click()
        
    def blender(self, blenderData):
        itemNo = blenderData["item"]
        st = time.time()
        def updateHourlyTime():
            self.hourlyReport.addHourlyStat("misc_time", time.time()-st)

        def saveBlenderData():
            with open("./data/user/blender.txt", "w") as f:
                f.write(str(blenderData))
            f.close()
            updateHourlyTime()
        
        def getNextItem():
            nextItem = itemNo
            for _ in range(4):
                nextItem += 1
                if nextItem > 3:
                    nextItem = 1
                #item must be set and have repeats
                if (self.setdat[f"blender_item_{nextItem}"] != "none") and (self.setdat[f"blender_repeat_{nextItem}"] > 0 or self.setdat[f"blender_repeat_inf_{nextItem}"]):
                    return nextItem
            else:
                return 0 #no items to craft

        #check if item is none (settings got changed but user did not reset the blender data)
        #or first blender of the reset
        if blenderData["collectTime"] == 0 or (itemNo and self.setdat[f"blender_item_{itemNo}"] == "none"): 
            itemNo = getNextItem() #get the first item
            if not itemNo: #no items available
                blenderData["item"] = itemNo
                blenderData["collectTime"] = -1
                saveBlenderData()
                return

        for _ in range(2):
            self.logger.webhook("","Travelling: Blender","dark brown")
            self.cannon()
            self.runPath("collect/blender")
            for _ in range(6):
                self.keyboard.walk("d", 0.2)
                reached = self.isBesideE(["open"])
                if reached: break
            if reached: break
        else:
            self.logger.webhook("","Failed to reach Blender", "dark brown", "screen")
            updateHourlyTime()
            return
        
        x = self.robloxWindow.mx + self.robloxWindow.mw//2 - 280
        y = self.robloxWindow.my + self.robloxWindow.mh//2 - 240

        def clickOnBlenderElement(cx, cy):
            cx //= self.robloxWindow.multi
            cy //= self.robloxWindow.multi
            mouse.moveTo(cx+x, cy+y)
            time.sleep(0.1)
            mouse.click()
            mouse.moveBy(2,2)
            time.sleep(0.1)
            mouse.click()
            #close and reopen gui
            time.sleep(0.1)
            self.closeBlenderGUI()
            time.sleep(0.3)
            self.keyboard.press("e")

        self.keyboard.press("e")
        time.sleep(1)
        #check if blender is done and click on end crafting
        doneImg = self.adjustImage("images/menu", "blenderdone")
        res = locateImageOnScreen(doneImg, x, self.robloxWindow.my+(y), 560, 480, 0.75)
        if res:
            print("done")
            clickOnBlenderElement(*res[1])
        
        #check for cancel button
        cancelImg = self.adjustImage("images/menu", "blendercancel")
        res = locateImageOnScreen(cancelImg, x, self.robloxWindow.my+(y), 560, 480, 0.75)
        if res:
            print("cancel")
            clickOnBlenderElement(*res[1])

        #check if still crafting and get cd
        notDoneImg = self.adjustImage("images/menu", "blenderend")
        res = locateImageOnScreen(notDoneImg, x, self.robloxWindow.my+(y), 560, 480, 0.75)

        def cancelCraft():
            self.logger.webhook("", "Unable to detect remaining crafting time, ending craft", "dark brown", "screen")
            #mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw/2-120), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48))+120)
            clickOnBlenderElement(*res[1])

        if res:
            cdImg = mssScreenshot(self.robloxWindow.mx+(self.robloxWindow.mw/2-130),self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48)-70), 400, 65)
            cdRaw = ocr.ocrRead(cdImg)
            cdRaw = ''.join([x[1][0] for x in cdRaw])
            cd = self.cdTextToSecs(cdRaw, False, 3600) #1 hour cd
            if cd:
                cooldownFormat = timedelta(seconds=cd)
                self.logger.webhook("", f"Blender is currently crafting an item ({cooldownFormat} remaining)", "dark brown", "screen")
                #set the target time and quit
                self.closeBlenderGUI()
                blenderData["collectTime"] = time.time() + cd
                saveBlenderData()
                return
            else: #cant detect cd, just cancel craft
                cancelCraft()
        
        #time to craft
        if not itemNo: #if itemNo is 0, there are no items to craft. The macro has collected the last item to craft
            self.closeBlenderGUI()
            blenderData["collectTime"] = -1 #set collectTime to -1 (disable blender)
            saveBlenderData()
            return
        item = self.setdat[f"blender_item_{itemNo}"]
        #click to the item
        itemDisplay = item.title()
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw/2+240), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48))+128)
        for _ in range(blenderItems.index(item)):
            mouse.click()
            sleep(0.06)
        #check if the item can be crafted
        canMake = self.adjustImage("images/menu", "blendermake")
        if not locateImageOnScreen(canMake, self.robloxWindow.mx+(x), self.robloxWindow.my+(y), 560, 480, 0.8):
            self.logger.webhook("", f"Unable to craft {itemDisplay}", "dark brown", "screen")
        #open the crafting menu
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw/2), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48))+130)
        time.sleep(0.1)
        mouse.click()
        #set the quantity
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw/2-60), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48))+140)
        #check if max
        if self.setdat[f"blender_quantity_max_{itemNo}"]:
            #get a screenshot of the quantity
            #add more
            #get another screenshot
            #if both screenshots are the same, break

            def quantityScreenshot(save = False):
                return imagehash.average_hash(mssScreenshot(self.robloxWindow.mx+(self.robloxWindow.mw/2-60-140), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48)+140-20), 110, 20*2, save))
            quantity1Img = quantityScreenshot()
            while True:
                for _ in range(5): #add 5 quantity
                    mouse.click()
                    sleep(0.03)
                quantity2Img = quantityScreenshot()
                if quantity2Img == quantity1Img: #check if screenshots are similar
                    break
                #update the quantity
                quantity1Img = quantity2Img
            quantity = ''.join([x[1][0] for x in ocr.ocrRead(mssScreenshot(self.robloxWindow.mx+(self.robloxWindow.mw/2-60-140), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48)+140-20), 110, 23*2))])
            quantity = ''.join([x for x in quantity if x.isdigit()])
            if quantity:
                quantity = int(quantity)
            else:
                self.logger.webhook("", "Failed to detect the quantity of items crafted. The macro will get the crafting time on the next visit", "dark brown")
                quantity = 0
        else: 
            #normal quantity
            quantity = self.setdat[f"blender_quantity_{itemNo}"]
            for _ in range(quantity-1): #-1 because the quantity starts from 1
                mouse.click()
                sleep(0.03)
        #confirm
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw/2 + 70), self.robloxWindow.my+(math.floor(self.robloxWindow.mh*0.48))+130)
        time.sleep(0.1)
        mouse.click()
        #go to next item
        #decrement the repeat count
        if not self.setdat[f"blender_repeat_inf_{itemNo}"]:
            self.setdat = {**self.setdat, **settingsManager.incrementProfileSetting(f"blender_repeat_{itemNo}", -1)}
            self.updateGUI.value = 1
        blenderData["item"] = getNextItem()
        #calculate the time to collect the blender
        craftTime = quantity*5*60 #5mins per item
        blenderData["collectTime"] = time.time() + craftTime
        time.sleep(1) #add a delay here before taking a screenshot, since bss displays the crafting screen with default values for a bit
        self.logger.webhook("", f"Crafted: {itemDisplay} x{quantity}, Ready in: {timedelta(seconds=craftTime)}", "bright green", "screen", ping_category="ping_conversion_events")
        #store the data
        saveBlenderData()
        self.closeBlenderGUI()
        
    def claimStickerStack(self):
        time.sleep(1)
        x = self.robloxWindow.mw//2-275
        y = 4*self.robloxWindow.mh//10

        #detect sticker stack boost time
        screen = mssScreenshot(self.robloxWindow.mx+(x+550/2),self.robloxWindow.my+y,550/2,40)
        ocrRes = ''.join([x[1][0] for x in ocr.ocrRead(screen)])
        ocrRes = re.findall(r"\(.*?\)", ocrRes) #get text between brackets
        finalTime = None
        def cantDetectTime():
            self.logger.webhook("", "Failed to detect sticker stack buff duration", "red", "screen", ping_category="ping_critical_errors")
        if ocrRes:
            times = []
            if "x" in ocrRes[0]: #number of stickers
                stickerCount = int(''.join([x for x in ocrRes[0] if x.isdigit()]))
                times.append(15*60 + 10*stickerCount)
                ocrRes.pop(0)
            if ":" in ocrRes[0]: #direct
                times.append(self.cdTextToSecs(ocrRes[0], True, 0))
            if times:
                finalTime = max(times)
            else:
                cantDetectTime()
        else:
            cantDetectTime()
        stickerUsed = False
        #use sticker
        if "sticker" in self.setdat["sticker_stack_item"]:
            regularSticker = self.adjustImage("images/sticker_stack", "regularsticker")
            hiveSticker = self.adjustImage("images/sticker_stack", "hivesticker")
            stickerLoc = locateTransparentImageOnScreen(regularSticker, self.robloxWindow.mx+(x), self.robloxWindow.my+(y), 550, 220, 0.7)
            if self.setdat["hive_skin"] and stickerLoc is None: #cant find regular sticker, use hive skin
                stickerLoc = locateTransparentImageOnScreen(hiveSticker, self.robloxWindow.mx+(x), self.robloxWindow.my+(y), 550, 220, 0.7)
            if stickerLoc: #found a available sticker
                xr, yr = [j//self.robloxWindow.multi for j in stickerLoc[1]]

                mouse.moveTo(self.robloxWindow.mx+(x+xr), self.robloxWindow.my+(y+yr))
                time.sleep(0.1)
                mouse.moveBy(3,-3)
                time.sleep(0.2)
                mouse.click()
                stickerUsed = True
            elif not "/" in self.setdat["sticker_stack_item"]:
                self.logger.webhook("", "No Stickers left to stack, Sticker Stack has been disabled", "red", "screen", ping_category="ping_critical_errors")
                self.setdat["sticker_stack"] = False
                self.keyboard.press("e")
                return
        if "ticket" in self.setdat["sticker_stack_item"] and not stickerUsed:
                mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw//2+105), self.robloxWindow.my+(4*self.robloxWindow.mh//10-78))
                time.sleep(0.1)
                mouse.click()
                time.sleep(0.1)
                mouse.moveBy(2,2)
                mouse.click()

        #click yes
        yesPopup = False
        #check if there are 4 yes/no popups
        for _ in range(4): 
            if not self.clickYes(detect=True, clickOnce=True): 
                break
            else:
                yesPopup = True
                time.sleep(0.4)
        else: #4 yes/no popups, either cub/hive skin
            if not self.setdat["hive_skin"] and not self.setdat["cub_skin"]: #do not use cub and hive stickers
                self.logger.webhook("", "A hive/cub sticker has been wrongly selected, aborting", "red", "screen", ping_category="ping_critical_errors")
                self.keyboard.press("e")
                return
        
        if "ticket" in self.setdat["sticker_stack_item"] and not yesPopup: #if no popup appears, ran out of tickets
            self.logger.webhook("", "No Tickets left, Sticker Stack has been disabled", "red", "screen", ping_category="ping_critical_errors")
            self.setdat["sticker_stack"] = False
            self.keyboard.press("e")
            return
        if finalTime is not None:
            if stickerUsed: finalTime += 10
            self.logger.webhook("", f"Activated Sticker Stack, Buff Duration: {timedelta(seconds=finalTime)}", "bright green")
        else:
            with open("./data/user/sticker_stack.txt", "r") as f: #get the cooldown from the prev detection
                stickerStackCD = int(f.read())
            f.close()
            if stickerStackCD > 15*60: #make sure the time is valid
                finalTime = stickerStackCD + 10
            else:
                finalTime = 60*60 #default to 1hr
            self.logger.webhook("", f"Activated Sticker Stack, Buff Duration: {timedelta(seconds=finalTime)} (Defaulted to 1hr)", "bright green")
        self.keyboard.press("e")
        with open("./data/user/sticker_stack.txt", "w") as f:
            f.write(str(finalTime))
        f.close()
    
    #click the "allow for one month" on the "terminal is requesting to bypass" popup
    #Source: https://github.com/sevmanash/sevs-modified-macro/blob/main/src/modules/macro.py
    def clickPermissionPopup(self):
        permissionPopup = self.adjustImage("./images/mac", "allow")
        permissionPopup2 = self.adjustImage("./images/mac", "allowfor")
        permissionPopup3 = self.adjustImage("./images/mac", "cancel")
        x = self.robloxWindow.mw/4
        y = self.robloxWindow.mh/3
        res = locateImageOnScreen(permissionPopup, x, y, self.robloxWindow.mw/2, self.robloxWindow.mh/3, 0.8)
        res2 = locateImageOnScreen(permissionPopup2, x, y, self.robloxWindow.mw/2, self.robloxWindow.mh/3, 0.8)
        res3 = locateImageOnScreen(permissionPopup3, x, y, self.robloxWindow.mw/2, self.robloxWindow.mh/3, 0.8)
        if res or res2 or res3:
            if res or res2:
                self.logger.webhook("", "Detected: Terminal permission popup", "orange")
            else:
                self.logger.webhook("", "Detected: Screen permission popup", "orange")
            reses = res or res2 or res3  
            x2, y2 = reses[1]
            if self.display_type == "retina":
                x2 /= 2
                y2 /= 2
            mouse.moveTo(x+x2, y+y2)
            time.sleep(0.08)
            mouse.moveBy(1,1)
            time.sleep(0.1)
            mouse.click()

    def backgroundOnce(self):
        with open("./data/user/hotbar_timings.txt", "r") as f:
            hotbarSlotTimings = ast.literal_eval(f.read())
        f.close()

        #night detection
        if self.enableNightDetection:
            self.detectNight()

        #hotbar
        for i in range(1,8):
            slotUseWhen = self.setdat[f"hotbar{i}_use_when"]
            #check if use when is correct
            if slotUseWhen == "never": continue
            elif self.status.value == "rejoining": continue
            elif slotUseWhen == "gathering" and not "gather_" in self.status.value: continue 
            elif slotUseWhen == "converting" and not self.status.value == "converting": continue 
            #check cd
            cdSecs = self.setdat[f"hotbar{i}_use_every_value"]
            if self.setdat[f"hotbar{i}_use_every_format"] == "mins": 
                cdSecs *= 60
            if time.time() - hotbarSlotTimings[i] < cdSecs: continue
            print(f"pressed hotbar {i}")
            #press the key
            for _ in range(2):
                keyboard.pagPress(str(i))
                time.sleep(0.4)
            #update the time pressed
            hotbarSlotTimings[i] = time.time()
            with open("./data/user/hotbar_timings.txt", "w") as f:
                f.write(str(hotbarSlotTimings))
            f.close()
    
    def background(self):
        while True:
            self.backgroundOnce()
            time.sleep(1)

    def getHoney(self):
        cap = mssScreenshot(self.robloxWindow.mx+(self.robloxWindow.mw//2-241), self.robloxWindow.my+self.robloxWindow.yOffset+5, 140, 36)
        ocrres = ocr.ocrFunc(cap)
        honey = ""
        try:
            result = ''.join([x[1][0] for x in ocrres])
            for i in result:
                if i == "(" or i == "+":
                    break
                elif i.isdigit():
                    honey += i
            honey = int(honey)
        except Exception as e:
            print(e)
            print(honey)
        return honey if honey else 0

    def hourlyReportBackgroundOnce(self):
        try:
            currMin = datetime.now().minute
            currSec = datetime.now().second

            #check if its time to send hourly report
            if currMin == 0 and time.time() - self.lastHourlyReport > 120:
                hourlyReportData = self.hourlyReport.generateHourlyReport(self.setdat)
                self.logger.hourlyReport("Hourly Report", "", "purple")

                #add to history
                with open("data/user/hourly_report_history.txt", "r") as f:
                    history = ast.literal_eval(f.read())
                f.close()

                historyObj = {
                    "endHour": datetime.now().hour,
                    "date": str(datetime.today().date()),
                    "honey": hourlyReportData["honey_per_min"][-1] - hourlyReportData["honey_per_min"][0]
                }
                #max 5 objs
                if len(history) > 4:
                    history.pop(-1)
                history.insert(0,historyObj)

                with open("data/user/hourly_report_history.txt", "w") as f:
                    f.write(str(history))
                f.close()

                self.lastHourlyReport = time.time()
                #reset stats
                self.hourlyReport.resetHourlyStats()

            #Hourly report
            if self.status.value != "rejoining":
                #instead of using time.sleep, we want to run the code at the start of the min
                if currMin != self.prevMin:
                    self.prevMin = currMin
                    honey = self.getHoney()
                    print(honey)
                    backpack = self.getBackpack()

                    self.hourlyReport.addHourlyStat("honey_per_min", honey)
                    self.hourlyReport.addHourlyStat("backpack_per_min", backpack)

            if self.status.value != "rejoining" and not currSec%6 and currSec != self.prevSec:
                i = (60*currMin + currSec)//6
                screen = cv2.cvtColor(self.buffDetector.screenshotBuffArea(), cv2.COLOR_BGRA2BGR)
                height, width = screen.shape[:2]
                uptimeBuffsColors = self.hourlyReport.uptimeBuffsColors
                uptimeBearBuffs = self.hourlyReport.uptimeBearBuffs

                for j in ["baby_love"]:
                    if self.buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors[j][0], uptimeBuffsColors[j][1], y1=30*self.multi, searchDirection=7):
                        self.hourlyReport.uptimeBuffsValues[j][i] = 1

                bearBuffRes = [int(x) for x in self.buffDetector.getBuffsWithImage(uptimeBearBuffs, screen=screen, threshold=0.78)]
                if any(bearBuffRes):
                    self.hourlyReport.uptimeBuffsValues["bear"][i] = 1

                for j in ["focus", "bomb_combo", "balloon_aura", "inspire"]:
                    res = self.buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors[j][0], uptimeBuffsColors[j][1], y1=30*self.multi, y2=50*self.multi, searchDirection=7)
                    if res:
                        x = res[0]+res[2]
                        x1 = max(0, int(x-25*self.multi))
                        x2 = min(width, int(x+5*self.multi))
                        buffImg = screen[15*self.multi:50*self.multi , x1:x2]
                        self.hourlyReport.uptimeBuffsValues[j][i] = int(self.buffDetector.getBuffQuantityFromImgTight(buffImg))

                x = 0
                for _ in range(3):
                    res = self.buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["haste"][0], uptimeBuffsColors["haste"][1],x, 30*self.multi, searchDirection=6)
                    if not res:
                        break
                    x = res[0]
                    if self.buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["melody"][0], uptimeBuffsColors["melody"][1], x+2*self.multi, 30, x+34*self.multi, 40*self.multi, 12):
                        self.hourlyReport.uptimeBuffsValues["melody"][i] = 1
                    elif not self.hourlyReport.uptimeBuffsValues["haste"][i]:
                        x1 = max(0, int(x+6*self.multi))
                        x2 = min(width, int(x+44*self.multi))
                        buffImg = screen[15*self.multi:50*self.multi , x1:x2]
                        self.hourlyReport.uptimeBuffsValues["haste"][i] = int(self.buffDetector.getBuffQuantityFromImgTight(buffImg))
                    x += 44*self.multi
                #print(bd.detectBuffColorInImage(screen, 0xff242424, variation=12, minSize=(3*2,2*2), show=True))

                x = screen.shape[1]
                for _ in range(3):
                    res = self.buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["boost"][0], uptimeBuffsColors["boost"][1], y1=30*self.multi, x2=x, searchDirection=7)
                    if not res:
                        break
                    x = res[0]+res[2]
                    y = res[1] + res[3]

                    if len(self.buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["red_boost"][0], uptimeBuffsColors["red_boost"][1], x-30*self.multi, 15*self.multi, x-4*self.multi, 34*self.multi, 20)):
                        buffType = "red_boost"
                    elif len(self.buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["blue_boost"][0], uptimeBuffsColors["blue_boost"][1], x-30*self.multi, 15*self.multi, x-4*self.multi, 34*self.multi, 20)):
                        buffType = "blue_boost"
                    else:
                        buffType = "white_boost"

                    x1 = max(0, x-25*self.multi)
                    buffImg = screen[15*self.multi: 50*self.multi, x1: x]
                    self.hourlyReport.uptimeBuffsValues[buffType][i] = int(self.buffDetector.getBuffQuantityFromImgTight(buffImg))

                    x -= 40*self.multi
                
                self.prevSec = currSec

                if "gather_" in self.status.value:
                    self.hourlyReport.buffGatherIntervals[i] = 1
                self.hourlyReport.saveHourlyReportData()
        except Exception:
            self.logger.webhook("Hourly Report Error", traceback.format_exc(), "red", ping_category="ping_critical_errors")
        
    def hourlyReportBackground(self):
        while True:
            self.hourlyReportBackgroundOnce()
            time.sleep(1)

    def mergedBackgrounds(self):
        while True:
            self.backgroundOnce()
            self.hourlyReportBackgroundOnce()
            time.sleep(1)

    def toggleQuest(self):
        #click quest icon
        mouse.moveTo(self.robloxWindow.mx+(80), self.robloxWindow.my+(113))
        time.sleep(0.1)
        mouse.moveBy(0,3)
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.3)
        mouse.moveTo(self.robloxWindow.mx+(312), self.robloxWindow.my+(200))
        mouse.click()

    def findQuest(self, questGiver):
        #map quest giver to a shorthand form for ocr searching
        questGiverShort = {
            "polar bear": "polar",
            "bucko bee": "bucko",
            "riley bee": "riley",
            "honey bee": "honey"
        }

        #prevent the macro from false detecting beesmas quests
        questTitleBlacklistedPhrases = {
            "polar bear": ["beesmas", "feast"],
            "bucko bee": ["snow", "machine"],
            "riley bee": ["snow", "machine"]
        }

        #sanity check
        if not questGiver in questGiverShort:
            raise Exception(f"Unknown Quest Giver: {questGiver}")
        
        def screenshotQuest(screenshotHeight, mode = "gray"):
            #Take a screenshot of the quest page
            mode = mode.lower()
            if mode == "rgba":
                screenshotFunction = mssScreenshotPillowRGBA
            else:
                screenshotFunction = mssScreenshotNP
            screen = screenshotFunction(self.robloxWindow.mx, self.robloxWindow.my+150, 300, min(screenshotHeight, self.robloxWindow.mh-(self.robloxWindow.my+150)))
            if mode == "gray":
                screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)
            return screen
        
        #open inventory to ensure quest page is closed
        self.toggleInventory("close")
        self.toggleQuest()
        #scroll to top
        #stop scrolling when the quest page remains unchanged
        prevHash = None
        for _ in range(200):
            mouse.scroll(100)
            sleep(0.08)
            hash = imagehash.average_hash(Image.fromarray(screenshotQuest(100)))
            if not prevHash is None and prevHash == hash:
                break
            prevHash = hash
        #scroll down, note the best match
        sleep(0.4)
        questTitle = None
        questTitleYPos = None

        questGiverImg = Image.open(f"./images/quest/{questGiver}-{self.robloxWindow.display_type}.png").convert('RGBA')
        prevHash = None
        for i in range(150):
            screen = screenshotQuest(800, mode="RGBA")

            res = bitmap_matcher.find_bitmap_cython(screen, questGiverImg, variance=5, h=250)
            if res:
                rx, ry = res
                rw, rh = questGiverImg.size
                img = cv2.cvtColor(np.array(screen), cv2.COLOR_RGBA2GRAY)
                img = img[ry-10:ry+rh+20, rx-5:]
                img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                img = cv2.GaussianBlur(img, (5, 5), 0)
                img = Image.fromarray(img)
                
                ocrRes = ocr.ocrRead(img)
                text = self.convertCyrillic(''.join([x[1][0].strip().lower() for x in ocrRes]))
                for word in questTitleBlacklistedPhrases.get(questGiver, []):
                    if word in text: 
                        break
                else:
                    #match text with the closest known quest title
                    questTitleYPos = ry
                    print(questTitleYPos)
                    questTitle, _ = fuzzywuzzy.process.extractOne(text, quest_data[questGiver].keys())
                    self.logger.webhook("", f"Quest Title: {questTitle}", "dark brown")
                    break
                
            mouse.scroll(-1, True)
            time.sleep(0.06)
            hash = imagehash.average_hash(Image.fromarray(screenshotQuest(100)))
            if not prevHash is None and prevHash == hash:
                break

        if questTitle is None:
            self.logger.webhook("", f"Could not find {questGiver} quest", "dark brown")
            self.toggleQuest()
            self.moveMouseToDefault()
            return None
        
        #quest title found, now find the objectives
        objectives = quest_data[questGiver][questTitle]

        #merge the texts into chunks. Using those chunks, compare it with the known objectives
        #assume that the merging is done properly, so 1st chunk = 1st objective
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGBA2BGR)
        #crop it just above the quest title
        screen = screen[questTitleYPos: , : ]
        screenOriginal = np.copy(screen)

        #crop it below the quest title, to the first objective
        #this is done by detecting the color of the title bar, since relying on ocr's bounding box can cause it to overcrop
        cropTargetColor = [247, 240, 229]
        cropColorTolerance = 3
        lower = np.array([c - cropColorTolerance for c in cropTargetColor], dtype=np.uint8)
        upper = np.array([c + cropColorTolerance for c in cropTargetColor], dtype=np.uint8)

        #create a mask for the target color
        cropMask = cv2.inRange(screen, lower, upper)
        cropRows = np.any(cropMask > 0, axis=1)
        startIndex = None
        endIndex = 0

        #start searching for the start and end y points of the quest title
        #if it can't find the title bar in the first y pixels, stop the search
        #in some cases, the questTitleYPos already crops below the quest title
        maxHeight = 20*self.robloxWindow.multi
        for i, hasColor in enumerate(cropRows):
            if i > maxHeight and startIndex is None:
                break
            if hasColor and startIndex is None:
                #found the starting point of the first quest title area
                startIndex = i
            elif not hasColor and startIndex is not None:
                #found the ending point of the quest title area
                endIndex = i
                break
        
        #crop
        if endIndex:
            screen = screen[endIndex:, :]

        #convert to grayscale
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        img = cv2.inRange(screenGray, 0, 50)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        #dilute the image so that texts can be merged into chunks
        kernelSize = 10 if self.robloxWindow.isRetina else 7
        kernel = np.ones((kernelSize, kernelSize), np.uint8) 
        img = cv2.dilate(img, kernel, iterations=1)

        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #filter out the contour sizes
        minArea = 4000*self.robloxWindow.multi       #too small = noise
        maxArea = 40000*self.robloxWindow.multi     #too big = background or large UI elements
        maxHeight = 75*self.robloxWindow.multi       #cap height to filter out title bar

        completedObjectives = []
        incompleteObjectives = []
        i = 0
        for contour in contours[::-1]:
            x, y, w, h = cv2.boundingRect(contour)
            #check if contour meets size requirements
            area = w*h
            if area < minArea or area > maxArea or h > maxHeight:
                cv2.rectangle(screen, (x, y), (x+w, y+h), (0, 255, 255), 1) #draw a yellow bounding box
                continue
            textImg =  Image.fromarray(screen[y:y+h, x:x+w])
            textChunk = []
            for line in ocr.ocrRead(textImg):
                textChunk.append(self.convertCyrillic(line[1][0].strip().lower()))
            textChunk = ''.join(textChunk)
            print(textChunk)

            #detect amount of items to feed
            objectiveData = objectives[i].split("_")
            if objectiveData[0] == "feed":
                amount = 0
                #start by trying to get the text from the progression, ie 0/x
                if "/" in textChunk: 
                    split = textChunk.split("/")[1].replace(",","").replace(".", "")
                    amount = int(split) if split.isdigit() else 0
                #find it via words, ie feed x bluberries
                if not amount:
                    words = textChunk.split(" ")
                    for word in words:
                        if word.isdigit():
                            amount = int(word)
                            break
                if amount:
                    objectiveData[1] = str(min(int(amount), 50))
                    objectives[i] = "_".join(objectiveData)

            if "complete" in textChunk:
                completedObjectives.append(objectives[i])
                color = (0, 255, 0)  #green
            else:
                incompleteObjectives.append(objectives[i])
                color = (0, 0, 255)  #red
            
            #draw bounding boxes and add the quest text
            drawY = y+endIndex
            print(drawY)
            cv2.rectangle(screenOriginal, (x, drawY), (x+w, drawY+h), color, 2)
            cv2.putText(screenOriginal, objectives[i], (x, drawY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            i += 1

            if i == len(objectives):
                break
        
        questImgPath = "latest-quest.png"
        cv2.imwrite(questImgPath, screenOriginal)
        
        print(completedObjectives)
        print(incompleteObjectives)
        self.logger.webhook(f"Detected {questGiver.title()} Quest: {questTitle.title()}", 
                            "**Completed Objectives:**\n{}\n\n**Incomplete Objectives:**\n{}".format(
                                '\n'.join(completedObjectives) if completedObjectives else "None", 
                                '\n'.join(incompleteObjectives) if incompleteObjectives else "None"), 
                            "light blue", imagePath=questImgPath)
        self.toggleQuest()
        self.moveMouseToDefault()
        return incompleteObjectives

    def goToQuestGiver(self, questGiver, reason):
        for _ in range(3):
            self.cannon()
            self.logger.webhook("",f"Travelling: {questGiver} ({reason}) ","brown")
            self.runPath(f"quests/{questGiver}")
            time.sleep(0.5)

            #check if player reached the quest giver
            if self.isBesideE(["talk"] + questGiver.lower().split(" "), log=True):
                self.logger.webhook("",f"Reached {questGiver}","brown", "screen")
                self.keyboard.press("e")
                sleep(0.2)
                self.keyboard.press("e")
                return True
            else:
                self.logger.webhook("",f"Failed to reach {questGiver}","brown", "screen")
                self.reset()
        return False

    def clickdialog(self, mustFindDialog=False):
        dialogImg = self.adjustImage("./images/menu", "dialog")
        x = self.robloxWindow.mw/2
        y = self.robloxWindow.mh*2/3
        a =  locateImageOnScreen(dialogImg, self.robloxWindow.mx+(x), self.robloxWindow.my+(y), 300, self.robloxWindow.mh/3, 0.8 if mustFindDialog else 0.5)
        if a:
            _, loc = a
            xr, yr = [j//self.robloxWindow.multi for j in loc]
        else:
            xr = 0
            yr = 0
            if mustFindDialog: return
            print("unable to locate dialog position")

        def screenshotDialog():
            return imagehash.average_hash(mssScreenshot(self.robloxWindow.mx+x+xr-40, self.robloxWindow.my+y+yr-40, 40, 40))
        
        dialogImg = screenshotDialog()
        mouse.moveTo(self.robloxWindow.mx+(self.robloxWindow.mw/2), self.robloxWindow.my+(y+yr-20))
        for _ in range(80):
            mouse.click()
            time.sleep(0.1)
            #check if the dialog is still there
            img = screenshotDialog()
            if abs(img - dialogImg) > 15:
                break

    def getNewQuest(self, questGiver, submitQuest):
        if not self.goToQuestGiver(questGiver, "Submit Quest" if submitQuest else "Get New Quest"): return
        dialogClickCountForQuestGivers = {
            "polar bear": 25,
            "bucko bee": 40,
            "honey bee": 40,
            "riley bee": 40
        }
        dialogClickCount = dialogClickCountForQuestGivers.get(questGiver, 50)
        self.clickdialog()
        #player submitted a quest, then get a new one
        if True: #submitQuest:
            sleep(1)
            self.keyboard.press("e")
            sleep(0.2)
            self.keyboard.press("e")
            self.clickdialog()
        self.reset()
        return self.findQuest(questGiver)

    def feedBee(self, item, quantity):
        res = self.findItemInInventory(item)
        if not res: 
            return
        
        x, y = res
        #re-adjust camera
        for _ in range(10):
            self.keyboard.press("pageup")
        for _ in range(4):
            self.keyboard.press("pagedown")

        for _ in range(2):
            mouse.moveTo(self.robloxWindow.mx+(x), self.robloxWindow.my+(y))
            time.sleep(0.3)
            pag.dragTo(self.robloxWindow.mx + self.robloxWindow.mw//2, self.robloxWindow.my + self.robloxWindow.mh//2-80, 0.6, button='left')

        #interact with feed menu
        time.sleep(1)
        feedButtonImg = self.adjustImage("./images/menu", "feed")
        fx = self.robloxWindow.mx + (54*self.robloxWindow.mw)//100-300
        fy = self.robloxWindow.my + self.robloxWindow.yOffset + (46*self.robloxWindow.mh)//100-59
        fres = locateImageOnScreen(feedButtonImg, fx, fy, 300, 120, 0.75)
        if not fres:         
            self.moveMouseToDefault()
            return

        frx, fry = [x//self.robloxWindow.multi for x in fres[1]]

        #change quantity
        mouse.moveTo(fx+frx+150, fy+fry+8)
        time.sleep(0.1)
        for _ in range(2):
            mouse.click()
            time.sleep(0.02)
        self.keyboard.write(str(quantity))

        #click feed button
        mouse.moveTo(fx+frx, fy+fry)
        time.sleep(0.1)
        for _ in range(2):
            mouse.click()
            time.sleep(0.02)
        
        self.logger.webhook("",f"Fed {quantity} {item}", "bright green")

        self.moveMouseToDefault()

    def saveAFB(self, name):
        return settingsManager.saveSettingFile(name, time.time(), "./data/user/AFB.txt")
    
    def getAFBtiming(self,name = None):
        for _ in range(3):
            data = settingsManager.readSettingsFile("./data/user/AFB.txt")
            if data: break #most likely another process is writing to the file
            time.sleep(0.1)
        if name is not None:
            if not name in data:
                print(f"could not find timing for {name}, setting a new one")
                self.saveAFB(name)
                return time.time()
            return data[name]
        return data
    
    def hasAFBRespawned(self, name, cooldown, applyMobRespawnBonus = False, timing = None):
        if timing is None: timing = self.getAFBtiming(name)
        if not isinstance(timing, float) and not isinstance(timing, int):
            print(f"Timing is not a valid number? {timing}")
        mobRespawnBonus = 1
        if applyMobRespawnBonus:
            mobRespawnBonus -= 0.15 if self.setdat["gifted_vicious"] else 0
            mobRespawnBonus -= self.setdat["stick_bug_amulet"]/100 
            mobRespawnBonus -= self.setdat["icicles_beequip"]/100 

        return time.time() - timing >= cooldown*mobRespawnBonus
    
    def AFB(self, gatherInterrupt = False, turnOffShiftLock = False):  # Auto Field Boost - WOOHOO
        
        def normalize(text):
            text = text.lower()
            text = re.sub(r'[^a-z\s]', ' ', text)  # remove symbols
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        
        returnVal = None
        # time limit - :(
        if self.AFBLIMIT: return True
        if not self.AFBLIMIT and self.setdat["AFB_limit_on"] and self.hasAFBRespawned("AFB_limit", self.setdat["AFB_limit"]*60*60):
            self.logger.webhook("AFB", "Time limit reached: Skipping", "red")
            self.AFBLIMIT = True

        goToField = threading.Thread(target=self.goToField, args=(self.setdat["AFB_field"],))
        Glitter = threading.Thread(target=self.useItemInInventory, args=("glitter",))

        x = self.setdat["AFB_attempts"]
        field = [f.replace("_", " ") for f in self.setdat["AFB_field"].lower().split(" ")]
        rebuff = self.setdat["AFB_rebuff"]
        dice = self.setdat["AFB_dice"]
        glitter = self.setdat["AFB_glitter"]
        diceslot = self.setdat["AFB_slotD"]
        glitterslot = self.setdat["AFB_slotG"]

        if gatherInterrupt:
            if ((glitter and self.hasAFBRespawned("AFB_glitter_cd", rebuff * 60) and self.AFBglitter) or (self.hasAFBRespawned("AFB_dice_cd", self.setdat["AFB_rebuff"] * 60) and not self.AFBglitter)) and not self.failed:                
                self.status.value = ""
                self.afb = True
                if turnOffShiftLock: self.keyboard.press("shift")
                self.logger.webhook("Gathering: interrupted", "Automatic Field Boost", "brown")
                if self.AFBglitter: 
                    self.reset(convert=False) 
                else: 
                    self.reset(AFB=True)

        if self.hasAFBRespawned("AFB_dice_cd", rebuff*60) or self.hasAFBRespawned("AFB_glitter_cd", rebuff*60):
            self.failed = False
            if self.setdat["Auto_Field_Boost"]:
                # dice
                if self.cAFBDice or (self.hasAFBRespawned("AFB_dice_cd", rebuff*60) and not self.AFBglitter):
                    self.cAFBDice = False
                    # get all fields
                    fields = {
                        "rose": [["rose"]],
                        "strawberry": [["strawberry"]],
                        "mushroom": [["mushroom"]],
                        "pepper": [["pepper"]],
                        "sunflower": [["sunflower"]],
                        "dandelion": [["dandelion"]],
                        "spider": [["spider"]],
                        "coconut": [["coconut"]],
                        "pine tree": [["pine", "tree"]],
                        "blue flower": [["blue", "flower"]],
                        "bamboo": [["bamboo"]],
                        "stump": [["stump"]],
                        "clover": [["clover"]],
                        "pineapple": [["pineapple"]],
                        "pumpkin": [["pumpkin"]],
                        "cactus": [["cactus"]],
                        "mountain top": [["mountain", "top"]],
                    }
                    # ignore detected lines with these words, reduces false positives
                    ignore = {"strawberry", "strawberries", "blueberry", "blueberries",
                    "seed", "seeds", "pineapple", "pineapples", "honey", "from"}

                    def ignore2(field, text):
                        for word in ignore:
                            # allow the word if it is part of the field name
                            if word in field.replace(" ", ""):
                                continue
                            if word in text.split():
                                return True
                        return False

                    #begin
                    self.logger.webhook("", f"Auto Field Boost", "white")
                    for i in range(2):
                        self.keyboard.press("i") # to avoid clicking on bees
                    self.keyboard.press("pageup") # to avoid clicking on stickers
                    # go to field if loaded, chance of field being boosted: 25% - 100%
                    if "loaded" in dice:
                        self.cannon()
                        self.goToField(field)

                    # using inv instead
                    if diceslot == 0: 
                        diceCoords = self.findItemInInventory(self.setdat['AFB_dice'])

                    for i in range(x):
                        bluetexts = ""
                        self.logger.webhook("", f"{str(dice).title()}, Attempt: {i+1}/{x}", "white")

                        # using inv instead
                        if diceslot == 0: 
                            if diceCoords:
                                self.useItemInInventory(x=diceCoords[0], y=diceCoords[1], closeInventoryAfter=False) 
                            # use
                        else: self.keyboard.press(str(diceslot))

                        #timeout: (IN CASE OF) failed detection or high lag
                        timeout = 0 
                        for _ in range(300):
                            if self.blueTextImageSearch("boosted"): # if message contains "boosted", continue
                                time.sleep(1.25)
                                break
                            timeout += 1    
                            if timeout == 300: # else try again after other tasks
                                self.logger.webhook("", "Auto Field Boost: Timeout", "white")
                                self.toggleInventory("close")
                                self.saveAFB("AFB_dice_cd")
                                self.AFBglitter = False
                                return
                        for _ in range(4):
                            bluetexts += ocr.imToString("blue") + "\n"

                        bluetexts = normalize(bluetexts)
                        tokens = set(bluetexts.split())

                        # smooth/loaded
                        clean = normalize(bluetexts)
                        # "and the" appears when using loaded and smooth
                        and_the = [line for line in bluetexts.split("\n") if "boosted" in line]
                        
                        the = bluetexts.split()  # get each line of detected text
                        boostedField = []

                        # for field dice only
                        if "field" in dice:
                            boostedField = None
                            for cf in field:
                                for pattern in fields[cf]:
                                    if set(pattern).issubset(tokens):
                                        if not ignore2(cf, bluetexts):
                                            boostedField = cf
                                            break
                                if boostedField:
                                    break
                            
                        #other die
                        else:
                            boostedFields = []
                            for cf in field:
                                cf_tokens = cf.split()
                                for sentence in and_the:
                                    sentence_tokens = set(normalize(sentence).split())
                                    for pattern in fields[cf]:
                                        if set(pattern).issubset(sentence_tokens) and not ignore2(cf, sentence):
                                            if cf not in boostedFields:
                                                boostedFields.append(cf)

                        # field user selected is detected
                        if "field" in dice:
                            if boostedField is not None:
                                self.logger.webhook("", f"Boosted Field: {boostedField}", "bright green", "blue")
                                returnVal = field
                                self.keyboard.press("pagedown")
                                for i in range(3):
                                    self.keyboard.press("o")
                                if diceslot == 0: self.toggleInventory("close")
                                self.saveAFB("AFB_dice_cd")
                                if glitter:
                                    self.AFBglitter = True
                                    self.saveAFB("AFB_glitter_cd")
                                return returnVal
                            else:
                                continue
                        else:
                            if field in boostedFields:
                                self.logger.webhook("", f"Boosted Fields: {', '.join(boostedFields)}", "blue")
                                returnVal = field
                                self.keyboard.press("pagedown")
                                for i in range(3):
                                    self.keyboard.press("o")
                                if diceslot == 0: self.toggleInventory("close")
                                self.saveAFB("AFB_dice_cd")
                                if glitter:
                                    self.AFBglitter = True
                                    self.saveAFB("AFB_glitter_cd")
                                return returnVal
                            else:
                                if boostedFields:
                                    self.logger.webhook("", f"Boosted Fields: {', '.join(boostedFields)}", "red")
                                else:
                                    self.logger.webhook("", "Boosted Fields: None", "red")
                                time.sleep(0.5)

                # glitter    
                if glitter and not self.failed:
                    if self.cAFBglitter or (self.hasAFBRespawned("AFB_glitter_cd", rebuff*60) and self.AFBglitter):
                        self.logger.webhook("", "Rebuffing: Glitter", "white")
                        if glitterslot == 0: 
                            self.cannon() 
                            Glitter.start()
                            goToField.start()
                            goToField.join()
                            Glitter.join()
                            self.clickYes()
                        else: 
                            self.cannon() 
                            self.goToField(field)
                            time.sleep(0.5)
                            self.keyboard.press(str(glitterslot))
                        self.logger.webhook("", "Rebuffed: Glitter", "white")
                        self.saveAFB("AFB_dice_cd")
                        self.saveAFB("AFB_glitter_cd")
                        self.reset()
                        self.AFBglitter = False
                        self.cAFBglitter = False
                        self.afb = False
                        return returnVal

            if returnVal == None:
                self.failed = True
                self.keyboard.press("pagedown")
                for i in range(3):
                    self.keyboard.press("o")
                self.logger.webhook("", f"Failed to boost {field}", "red")
                self.saveAFB("AFB_dice_cd")
                if glitter: 
                    self.saveAFB("AFB_glitter_cd")
                    self.AFBglitter = False
                if diceslot == 0: self.toggleInventory("close")
                return

    def startDetect(self):
        #disable game mode
        self.moveMouseToDefault()
        if sys.platform == "darwin":
            time.sleep(1)
            #check roblox scaling
            #this is done by checking if all pixels at the top of the screen are black
            topScreen = mssScreenshot(0, 0, self.robloxWindow.mw, 2)
            extrema = topScreen.convert("L").getextrema()
            #all are black
            if extrema == (0, 0):
                messageBox.msgBox(text='It seems like you have not enabled roblox scaling. The macro will not work properly.\n1. Close Roblox\n2. Go to finder -> applications -> right click roblox -> get info -> enable "scale to fit below built-in camera"', title='Roblox scaling')
            #make sure game mode is disabled (macOS 14.0 and above and apple chips)
            macVersion, _, _ = platform.mac_ver()
            macVersion = float('.'.join(macVersion.split('.')[:2]))

            # if 14 <= macVersion <= 15 and platform.processor() == "arm" and self.isFullScreen():
            #     self.logger.webhook("","Detecting and disabling game mode","dark brown")
            #     #make sure roblox is not fullscreen
            #     self.toggleFullScreen()

            #     #find the game mode button
            #     lightGameMode = self.adjustImage("./images/mac", "gamemodelight")
            #     darkGameMode = self.adjustImage("./images/mac", "gamemodedark")
            #     x = self.robloxWindow.mw/2.3
            #     time.sleep(1.2)
            #     #find light mode
            #     res = locateImageOnScreen(lightGameMode, self.robloxWindow.mx+(x), self.robloxWindow.my+(0), self.robloxWindow.mw-x, 60, 0.7)
            #     if res is None: #cant find light, find dark
            #         res = locateImageOnScreen(darkGameMode, self.robloxWindow.mx+(x), self.robloxWindow.my+(0), self.robloxWindow.mw-x, 60, 0.7)
            #     #found either light or dark
            #     if not res is None:
            #         gx, gy = [x//self.robloxWindow.multi for x in res[1]]
            #         mouse.moveTo(self.robloxWindow.mx+(gx+x), self.robloxWindow.my+(gy))
            #         time.sleep(0.1)
            #         mouse.fastClick()
            #         time.sleep(0.5)
            #         #check if game mode is enabled
            #         screen = mssScreenshot(x, 0, self.robloxWindow.mw-x, 150)
            #         ocrRes = ocr.ocrRead(screen)
            #         for i in ocrRes:
            #             if "mode off" in i[1][0].lower():
            #                 #disable game mode
            #                 bX, bY = ocr.getCenter(i[0])
            #                 if self.display_type == "retina":
            #                     bX //= 2
            #                     bY //= 2
            #                 mouse.moveTo(self.robloxWindow.mx+(x+bX), self.robloxWindow.my+(bY))
            #                 mouse.click()                        
            #                 break
            #         else: #game mode is already disabled/couldnt be found
            #             mouse.moveTo(self.robloxWindow.mx+(x+gx), self.robloxWindow.my+(gy))
            #             mouse.click()
            #     #fullscreen back roblox
            #     appManager.openApp("Roblox")
            #     self.toggleFullScreen()
            # Removed lines that were un-fullscreening Roblox on startup
            # appManager.setAppFullscreen(fullscreen=False)
            # appManager.maximiseAppWindow()
            time.sleep(1)
            self.moveMouseToDefault()

        #detect new/old ui and set 
        #also check for screen recording permission 
        # if self.getTop(0):
        #     self.newUI = False
        #     self.logger.webhook("","Detected: Old Roblox UI","light blue")
        # elif self.getTop(30):
        #     self.newUI = True
        #     self.logger.webhook("","Detected: New Roblox UI","light blue")
        # else:
        #     self.logger.webhook("","Unable to detect Roblox UI","red", "screen")
        self.newUI = True
        ocr.newUI = True
        logModule.newUI = True

        #check for accessibility
        #this is done by taking 2 different screenshots
        #if they are both the same, we assume that the keypress didnt go through and hence accessibility is not enabled
        if sys.platform == "darwin":
            originalX = mouse.getPos()[0]
            mouse.moveBy(100, 0)
            time.sleep(0.15)
            newX = mouse.getPos()[0]
            if originalX == newX:
                messageBox.msgBox(text='It seems like terminal does not have the accessibility permission. The macro will not work properly.\n\nTo fix it, go to System Settings -> Privacy and Security -> Accessibility -> add and enable Terminal.\n\nVisit https://existance-macro.gitbook.io/existance-macro-docs/macro-installation/images-and-media/1.-terminal-permissions for detailed instructions\n\n NOTE: This popup might be incorrect. If the macro is able to input keypresses and interact with the game, you can dismiss this popup', title='Accessibility Permission')
            time.sleep(1)
            # img1 = pillowToHash(mssScreenshot())
            # self.keyboard.press("esc")
            # time.sleep(0.1)
            # time.sleep(0.5)
            # img2 = pillowToHash(mssScreenshot())
            # self.keyboard.press("esc")
            # if similarHashes(img1, img2, 3):
            #     messageBox.msgBox(text='It seems like terminal does not have the accessibility permission. The macro will not work properly.\n\nTo fix it, go to System Settings -> Privacy and Security -> Accessibility -> add and enable Terminal.\n\nVisit #6system-settings in the discord for more detailed instructions\n\n NOTE: This popup might be incorrect. If the macro is able to input keypresses and interact with the game, you can dismiss this popup', title='Accessibility Permission')
            # time.sleep(1)
        
        private_server_link = self.setdat.get("private_server_link", "")
        if private_server_link and "share" in private_server_link and self.setdat.get("rejoin_method") == "deeplink":
            messageBox.msgBox(text="You entered a 'share?code' private server link!\n\nTo fix this:\n1. Paste the link in your browser\n2. Wait for roblox to load in\n3. Copy the link from the top of your browser.  It should now be a 'privateServerLinkCode' link", title='Unsupported private server link')

    def start(self):
        print("macro object started")

        #enable background threads
        self.nightDetectStreaks = 0
        self.hourlyReport.loadHourlyReportData()
        self.prevMin = -1  
        self.prevSec = -1
        self.multi = self.robloxWindow.multi
        self.lastHourlyReport = 0

        if self.setdat["low_performance"]:
            mergedBackgroundThread = threading.Thread(target=self.mergedBackgrounds, daemon=True)
            mergedBackgroundThread.start()
        else:
            backgroundThread = threading.Thread(target=self.background, daemon=True)
            backgroundThread.start()

            hourlyReportBackgroundThread = threading.Thread(target=self.hourlyReportBackground, daemon=True)
            hourlyReportBackgroundThread.start()
        
        #if roblox is not open, rejoin
        if not appManager.openApp("Roblox"):
            self.rejoin()
        else:
            #toggle fullscreen
            # if not self.isFullScreen():
            #     self.toggleFullScreen()
            self.startDetect()
            self.setRobloxWindowInfo()
    
        if not benchmarkMSS():
            self.logger.webhook("", "MSS is too slow, switching to pillow", "dark brown")
        
        if not self.hourlyReport.hourlyReportStats["start_time"] or not self.hourlyReport.hourlyReportStats["start_honey"]:
            self.hourlyReport.setSessionStats(self.getHoney(), time.time())

        self.reset(convert=True)
        self.saveTiming("rejoin_every")
