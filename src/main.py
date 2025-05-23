
from pynput import keyboard
import multiprocessing
import ctypes
import typing
from threading import Thread
import eel
import time
import sys
import ast
import subprocess
from modules.misc import messageBox
import copy
import atexit
from modules.misc.imageManipulation import adjustImage
from modules.screen.imageSearch import locateImageOnScreen
import pyautogui as pag
mw, mh = pag.size()

def hasteCompensationThread(baseSpeed, isRetina, haste):
    from modules.submacros.hasteCompensation import HasteCompensation
    hasteCompensation = HasteCompensation(isRetina, baseSpeed)
    global stopThreads
    while not stopThreads:
        haste.value = hasteCompensation.getHaste()

def disconnectCheck(run, status, display_type):
    img = adjustImage("./images/menu", "disconnect", display_type)
    while not stopThreads:
        if locateImageOnScreen(img, mw/3, mh/2.8, mw/2.3, mh/5, 0.7):
            print("disconnected")
            run.value = 4
            time.sleep(300) #5 min cd to let the macro run through all 3 rejoins
        time.sleep(1)

#controller for the macro
def macro(status, logQueue, haste, updateGUI):
    print("importing settings manager")
    import modules.misc.settingsManager as settingsManager
    print("importing macro module")
    import modules.macro as macroModule
    print("macro main process started")
    macro = macroModule.macro(status, logQueue, haste, updateGUI)
    #invert the regularMobsInFields dict
    #instead of storing mobs in field, store the fields associated with each mob
    regularMobData = {}
    for k,v in macroModule.regularMobTypesInFields.items():
        for x in v:
            if x in regularMobData:
                regularMobData[x].append(k)
            else:
                regularMobData[x] = [k]
    #Limit werewolf to just pumpkin 
    regularMobData["werewolf"] = ["pumpkin"]
    
    if "share" in macro.setdat["private_server_link"] and macro.setdat["rejoin_method"] == "deeplink":
                messageBox.msgBox(text="You entered a 'share?code' link!\n\nTo fix this:\n1. Paste the link in your browser\n2. Wait for roblox to load in\n3. Copy the link from the top of your browser.  It should now be a 'privateServerLinkCode' link", title='Unsupported private server link')
                return
    macro.start()
    #macro.useItemInInventory("blueclayplanter")
    #function to run a task
    #makes it easy to do any checks after a task is complete (like stinger hunt, rejoin every, etc)
    def runTask(func = None, args = (), resetAfter = True, convertAfter = True):
        #execute the task
        returnVal = func(*args) if func else None
        #task done
        if resetAfter: 
            macro.reset(convert=convertAfter)

        #do priority tasks
        if macro.night and macro.setdat["stinger_hunt"]:
            macro.stingerHunt()
        if macro.setdat["mondo_buff"]:
            macro.collectMondoBuff()
        if macro.setdat["rejoin_every"]:
            if macro.hasRespawned("rejoin_every", macro.setdat["rejoin_every"]*60*60):
                macro.rejoin("Rejoining (Scheduled)")
                macro.saveTiming("rejoin_every")
        
        #auto field boost
        if macro.setdat["Auto_Field_Boost"] and not macro.AFBLIMIT:
            if macro.hasAFBRespawned("AFB_dice_cd", macro.setdat["AFB_rebuff"]*60) or macro.hasAFBRespawned("AFB_glitter_cd", macro.setdat["AFB_rebuff"]*60-30):
                macro.AFB(gatherInterrupt=False)

        status.value = ""
        return returnVal
    
    def handleQuest(questGiver):
        gatherFieldsList = []
        gumdropGatherFieldsList = []
        requireRedField = False
        requireBlueField = False
        requireField = False
        requireBlueGumdropField = False
        requireRedGumdropField = False
        feedBees = []
        setdatEnable = []

        questObjective = macro.findQuest(questGiver)

        if questObjective is None:  # Quest does not exist
            questObjective = macro.getNewQuest(questGiver, False)
        elif not len(questObjective):  # Quest completed
            questObjective = macro.getNewQuest(questGiver, True)
            macro.hourlyReport.addHourlyStat("quests_completed", 1)

        if questObjective is None: #still not able to find quest
            return setdatEnable, gatherFieldsList, gumdropGatherFieldsList, requireRedField, requireBlueField, feedBees, requireRedGumdropField, requireBlueGumdropField, requireField

        for obj in questObjective:
            objData = obj.split("_")
            if objData[0] == "gather":
                gatherFieldsList.append(objData[1])
            elif objData[0] == "gathergoo":
                if macro.setdat["quest_use_gumdrops"]:
                    gumdropGatherFieldsList.append(objData[1])
                else:
                    gatherFieldsList.append(objData[1])
            elif objData[0] == "kill":
                if "ant" in objData[1] and objData[1] != "mantis":
                    setdatEnable.append("ant_challenge")
                    setdatEnable.append("ant_pass_dispenser")
                else:
                    setdatEnable.append(objData[2])
            elif objData[0] == "token":
                if questGiver == "riley bee":
                    requireRedField = True
                elif questGiver == "bucko bee":
                    requireBlueField = True
                else:
                    requireField = True

            elif objData[0] == "token" and objData[1] == "honeytoken":
                setdatEnable.append("honeytoken")
            elif objData[0] == "fieldtoken" and objData[1] == "blueberry":
                requireBlueField = True
            elif objData[0] == "fieldtoken" and objData[1] == "strawberry":
                requireRedField = True
            elif objData[0] == "feed":
                if objData[1] == "*":
                    amount = 25
                else:
                    amount = int(objData[1])
                feedBees.append((objData[2], amount))
            elif objData[0] == "pollen" and objData[1] == "blue":
                requireBlueField = True
            elif objData[0] == "pollen" and objData[1] == "red":
                requireRedField = True
            elif objData[0] == "pollengoo" and objData[1] == "blue":
                if macro.setdat["quest_use_gumdrops"]:
                    requireBlueGumdropField = True
                else:
                    requireBlueField = True
            elif objData[0] == "pollengoo" and objData[1] == "red":
                if macro.setdat["quest_use_gumdrops"]:
                    requireRedGumdropField = True
                else:
                    requireBlueField = True
            elif objData[0] == "collect":
                setdatEnable.append(objData[1].replace("-","_"))
        
        return setdatEnable, gatherFieldsList, gumdropGatherFieldsList, requireRedField, requireBlueField, feedBees, requireRedGumdropField, requireBlueGumdropField, requireField

    #macro.rejoin()
    while True:
        macro.setdat = settingsManager.loadAllSettings()
        #run empty task
        #this is in case no other settings are selected 
        runTask(resetAfter=False)

        #handle quests
        questGatherFields = []
        questGumdropGatherFields = []
        redFieldNeeded = False
        blueFieldNeeded = False
        fieldNeeded = False
        itemsToFeedBees = []
        redGumdropFieldNeeded = False
        blueGumdropFieldNeeded = False

        for questName, enabledKey in [
            ("polar bear", "polar_bear_quest"),
            ("honey bee", "honey_bee_quest"),
            ("bucko bee", "bucko_bee_quest"),
            ("riley bee", "riley_bee_quest")
        ]:
            if macro.setdat.get(enabledKey):
                setdatEnable, gatherFields, gumdropFields, needsRed, needsBlue, feedBees, needsRedGumdrop, needsBlueGumdrop, needsField = handleQuest(questName)
                for k in setdatEnable:
                    macro.setdat[k] = True
                questGatherFields.extend(gatherFields)
                questGumdropGatherFields.extend(gumdropFields)
                redFieldNeeded = redFieldNeeded or needsRed
                blueFieldNeeded = blueFieldNeeded or needsBlue
                itemsToFeedBees.extend(feedBees)
                redGumdropFieldNeeded = redGumdropFieldNeeded or needsRedGumdrop
                blueGumdropFieldNeeded = blueGumdropFieldNeeded or needsBlueGumdrop
                fieldNeeded = fieldNeeded or needsField
        
        #feed bees for quest
        for item, quantity in itemsToFeedBees:
            macro.feedBee(item, quantity)
                    
        #collect
        for k, _ in macroModule.collectData.items():
            #check if the cooldown is up
            if macro.setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]):
                runTask(macro.collect, args=(k,))

        if macro.setdat["sticker_printer"] and macro.hasRespawned("sticker_printer", macro.collectCooldowns["sticker_printer"]):
            runTask(macro.collectStickerPrinter)
        #blender
        if macro.setdat["blender_enable"]:
            with open("./data/user/blender.txt", "r") as f:
                blenderData = ast.literal_eval(f.read())
            f.close()
            #collectTime: time where the blender is done crafting
            #item: the next item number to craft
            #check if its time to collect the previous item
            if blenderData["collectTime"] > -1 and time.time() > blenderData["collectTime"]:
                runTask(macro.blender, args=(blenderData,))

        #planters
        def goToNextCycle(cycle, slot):
            #go to the next cycle
            for _ in range(8):
                cycle += 1
                if cycle > 5:
                    cycle = 1
                if macro.setdat[f"cycle{cycle}_{slot+1}_planter"] != "none" and macro.setdat[f"cycle{cycle}_{slot+1}_field"] != "none":
                    return cycle
            else: 
                return False
        
        planterDataRaw = None
        if macro.setdat["planters_mode"] == 1:
            with open("./data/user/manualplanters.txt", "r") as f:
                planterDataRaw = f.read()
            f.close()
            #no data, place planters
            if not planterDataRaw:
                runTask(macro.placeAllPlantersInCycle, args = (1,),resetAfter=False)
            #planter data does exist, check if its time to collect them
            else: 
                planterData = ast.literal_eval(planterDataRaw)
                planterChanged = False
                #check all 3 slots
                for i in range(3):
                    cycle = planterData["cycles"][i]
                    if time.time() > planterData["harvestTimes"][i] and planterData["planters"][i]:
                        #Collect planters
                        runTask(macro.collectPlanter, args=(planterData["planters"][i], planterData["fields"][i]))
                        #go to the next cycle
                        cycle = goToNextCycle(cycle, i)
                        #place them
                        planterData = runTask(macro.placePlanterInCycle, args = (i, cycle, planterData),resetAfter=False)
                        planterChanged = True
                if planterChanged:
                    #save the planter data
                    # with open("./data/user/manualplanters.txt", "w") as f:
                    #     f.write(str(planterData))
                    # f.close()
                    pass
                 
        #mob run
        for mob, fields in regularMobData.items():
            if not macro.setdat[mob]: continue
            for f in fields:
                if macro.hasMobRespawned(mob, f):
                    runTask(macro.killMob, args=(mob, f,), convertAfter=False)
        #ant challenge
        if macro.setdat["ant_challenge"]: 
            runTask(macro.antChallenge)

        #coconut crab
        if macro.setdat["coconut_crab"] and macro.hasRespawned("coconut_crab", 36*60*60, applyMobRespawnBonus=True):
            macro.coconutCrab()
            
        #stump snail
        if macro.setdat["stump_snail"] and macro.hasRespawned("stump_snail", 96*60*60, applyMobRespawnBonus=True):
            runTask(macro.stumpSnail)
        
        #sticker stack
        if macro.setdat["sticker_stack"]:
            with open("./data/user/sticker_stack.txt", "r") as f:
                stickerStackCD = int(f.read())
            f.close()
            if macro.hasRespawned("sticker_stack", stickerStackCD):
                runTask(macro.collect, args=("sticker_stack",))
        #field boosters
        boostedGatherFields = []
        for k, _ in macroModule.fieldBoosterData.items():
            #check if the cooldown is up
            if macro.setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]) and macro.hasRespawned("last_booster", macro.setdat["boost_seperate"]*60):
                boostedField = runTask(macro.collect, args=(k,))
                if macro.setdat["gather_boosted"] and boostedField:
                    boostedGatherFields.append(boostedField)

        allGatheredFields = []
        allGatheredFields.extend(boostedGatherFields)
        #gather in boosted fields
        #gather for the entire 15min duration
        for field in boostedGatherFields:
            st = time.time()
            while time.time() - st < 15*60:
                runTask(macro.gather, args=(field,), resetAfter=False)

        #add gather tab fields
        gatherFields = []
        for i in range(3):
            if macro.setdat["fields_enabled"][i]:
                gatherFields.append(macro.setdat["fields"][i])
        
        #add planter gather fields
        if planterDataRaw:
            planterGatherFields = [x for x in ast.literal_eval(planterDataRaw)["gatherFields"] if x]
        else:
            planterGatherFields = []
        gatherFields.extend([x for x in planterGatherFields if x not in gatherFields])

        #remove fields that are already in boosted fields
        gatherFields = [x for x in gatherFields if not x in boostedGatherFields]

        allGatheredFields.extend(gatherFields)
        
        for field in gatherFields:
            runTask(macro.gather, args=(field,), resetAfter=False)

        #do quests

        blueFields = ["blue flower", "bamboo", "pine tree", "stump"]
        redFields = ["mushroom", "strawberry", "rose", "pepper"]

        #setup the override
        questGatherOverrides = {}
        if macro.setdat["quest_gather_mins"]:
            questGatherOverrides["mins"] = macro.setdat["quest_gather_mins"]
        if macro.setdat["quest_gather_return"] != "no override":
            questGatherOverrides["return"] = macro.setdat["quest_gather_return"]
            

        #do goo-field gathers first
        if blueGumdropFieldNeeded:
            for f in blueFields:
                if f in questGumdropGatherFields:
                    break
            else:
                questGumdropGatherFields.append("pine tree")
        
        if redGumdropFieldNeeded:
            for f in redFields:
                if f in questGumdropGatherFields:
                    break
            else:
                questGumdropGatherFields.append("rose")

        for field in questGumdropGatherFields:
            runTask(macro.gather, args=(field, questGatherOverrides, True), resetAfter=False)
        allGatheredFields.extend(questGumdropGatherFields)


        #do regular gathers
        questGatherFields = [x for x in questGatherFields if not (x in allGatheredFields)]
        for field in questGatherFields:
            runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
        allGatheredFields.extend(questGatherFields)

        #do required blue/red fields
        if blueFieldNeeded:
            for f in blueFields:
                if f in allGatheredFields:
                    break
            else:
                field = "pine tree"
                allGatheredFields.append(field)
                runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
        
        if redFieldNeeded:
            for f in redFields:
                if f in allGatheredFields:
                    break
            else:
                field = "rose"
                allGatheredFields.append(field)
                runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
        
        if fieldNeeded and not allGatheredFields:
            runTask(macro.gather, args=("pine tree",), resetAfter=False)
        
        


def watch_for_hotkeys(run):
    def on_press(key):
        nonlocal run
        if key == keyboard.Key.f1:
            
            if run.value == 2: #already running
                print("Already running")
                return 
            run.value = 1
        elif key == keyboard.Key.f3:
            if run.value == 3: #already stopped
                print("Already stopped")
                return
            run.value = 0

    keyboard.Listener(on_press=on_press).start()

if __name__ == "__main__":
    print("Loading gui...")
    global stopThreads, macroProc
    import gui
    import modules.screen.screenData as screenData
    from modules.controls.keyboard import keyboard as keyboardModule
    import modules.logging.log as logModule
    import modules.controls.mouse as mouse
    import modules.misc.appManager as appManager
    import modules.misc.settingsManager as settingsManager
    from modules.discord_bot.discordBot import discordBot
    from modules.submacros.convertAhkPattern import ahkPatternToPython
    from modules.submacros.stream import cloudflaredStream
    import os

    if sys.platform == "darwin" and sys.version_info[1] <= 7:
        print("start method set to spawn")
        multiprocessing.set_start_method("spawn")
    macroProc = None
    #set screen data
    screenData.setScreenData()
    screenInfo = screenData.getScreenData()
    #value to control if macro main loop is running
    #0: stop (terminate process)
    #1: start (start process)
    #2: already running (do nothing)
    #3: already stopped (do nothing)
    manager = multiprocessing.Manager()
    run = multiprocessing.Value('i', 3)
    updateGUI = multiprocessing.Value('i', 0)
    status = manager.Value(ctypes.c_wchar_p, "none")
    logQueue = manager.Queue()
    haste = multiprocessing.Value('d', 0)
    watch_for_hotkeys(run)
    logger = logModule.log(logQueue, False, None, blocking=True)

    disconnectCooldownUntil = 0 #only for running disconnect check on low performance

    #update settings
    profileSettings = settingsManager.loadSettings()
    profileSettingsReference = settingsManager.readSettingsFile("./data/default_settings/settings.txt")
    settingsManager.saveDict("../settings/profiles/a/settings.txt", {**profileSettingsReference, **profileSettings})

    #update general settings
    generalSettings = settingsManager.readSettingsFile("../settings/generalsettings.txt")
    generalSettingsReference = settingsManager.readSettingsFile("./data/default_settings/generalsettings.txt")
    settingsManager.saveDict("../settings/generalsettings.txt", {**generalSettingsReference, **generalSettings})

    #convert ahk pattern
    ahkPatterns = [x for x in os.listdir("../settings/patterns") if ".ahk" in x]
    for pattern in ahkPatterns:
        with open(f"../settings/patterns/{pattern}", "r") as f:
            ahk = f.read()
        f.close()
        python = ahkPatternToPython(ahk)
        print(f"Converted: {pattern}")
        patternName = pattern.rsplit(".", 1)[0].lower()
        with open(f"../settings/patterns/{patternName}.py", "w") as f:
            f.write(python)
        f.close()
    
    #setup stream class
    stream = cloudflaredStream()

    def onExit():
        stopApp()
        if discordBotProc and discordBotProc.is_alive():
            discordBotProc.terminate()
            discordBotProc.join()
        
    def stopApp(page= None, sockets = None):
        global stopThreads
        global macroProc
        stopThreads = True
        print("stop")
        #print(sockets)
        if macroProc and macroProc.is_alive():
            macroProc.kill()
            macroProc.join()
            macroProc = None
        stream.stop()
        #if discordBotProc.is_alive(): discordBotProc.kill()
        keyboardModule.releaseMovement()
        mouse.mouseUp()
    
    atexit.register(onExit)
        
    #setup and launch gui
    gui.run = run
    gui.launch()
    #use run.value to control the macro loop

    #check color profile
    if sys.platform == "darwin":
        try:
            cmd = """
                osascript -e 'tell application "Image Events" to display profile of display 1' 
                """
            colorProfile = subprocess.check_output(cmd, shell=True).decode(sys.stdout.encoding)
            colorProfile = colorProfile.strip()
            if colorProfile == "missing value": colorProfile = "Color LCD"
            if not "sRGB IEC61966" in colorProfile:
                messageBox.msgBox(text = f"Your current color profile is {colorProfile}.The required one is sRGB IEC61966-2.1.\
                \nThis is necessary for the macro to work\
                \nTVisit step 6 of the macro installation guide in the discord for instructions", title="Wrong Color Profile")
        except:
            pass

    discordBotProc = None
    prevDiscordBotToken = None

    while True:
        eel.sleep(0.5)
        setdat = settingsManager.loadAllSettings()

        #discord bot. Look for changes in the bot token
        currentDiscordBotToken = setdat["discord_bot_token"]
        if setdat["discord_bot"] and currentDiscordBotToken and currentDiscordBotToken != prevDiscordBotToken:
            if discordBotProc is not None and discordBotProc.is_alive():
                print("Detected change in discord bot token, killing previous bot process")
                discordBotProc.terminate()
                discordBotProc.join()
            discordBotProc = multiprocessing.Process(target=discordBot, args=(currentDiscordBotToken, run, status), daemon=True)
            prevDiscordBotToken = currentDiscordBotToken
            discordBotProc.start()

        if run.value == 1:
            print("start")
            #create and set webhook obj for the logger
            logger.enableWebhook = setdat["enable_webhook"]
            logger.webhookURL = setdat["webhook_link"]
            haste.value = setdat["movespeed"]
            stopThreads = False
            print("variables initalised")

            #stream
            def waitForStreamURL():
                #wait for up to 15 seconds for the public link
                for _ in range(150):
                    time.sleep(0.1)
                    if stream.publicURL:
                        logger.webhook("Stream Started", f'Stream URL: {stream.publicURL}', "purple")
                        return
            
                logger.webhook("", f'Stream could not start. Check terminal for more info', "red")

            print("checking stream")
            streamLink = None
            if setdat["enable_stream"]:
                print("stream enabled")
                logger.webhook("", "Starting Stream...", "light blue")
                streamLink = stream.start(setdat["stream_resolution"])
                Thread(target=waitForStreamURL, daemon=True).start()

            print("starting macro proc")
            #macro proc
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, haste, updateGUI), daemon=True)
            macroProc.start()

            #haste compensation
            if setdat["haste_compensation"]:
                hasteCompThread = Thread(target=hasteCompensationThread, args=(setdat["movespeed"], screenInfo["display_type"] == "retina", haste,))
                hasteCompThread.daemon = True
                hasteCompThread.start()

            logger.webhook("Macro Started", f'Existance Macro v2.0\nDisplay: {screenInfo["display_type"]}, {screenInfo["screen_width"]}x{screenInfo["screen_height"]}', "purple")
            run.value = 2
            gui.toggleStartStop()
        elif run.value == 0:
            if macroProc:
                logger.webhook("Macro Stopped", "exih macro", "red")
                run.value = 3
                gui.toggleStartStop()
                stopApp()
        elif run.value == 4: #disconnected
            macroProc.kill()
            logger.webhook("","Disconnected", "red", "screen")
            appManager.closeApp("Roblox")
            keyboardModule.releaseMovement()
            mouse.mouseUp()
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, haste, updateGUI), daemon=True)
            macroProc.start()
            run.value = 2

        #detect a new log message
        if not logQueue.empty():
            logData = logQueue.get()
            if logData["type"] == "webhook": #webhook
                msg = f"{logData['title']}<br>{logData['desc']}"

            #add it to gui
            gui.log(logData["time"], msg, logData["color"])
        
        #detect if the gui needs to be updated
        if updateGUI.value:
            gui.updateGUI()
            updateGUI.value = 0
        
        if run.value == 2 and time.time() > disconnectCooldownUntil:
            img = adjustImage("./images/menu", "disconnect", screenInfo["display_type"])
            if locateImageOnScreen(img, mw/3, mh/2.8, mw/2.3, mh/5, 0.7):
                print("disconnected")
                run.value = 4
                disconnectCooldownUntil = time.time() + 300  # 5 min cooldown
    
            
            
            
