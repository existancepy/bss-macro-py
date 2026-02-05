
from modules.misc import messageBox
#check if step 3 installing dependencies was ran
try:
    import requests
except ModuleNotFoundError:
    messageBox.msgBox(title="Dependencies not installed", text="It seems like you have not finished step 3 of the installation process. Refer to https://existance-macro.gitbook.io/existance-macro-docs/macro-installation/markdown/2.-installing-dependencies")
from pynput import keyboard
import multiprocessing
import ctypes
from threading import Thread
import eel
import time
import sys
import os
import ast
import subprocess
import atexit
from modules.misc.imageManipulation import adjustImage
from modules.screen.imageSearch import locateImageOnScreen
import pyautogui as pag
from modules.misc.appManager import getWindowSize
import traceback
import modules.misc.settingsManager as settingsManager
import modules.macro as macroModule
import modules.controls.mouse as mouse
import json

try:
	from modules.misc.ColorProfile import DisplayColorProfile
except ModuleNotFoundError:
	messageBox.msgBox(title="Dependencies not installed", text="The new update requires new dependencies. Refer to https://existance-macro.gitbook.io/existance-macro-docs/macro-installation/markdown/2.-installing-dependencies.")
	quit()
from modules.submacros.hourlyReport import HourlyReport
mw, mh = pag.size()

#controller for the macro
def macro(status, logQueue, updateGUI, run, skipTask):
    macro = macroModule.macro(status, logQueue, updateGUI, run, skipTask)
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
    
    private_server_link = macro.setdat.get("private_server_link", "")
    if private_server_link and "share" in private_server_link and macro.setdat.get("rejoin_method") == "deeplink":
                messageBox.msgBox(text="You entered a 'share?code' link!\n\nTo fix this:\n1. Paste the link in your browser\n2. Wait for roblox to load in\n3. Copy the link from the top of your browser.  It should now be a 'privateServerLinkCode' link", title='Unsupported private server link')
                return

    taskCompleted = True
    questCache = {}
    
    macro.start()
    #macro.useItemInInventory("blueclayplanter")
    #function to run a task
    #makes it easy to do any checks after a task is complete (like stinger hunt, rejoin every, etc)
    def runTask(func = None, args = (), resetAfter = True, convertAfter = True):
        nonlocal taskCompleted
        # Check if skip was requested
        if skipTask.value == 1:
            skipTask.value = 0  # Reset skip flag
            macro.logger.webhook("Task Skipped", f"Skipped: {status.value.replace('_', ' ').title()}", "orange")
            status.value = ""
            taskCompleted = True
            if resetAfter:
                macro.reset(convert=False)
            return None
        
        #execute the task
        if func:
            returnVal = func(*args) 
            taskCompleted = True
        else:
            returnVal = None
        #task done
        if resetAfter: 
            macro.reset(convert=convertAfter)
        
        #do priority tasks
        if macro.night and macro.setdat["stinger_hunt"]:
            macro.stingerHunt()
        if macro.setdat["mondo_buff"] and macro.hasMondoRespawned():
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
    
    def handleQuest(questGiver, executeQuest=True):
        nonlocal questCache, taskCompleted
        
        gatherFieldsList = []
        gumdropGatherFieldsList = []
        requireRedField = False
        requireBlueField = False
        requireField = False
        requireBlueGumdropField = False
        requireRedGumdropField = False
        feedBees = []
        setdatEnable = []

        #if the macro has completed a task in the last cycle
        if taskCompleted or not questGiver in questCache:
            questObjective = macro.findQuest(questGiver)
            questCache[questGiver] = questObjective
        else:
            questObjective = questCache[questGiver]

        # Only submit/get quests if executeQuest is True (when quest appears in priority queue)
        if executeQuest:
            if questObjective is None:  # Quest does not exist
                questObjective = macro.getNewQuest(questGiver, False)
            elif not len(questObjective):  # Quest completed
                questObjective = macro.getNewQuest(questGiver, True)
                macro.hourlyReport.addHourlyStat("quests_completed", 1)
        else:
            # If not executing, use cached quest or return empty if no quest exists or is completed
            if questObjective is None or not len(questObjective):
                # No quest found or quest completed - we're not executing, so we can't determine requirements
                # Return empty requirements (will be determined when quest executes in priority order)
                return setdatEnable, gatherFieldsList, gumdropGatherFieldsList, requireRedField, requireBlueField, feedBees, requireRedGumdropField, requireBlueGumdropField, requireField

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
    # Cache settings to avoid reloading on every iteration
    settings_cache = {}
    last_settings_load = 0
    settings_cache_duration = 0.5  # Reload settings every 0.5 seconds max
    
    def get_cached_settings():
        nonlocal settings_cache, last_settings_load
        current_time = time.time()
        if current_time - last_settings_load > settings_cache_duration:
            settings_cache = settingsManager.loadAllSettings()
            last_settings_load = current_time
        return settings_cache
    
    while True:
        # Check for pause request (state 5) - release inputs and transition to paused
        if run.value == 5:
            macro.keyboard.releaseMovement()
            mouse.mouseUp()
            run.value = 6  # Transition to paused state
        # Check for pause - wait while paused
        while run.value == 6:  # 6 = paused
            time.sleep(0.1)  # Wait while paused
        # Check if stop was requested while paused
        if run.value == 0:
            break  # Exit macro loop if stop requested
        
        macro.setdat = get_cached_settings()
        # Check if profile has changed and reload settings if needed
        macro.checkAndReloadSettings()

        # Migration from old boolean flags to macro_mode is now handled in settings loader

        #run empty task
        #this is in case no other settings are selected
        runTask(resetAfter=False)

        updateGUI.value = 1

        # Check if field-only mode is enabled
        if macro.setdat.get("macro_mode", "normal") == "field":
            # Field-only mode: skip all tasks except field gathering
            # Get priority order and filter to only include enabled field gathering tasks
            priorityOrder = macro.setdat.get("task_priority_order", [])
            executedTasks = set()

            # Filter priority order to only include gather tasks for enabled fields
            fieldOnlyTasks = []
            for taskId in priorityOrder:
                if taskId.startswith("gather_"):
                    fieldName = taskId.replace("gather_", "").replace("_", " ")
                    # Check if this field is enabled
                    for i in range(len(macro.setdat["fields_enabled"])):
                        if macro.setdat["fields_enabled"][i] and macro.setdat["fields"][i] == fieldName:
                            fieldOnlyTasks.append(taskId)
                            break

            # If no gather tasks are in priority order, fall back to sequential order of enabled fields
            if not fieldOnlyTasks:
                for i in range(len(macro.setdat["fields_enabled"])):
                    if macro.setdat["fields_enabled"][i]:
                        field = macro.setdat["fields"][i]
                        fieldOnlyTasks.append(f"gather_{field.replace(' ', '_')}")

            # Execute field gathering tasks in priority order
            for taskId in fieldOnlyTasks:
                if taskId.startswith("gather_"):
                    fieldName = taskId.replace("gather_", "").replace("_", " ")
                    if taskId not in executedTasks:
                        runTask(macro.gather, args=(fieldName,), resetAfter=False)
                        executedTasks.add(taskId)

            # Skip to next iteration
            continue

        # Check if quest-only mode is enabled
        if macro.setdat.get("macro_mode", "normal") == "quest":
            # Quest-only mode: skip all tasks except quest-related tasks
            # Initialize quest-related variables
            questGatherFields = []
            questGumdropGatherFields = []
            redFieldNeeded = False
            blueFieldNeeded = False
            fieldNeeded = False
            itemsToFeedBees = []
            redGumdropFieldNeeded = False
            blueGumdropFieldNeeded = False

            # Get priority order and filter to only include quest tasks
            priorityOrder = macro.setdat.get("task_priority_order", [])
            executedTasks = set()

            # Filter priority order to only include quest tasks
            questOnlyTasks = []
            for taskId in priorityOrder:
                if taskId.startswith("quest_"):
                    questOnlyTasks.append(taskId)

            # If no quest tasks are in priority order, add all enabled quests
            if not questOnlyTasks:
                questMappings = [
                    ("polar bear", "polar_bear_quest"),
                    ("honey bee", "honey_bee_quest"),
                    ("bucko bee", "bucko_bee_quest"),
                    ("riley bee", "riley_bee_quest")
                ]
                for questName, questKey in questMappings:
                    if macro.setdat.get(questKey):
                        questOnlyTasks.append(f"quest_{questName.replace(' ', '_')}")

            # Execute quest tasks in priority order
            for taskId in questOnlyTasks:
                if taskId.startswith("quest_"):
                    questName = taskId.replace("quest_", "").replace("_", " ")
                    questKey = f"{questName.replace(' ', '_')}_quest"
                    if macro.setdat.get(questKey):
                        # Handle quest feeding and gathering requirements
                        questMappings = {
                            "polar bear": "polar_bear_quest",
                            "honey bee": "honey_bee_quest",
                            "bucko bee": "bucko_bee_quest",
                            "riley bee": "riley_bee_quest"
                        }

                        if questName in questMappings:
                            enabledKey = questMappings[questName]
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

                        if taskId not in executedTasks:
                            executedTasks.add(taskId)

            # Feed bees for quests (done once per cycle)
            for item, quantity in itemsToFeedBees:
                macro.feedBee(item, quantity)
                taskCompleted = True

            # Handle quest gather fields (done once per cycle)
            questGatherOverrides = {}
            if macro.setdat["quest_gather_mins"]:
                questGatherOverrides["mins"] = macro.setdat["quest_gather_mins"]
            if macro.setdat["quest_gather_return"] != "no override":
                questGatherOverrides["return"] = macro.setdat["quest_gather_return"]

            allGatheredFields = []

            # Handle gumdrop gather fields first
            if blueGumdropFieldNeeded:
                blueFields = ["blue flower", "bamboo", "pine tree", "stump"]
                for f in blueFields:
                    if f in questGumdropGatherFields:
                        break
                else:
                    questGumdropGatherFields.append("pine tree")

            if redGumdropFieldNeeded:
                redFields = ["mushroom", "strawberry", "rose", "pepper"]
                for f in redFields:
                    if f in questGumdropGatherFields:
                        break
                else:
                    questGumdropGatherFields.append("rose")

            for field in questGumdropGatherFields:
                if field not in allGatheredFields:
                    runTask(macro.gather, args=(field, questGatherOverrides, True), resetAfter=False)
                    allGatheredFields.append(field)

            # Handle regular quest gather fields
            questGatherFields = [x for x in questGatherFields if not (x in allGatheredFields)]
            for field in questGatherFields:
                runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
                allGatheredFields.append(field)

            # Handle required blue/red fields for quests
            blueFields = ["blue flower", "bamboo", "pine tree", "stump"]
            redFields = ["mushroom", "strawberry", "rose", "pepper"]

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

            # Skip to next iteration
            continue

        # Check quest requirements for ALL enabled quests (needed for quest-related gathering fields)
        # But only feed bees for quests that appear in priority queue order
        questGatherFields = []
        questGumdropGatherFields = []
        redFieldNeeded = False
        blueFieldNeeded = False
        fieldNeeded = False
        itemsToFeedBees = []
        redGumdropFieldNeeded = False
        blueGumdropFieldNeeded = False
        
        # Track which quests have been executed in priority order (for feeding bees)
        executedQuests = set()
        
        # Store quest feed requirements per quest (to feed only when quest appears in priority)
        questFeedRequirements = {}

        # Check ALL enabled quests for requirements (to know what fields might be needed)
        # But don't execute quests (submit/get) - that will happen when quest appears in priority queue
        for questName, enabledKey in [
            ("polar bear", "polar_bear_quest"),
            ("honey bee", "honey_bee_quest"),
            ("bucko bee", "bucko_bee_quest"),
            ("riley bee", "riley_bee_quest")
        ]:
            if macro.setdat.get(enabledKey):
                # Check requirements without executing (submit/get) the quest
                setdatEnable, gatherFields, gumdropFields, needsRed, needsBlue, feedBees, needsRedGumdrop, needsBlueGumdrop, needsField = handleQuest(questName, executeQuest=False)
                # Enable any required settings
                for k in setdatEnable:
                    macro.setdat[k] = True
                # Store gather fields (will be used after priority queue)
                questGatherFields.extend(gatherFields)
                questGumdropGatherFields.extend(gumdropFields)
                redFieldNeeded = redFieldNeeded or needsRed
                blueFieldNeeded = blueFieldNeeded or needsBlue
                redGumdropFieldNeeded = redGumdropFieldNeeded or needsRedGumdrop
                blueGumdropFieldNeeded = blueGumdropFieldNeeded or needsBlueGumdrop
                fieldNeeded = fieldNeeded or needsField
                # Store feed requirements (will be used when quest appears in priority queue)
                questFeedRequirements[questName] = feedBees
        
                    
        taskCompleted = False

        # Helper function for manual planters
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
        
        # Get priority order from settings, or use empty list if not set
        priorityOrder = macro.setdat.get("task_priority_order", [])
        
        # Track which tasks have been executed to avoid duplicates
        executedTasks = set()
        
        # Track planter data for gather fields
        planterDataRaw = None
        
        # Helper function to execute a task by its ID
        def executeTask(taskId):
            nonlocal planterDataRaw, executedTasks, taskCompleted
            
            # Skip if already executed
            if taskId in executedTasks:
                return False
            
            # Handle quest tasks - execute quest (submit/get) and feed bees when quest appears in priority order
            if taskId.startswith("quest_"):
                questName = taskId.replace("quest_", "").replace("_", " ")
                questKey = f"{questName.replace(' ', '_')}_quest"
                if not macro.setdat.get(questKey):
                    return False
                
                # Actually execute the quest (submit/get) - this will travel to quest giver if needed
                handleQuest(questName, executeQuest=True)
                
                # Feed bees for this quest (requirements were already checked above)
                if questName in questFeedRequirements:
                    feedBees = questFeedRequirements[questName]
                    for item, quantity in feedBees:
                        macro.feedBee(item, quantity)
                        taskCompleted = True
                
                executedTasks.add(taskId)
                executedQuests.add(questName)
                return True
            
            # Handle collect tasks
            if taskId.startswith("collect_"):
                collectName = taskId.replace("collect_", "")
                
                # Special case: sticker_printer
                if collectName == "sticker_printer":
                    if macro.setdat["sticker_printer"] and macro.hasRespawned("sticker_printer", macro.collectCooldowns["sticker_printer"]):
                        runTask(macro.collectStickerPrinter)
                        executedTasks.add(taskId)
                        return True
                    return False
                
                # Special case: sticker_stack
                if collectName == "sticker_stack":
                    if macro.setdat["sticker_stack"]:
                        with open("./data/user/sticker_stack.txt", "r") as f:
                            stickerStackCD = int(f.read())
                        f.close()
                        if macro.hasRespawned("sticker_stack", stickerStackCD):
                            runTask(macro.collect, args=("sticker_stack",))
                            executedTasks.add(taskId)
                            return True
                    return False
                
                # Field boosters (handled separately due to gather logic)
                if collectName in ["blue_booster", "red_booster", "mountain_booster"]:
                    if collectName in macroModule.fieldBoosterData:
                        if macro.setdat[collectName] and macro.hasRespawned(collectName, macro.collectCooldowns[collectName]) and macro.hasRespawned("last_booster", macro.setdat["boost_seperate"]*60):
                            boostedField = runTask(macro.collect, args=(collectName,))
                            if macro.setdat["gather_boosted"] and boostedField:
                                # Gather in boosted field for 15 minutes
                                st = time.time()
                                while time.time() - st < 15*60:
                                    runTask(macro.gather, args=(boostedField,), resetAfter=False)
                            executedTasks.add(taskId)
                            return True
                    return False
                
                # Regular collect items
                if collectName in macroModule.collectData:
                    if macro.setdat[collectName] and macro.hasRespawned(collectName, macro.collectCooldowns[collectName]):
                        runTask(macro.collect, args=(collectName,))
                        executedTasks.add(taskId)
                        return True
                return False
            
            # Handle kill tasks
            if taskId.startswith("kill_"):
                mob = taskId.replace("kill_", "")
                
                # Special cases: coconut_crab and stump_snail
                if mob == "coconut_crab":
                    if macro.setdat["coconut_crab"] and macro.hasRespawned("coconut_crab", 36*60*60, applyMobRespawnBonus=True):
                        macro.coconutCrab()
                        executedTasks.add(taskId)
                        return True
                    return False
                
                if mob == "stump_snail":
                    if macro.setdat["stump_snail"] and macro.hasRespawned("stump_snail", 96*60*60, applyMobRespawnBonus=True):
                        runTask(macro.stumpSnail)
                        executedTasks.add(taskId)
                        return True
                    return False
                
                # Regular mobs
                if mob in regularMobData:
                    if macro.setdat[mob]:
                        # Check all fields for this mob and kill in each field where it has respawned
                        # We need to check ALL fields before moving to the next task
                        killedInAnyField = False
                        for f in regularMobData[mob]:
                            if macro.hasMobRespawned(mob, f):
                                runTask(macro.killMob, args=(mob, f,), convertAfter=False)
                                killedInAnyField = True
                                # After killing in one field, return True to trigger re-check
                                # This allows the outer loop to iterate again and check remaining fields
                                return True
                        # If we checked all fields and none had respawned mobs, return False
                        # This will allow the loop to move to the next task
                        return False
                return False
            
            # Handle gather tasks
            if taskId.startswith("gather_"):
                fieldName = taskId.replace("gather_", "").replace("_", " ")
                
                # Check if this field is enabled in gather tab
                for i in range(len(macro.setdat["fields_enabled"])):
                    if macro.setdat["fields_enabled"][i] and macro.setdat["fields"][i] == fieldName:
                        runTask(macro.gather, args=(fieldName,), resetAfter=False)
                        executedTasks.add(taskId)
                        return True
                
                # Check if it's a quest gather field
                if fieldName in questGatherFields or fieldName in questGumdropGatherFields:
                    questGatherOverrides = {}
                    if macro.setdat["quest_gather_mins"]:
                        questGatherOverrides["mins"] = macro.setdat["quest_gather_mins"]
                    if macro.setdat["quest_gather_return"] != "no override":
                        questGatherOverrides["return"] = macro.setdat["quest_gather_return"]
                    
                    isGumdrop = fieldName in questGumdropGatherFields
                    runTask(macro.gather, args=(fieldName, questGatherOverrides, isGumdrop), resetAfter=False)
                    executedTasks.add(taskId)
                    return True
                
                return False
            
            # Handle special tasks
            if taskId == "blender":
                if macro.setdat["blender_enable"]:
                    with open("./data/user/blender.txt", "r") as f:
                        blenderData = ast.literal_eval(f.read())
                    f.close()
                    if blenderData["collectTime"] > -1 and time.time() > blenderData["collectTime"]:
                        runTask(macro.blender, args=(blenderData,))
                        executedTasks.add(taskId)
                        return True
                return False
            
            if taskId == "planters":
                if not macro.setdat["planters_mode"]:
                    return False
                
                # Manual planters
                if macro.setdat["planters_mode"] == 1:
                    if planterDataRaw is None:
                        with open("./data/user/manualplanters.txt", "r") as f:
                            planterDataRaw = f.read()
                        f.close()
                    
                    if not planterDataRaw.strip():
                        planterData = {
                            "cycles": [1,1,1],
                            "planters": ["","",""],
                            "fields": ["","",""],
                            "gatherFields": ["","",""],
                            "harvestTimes": [0,0,0]
                        }
                        for i in range(3):
                            if macro.setdat[f"cycle1_{i+1}_planter"] == "none" or macro.setdat[f"cycle1_{i+1}_field"] == "none":
                                continue
                            planter = runTask(macro.placePlanterInCycle, args = (i, 1),resetAfter=False)
                            if planter:
                                planterData["planters"][i] = planter[0]
                                planterData["fields"][i] = planter[1]
                                planterData["harvestTimes"][i] = planter[2]
                                planterData["gatherFields"][i] = planter[1] if planter[3] else ""
                                with open("./data/user/manualplanters.txt", "w") as f:
                                    f.write(str(planterData))
                                f.close()
                        executedTasks.add(taskId)
                        return True
                    else:
                        planterData = ast.literal_eval(planterDataRaw)
                        for i in range(3):
                            cycle = planterData["cycles"][i]
                            if planterData["planters"][i] and time.time() > planterData["harvestTimes"][i]:
                                if runTask(macro.collectPlanter, args=(planterData["planters"][i], planterData["fields"][i])):
                                    planterData["harvestTimes"][i] = ""
                                    planterData["planters"][i] = ""
                                    planterData["fields"][i] = ""
                                    with open("./data/user/manualplanters.txt", "w") as f:
                                        f.write(str(planterData))
                                    f.close()
                                    updateGUI.value = 1
                        
                        for i in range(3):
                            cycle = planterData["cycles"][i]
                            if planterData["planters"][i]:
                                continue
                            nextCycle = goToNextCycle(cycle, i)
                            if not nextCycle:
                                continue
                            
                            planterToPlace = macro.setdat[f"cycle{nextCycle}_{i+1}_planter"]
                            otherSlotPlanters = planterData["planters"][:i] + planterData["planters"][i+1:]
                            if planterToPlace in otherSlotPlanters:
                                continue
                            
                            fieldToPlace = macro.setdat[f"cycle{nextCycle}_{i+1}_field"]
                            otherSlotFields = planterData["fields"][:i] + planterData["fields"][i+1:]
                            if fieldToPlace in otherSlotFields:
                                continue
                            
                            planter = runTask(macro.placePlanterInCycle, args = (i, nextCycle),resetAfter=False)
                            if planter:
                                planterData["cycles"][i] = nextCycle
                                planterData["planters"][i] = planter[0]
                                planterData["fields"][i] = planter[1]
                                planterData["harvestTimes"][i] = planter[2]
                                planterData["gatherFields"][i] = planter[1] if planter[3] else ""
                                with open("./data/user/manualplanters.txt", "w") as f:
                                    f.write(str(planterData))
                                f.close()
                                updateGUI.value = 1
                        executedTasks.add(taskId)
                        return True
                
                # Auto planters
                elif macro.setdat["planters_mode"] == 2:
                    with open("./data/user/auto_planters.json", "r") as f:
                        data = json.load(f)
                        planterData = data["planters"]
                        nectarLastFields = data["nectar_last_field"]
                    f.close()

                    def saveAutoPlanterData():
                        data = {
                            "planters": planterData,
                            "nectar_last_field": nectarLastFields,
                        }
                        with open("./data/user/auto_planters.json", "w") as f:
                            json.dump(data, f, indent=3)
                        f.close()
                        updateGUI.value = 1
                    
                    def getCurrentNectarPercent(nectar):
                        res = macro.buffDetector.getNectar(nectar)
                        print(f"Current {nectar} Nectar: {res}%")
                        return res
                    
                    def getEstimateNectarPercent(nectar):
                        estimatedNectarPercent = 0
                        for i in range(3):
                            if planterData[i]["nectar"] == nectar:
                                estimatedNectarPercent += planterData[i]["nectar_est_percent"]
                        return estimatedNectarPercent
                    
                    def getTotalNectarPercent(nectar):
                        return getCurrentNectarPercent(nectar) + getEstimateNectarPercent(nectar)

                    def getNextField(nectar):
                        availableFields = []
                        occupiedFields = [planter["field"] for planter in planterData]
                        for field in macroModule.nectarFields[nectar]:
                            if macro.setdat[f"auto_field_{field.replace(' ','_')}"] and not field in occupiedFields:
                                availableFields.append(field)
                        if not availableFields:
                            return None
                        for i, field in enumerate(availableFields):
                            if field == nectarLastFields[nectar]:
                                nextFieldIndex = i+1
                                if nextFieldIndex >= len(availableFields):
                                    nextFieldIndex = 0
                                return availableFields[nextFieldIndex]
                        return availableFields[1] if len(availableFields) > 1 else availableFields[0]
                    
                    def getBestPlanter(field):
                        bestPlanterObj = None
                        occupiedPlanters = [planter["planter"] for planter in planterData]
                        for planterObj in macroModule.autoPlanterRankings[field]:
                            planter = planterObj["name"]
                            settingPlanter = planter.replace(" ", "_")
                            if not planter in occupiedPlanters and macro.setdat[f"auto_planter_{settingPlanter}"]:
                                bestPlanterObj = planterObj
                                return bestPlanterObj
                    
                    def savePlacedPlanter(slot, field, planter, nectar):
                        nonlocal planterData, nectarLastFields
                        estimatedNectarPercent = getTotalNectarPercent(nectar)

                        for i in range(5):
                            if macro.setdat[f"auto_priority_{i}_nectar"] == nectar:
                                minPercent = max(macro.setdat[f"auto_priority_{i}_min"], estimatedNectarPercent)
                                break
                        
                        if macro.setdat["auto_planters_collect_auto"]:
                            totalBonus = planter["nectar_bonus"] * planter["grow_bonus"]
                            timeToCap = max(0.25, ((max(0, (100 - estimatedNectarPercent) / planter["nectar_bonus"]) * 0.24) / planter["grow_bonus"]))

                            if totalBonus < 1.2:
                                growTime = min(timeToCap, 0.5)
                            elif minPercent > estimatedNectarPercent and estimatedNectarPercent <=90:
                                if estimatedNectarPercent > 20:
                                    bonusTime = (100/estimatedNectarPercent)*totalBonus
                                    growTime = (((minPercent - estimatedNectarPercent + bonusTime) / planter["nectar_bonus"]) * 0.24) / planter["grow_bonus"]
                                elif estimatedNectarPercent > 10:
                                    growTime = min(planter["grow_time"], 4)
                                else:
                                    growTime = min(planter["grow_time"], 2)
                            else:
                                growTime = timeToCap

                            finalGrowTime = min(planter["grow_time"], (growTime + growTime/totalBonus), timeToCap + timeToCap/totalBonus)*60*60
                            planterHarvestTime = time.time() + finalGrowTime
                        elif macro.setdat["auto_planters_collect_full"]:
                            finalGrowTime = planter["grow_time"]*60*60
                            planterHarvestTime = time.time() + finalGrowTime
                        else:
                            finalGrowTime = min(planter["grow_time"], macro.setdat["auto_planters_collect_every"])*60*60
                            lowestHarvestTime = time.time() + finalGrowTime
                            for i in range(3):
                                harvestTime = planterData[i]["harvest_time"]
                                if harvestTime > time.time() and lowestHarvestTime > harvestTime:
                                    lowestHarvestTime = harvestTime

                            planterHarvestTime = lowestHarvestTime
                            finalGrowTime = lowestHarvestTime - time.time()
                        
                        planterEstPerc = round((finalGrowTime * planter["nectar_bonus"]/864), 1)

                        planterData[slot] = {
                            "planter": planter["name"],
                            "nectar": nectar,
                            "field": field,
                            "harvest_time": planterHarvestTime,
                            "nectar_est_percent": planterEstPerc
                        }
                        planterReady = time.strftime("%H:%M:%S", time.gmtime(finalGrowTime))
                        macro.logger.webhook("", f"Planter will be ready in: {planterReady}", "light blue")
                        nectarLastFields[nectar] = field
                        saveAutoPlanterData()

                    planterSlotsToHarvest = []
                    for i in range(5):
                        nectar = macro.setdat[f"auto_priority_{i}_nectar"]
                        if nectar == "none":
                            continue
                        currentNectarPerc = getCurrentNectarPercent(nectar)
                        estimateNectarPerc = getEstimateNectarPercent(nectar) 
                        if (macro.setdat["auto_planters_collect_auto"] and (
                            (currentNectarPerc > 99) or
                            (currentNectarPerc > 90 and currentNectarPerc + estimateNectarPerc > 110) or
                            (currentNectarPerc + estimateNectarPerc > 120)
                            )):
                            for j in range(3):
                                if (nectar == planterData[j]["nectar"]):
                                    planterSlotsToHarvest.append(j)
                    
                    for i in range(3):
                        planter = planterData[i]
                        if planter["planter"] and time.time() > planter["harvest_time"]:
                            planterSlotsToHarvest.append(i)
                    
                    planterSlotsToHarvest = list(set(planterSlotsToHarvest))
                    for slot in planterSlotsToHarvest:
                        planter = planterData[slot]
                        if runTask(macro.collectPlanter, args=(planter["planter"], planter["field"])):
                            planterData[slot] = {
                                "planter": "",
                                "nectar": "",
                                "field": "",
                                "harvest_time": 0,
                                "nectar_est_percent": 0
                            }
                            saveAutoPlanterData()
                    
                    maxAllowedPlanters = 0
                    for x in macroModule.allPlanters:
                        x = x.replace(" ","_")
                        if macro.setdat[f"auto_planter_{x}"]:
                            maxAllowedPlanters += 1
                    maxAllowedPlanters = min(maxAllowedPlanters, macro.setdat["auto_max_planters"])

                    plantersPlaced = sum(bool(p["planter"]) for p in planterData)

                    for i in range(5):
                        if plantersPlaced >= maxAllowedPlanters:
                            break
                        nectar = macro.setdat[f"auto_priority_{i}_nectar"]
                        for j in range(3):
                            planter = planterData[j]
                            if planter["planter"]:
                                continue

                            nextField = getNextField(nectar)
                            if nextField is None:
                                break

                            minPerc = macro.setdat[f"auto_priority_{i}_min"]
                            totalNectarPercent = getTotalNectarPercent(nectar)
                            if totalNectarPercent > minPerc:
                                break

                            planterToPlace = getBestPlanter(nextField)
                            if planterToPlace is None:
                                break
                            if runTask(macro.placePlanter, args=(planterToPlace["name"], nextField, False), convertAfter=False):
                                savePlacedPlanter(j, nextField, planterToPlace, nectar)
                                plantersPlaced += 1
                    
                    if plantersPlaced < maxAllowedPlanters:
                        nectarPercentages = []
                        for nectar in macroModule.nectarFields:
                            nectarPercentages.append((nectar, getTotalNectarPercent(nectar)))
                        nectarPercentages.sort(key=lambda x: x[1])

                        for nectar, totalNectarPercent in nectarPercentages:
                            if plantersPlaced >= maxAllowedPlanters:
                                break
                            for j in range(3):
                                planter = planterData[j]
                                if planter["planter"]:
                                    continue

                                nextField = getNextField(nectar)
                                if nextField is None:
                                    break

                                if totalNectarPercent > 110:
                                    break

                                planterToPlace = getBestPlanter(nextField)
                                if planterToPlace is None:
                                    break
                                if runTask(macro.placePlanter, args=(planterToPlace["name"], nextField, False), convertAfter=False):
                                    savePlacedPlanter(j, nextField, planterToPlace, nectar)
                                    plantersPlaced += 1
                    
                    if plantersPlaced < maxAllowedPlanters:
                        for i in range(5):
                            if plantersPlaced >= maxAllowedPlanters:
                                break
                            nectar = macro.setdat[f"auto_priority_{i}_nectar"]
                            for j in range(3):
                                planter = planterData[j]
                                if planter["planter"]:
                                    continue

                                nextField = getNextField(nectar)
                                if nextField is None:
                                    break

                                planterToPlace = getBestPlanter(nextField)
                                if planterToPlace is None:
                                    break
                                if runTask(macro.placePlanter, args=(planterToPlace["name"], nextField, False), convertAfter=False):
                                    savePlacedPlanter(j, nextField, planterToPlace, nectar)
                                    plantersPlaced += 1
                    
                    executedTasks.add(taskId)
                    return True
                
                return False
            
            if taskId == "ant_challenge":
                if macro.setdat["ant_challenge"]:
                    runTask(macro.antChallenge)
                    executedTasks.add(taskId)
                    return True
                return False
            
            # Special priority tasks (stinger_hunt, mondo_buff, auto_field_boost) are handled after each task
            if taskId in ["stinger_hunt", "mondo_buff", "auto_field_boost"]:
                # These are handled in runTask's priority tasks section
                executedTasks.add(taskId)
                return False
            
            return False
        
        # Execute tasks in priority order
        if priorityOrder and len(priorityOrder) > 0:
            # Keep executing tasks until no more tasks can be executed
            # This ensures mobs check all fields before moving to next task
            maxIterations = len(priorityOrder) * 10  # Safety limit to prevent infinite loops
            iteration = 0
            while iteration < maxIterations:
                iteration += 1
                anyTaskExecuted = False
                # Track which regular mob tasks we've checked in this iteration to prevent infinite loops
                regularMobTasksChecked = set()
                for taskId in priorityOrder:
                    # Skip if already executed (for non-mob tasks)
                    if taskId in executedTasks:
                        continue
                    # For regular mob kill tasks, track if we've checked them this iteration
                    # This prevents checking the same mob multiple times in one iteration
                    isRegularMobTask = taskId.startswith("kill_") and taskId.replace("kill_", "") not in ["coconut_crab", "stump_snail"]
                    if isRegularMobTask:
                        if taskId in regularMobTasksChecked:
                            continue  # Already checked this mob in this iteration
                        regularMobTasksChecked.add(taskId)
                    # Execute the task
                    if executeTask(taskId):
                        anyTaskExecuted = True
                        # For regular mob kill tasks, don't mark as executed so they can be checked again in next iteration
                        # This allows checking all fields for the mob before moving on
                        if not isRegularMobTask:
                            executedTasks.add(taskId)
                    # For regular mob tasks, if we killed in any field, break to start next iteration
                    # This ensures we check all fields for the mob before moving to the next task
                    # The break causes the while loop to continue, which will re-check this mob
                    if isRegularMobTask and anyTaskExecuted:
                        break  # Break inner loop to start next iteration and re-check this mob
                # If no tasks were executed, break the loop
                if not anyTaskExecuted:
                    break
        else:
            # Fallback to old order if no priority order is set
            #collect
            for k, _ in macroModule.collectData.items():
                if macro.setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]):
                    runTask(macro.collect, args=(k,))

            if macro.setdat["sticker_printer"] and macro.hasRespawned("sticker_printer", macro.collectCooldowns["sticker_printer"]):
                runTask(macro.collectStickerPrinter)
            
            #blender
            if macro.setdat["blender_enable"]:
                with open("./data/user/blender.txt", "r") as f:
                    blenderData = ast.literal_eval(f.read())
                f.close()
                if blenderData["collectTime"] > -1 and time.time() > blenderData["collectTime"]:
                    runTask(macro.blender, args=(blenderData,))

        # Handle quest gather fields and required fields that weren't executed in priority order
        # These need to be handled separately as they depend on quest requirements
        blueFields = ["blue flower", "bamboo", "pine tree", "stump"]
        redFields = ["mushroom", "strawberry", "rose", "pepper"]
        
        # Setup quest gather overrides
        questGatherOverrides = {}
        if macro.setdat["quest_gather_mins"]:
            questGatherOverrides["mins"] = macro.setdat["quest_gather_mins"]
        if macro.setdat["quest_gather_return"] != "no override":
            questGatherOverrides["return"] = macro.setdat["quest_gather_return"]
        
        # Track all gathered fields to avoid duplicates
        allGatheredFields = []
        
        # Handle gumdrop gather fields first
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
            if field not in allGatheredFields:
                runTask(macro.gather, args=(field, questGatherOverrides, True), resetAfter=False)
                allGatheredFields.append(field)

        # Handle regular quest gather fields
        questGatherFields = [x for x in questGatherFields if not (x in allGatheredFields)]
        for field in questGatherFields:
            runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
            allGatheredFields.append(field)

        # Handle required blue/red fields for quests
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
        
        # Handle planter gather fields (if not already gathered)
        if planterDataRaw:
            try:
                planterGatherFields = [x for x in ast.literal_eval(planterDataRaw)["gatherFields"] if x]
                for field in planterGatherFields:
                    if field not in allGatheredFields:
                        runTask(macro.gather, args=(field,), resetAfter=False)
                        allGatheredFields.append(field)
            except:
                pass
        
        # Old code removed - all tasks now execute via priority order
        
        mouse.click()


def watch_for_hotkeys(run):
    # Track currently pressed keys for combination detection
    pressed_keys = set()
    
    # Add debouncing to prevent duplicate triggers
    last_trigger_time = {"start": 0.0, "stop": 0.0}  # , "pause": 0.0}
    debounce_duration = 0.3  # 300ms debounce
    
    # Add threading lock for synchronization
    import threading
    key_lock = threading.Lock()
    
    # Add key state cleanup to handle stuck keys
    last_cleanup_time = 0
    cleanup_interval = 5.0  # Clean up every 5 seconds
    
    # Force stop tracking
    stop_key_held = False
    force_stop_check_interval = 0.1  # Check every 100ms
    last_force_stop_check = 0
    
    # Cache settings to avoid reloading on every keypress
    settings_cache = {}
    last_settings_load = 0
    settings_cache_duration = 1.0  # Reload settings every 1 second max
    
    # Cache Eel recording state to avoid repeated calls
    recording_cache = {"start": False, "stop": False}  # , "pause": False}
    last_recording_check = 0
    recording_cache_duration = 0.5  # Check recording state every 0.5 seconds max
    
    def get_cached_settings():
        nonlocal settings_cache, last_settings_load
        current_time = time.time()
        if current_time - last_settings_load > settings_cache_duration:
            settings_cache = settingsManager.loadAllSettings()
            last_settings_load = current_time
        return settings_cache
    
    def is_recording_keybind():
        nonlocal recording_cache, last_recording_check
        current_time = time.time()
        if current_time - last_recording_check > recording_cache_duration:
            try:
                import eel
                recording_cache["start"] = eel.getElementProperty("start_keybind", "dataset.recording")() == "true"
                recording_cache["stop"] = eel.getElementProperty("stop_keybind", "dataset.recording")() == "true"
                # recording_cache["pause"] = eel.getElementProperty("pause_keybind", "dataset.recording")() == "true"
                last_recording_check = current_time
            except:
                recording_cache = {"start": False, "stop": False}  # , "pause": False}
        return recording_cache["start"] or recording_cache["stop"]  # or recording_cache["pause"]
    
    def convert_key_to_string(key):
        """Optimized key conversion with minimal string operations and error handling"""
        try:
            key_str = str(key)
            if key_str.startswith("Key."):
                key_str = key_str[4:]  # Remove "Key." prefix
            
            # Use dictionary lookup for better performance
            key_mapping = {
                "ctrl_l": "Ctrl", "ctrl_r": "Ctrl",
                "alt_l": "Alt", "alt_r": "Alt", 
                "shift_l": "Shift", "shift_r": "Shift",
                "cmd_l": "Cmd", "cmd_r": "Cmd", "cmd": "Cmd",
                "space": "Space",
                "enter": "Enter", "return": "Enter",
                "tab": "Tab", "backspace": "Backspace",
                "delete": "Delete", "esc": "Escape"
            }
            
            if key_str in key_mapping:
                return key_mapping[key_str]
            elif key_str.startswith("f") and len(key_str) <= 3:
                return key_str.upper()  # F1, F2, etc.
            elif key_str.startswith("'") and key_str.endswith("'"):
                return key_str[1:-1].upper()  # Remove quotes and uppercase
            elif len(key_str) == 1:
                return key_str.upper()  # A, B, C, etc.
            else:
                return key_str
        except Exception as e:
            # Log error but don't crash the listener
            print(f"Error converting key {key}: {e}")
            return str(key)
    
    def build_key_combination():
        """Build current key combination string in consistent order"""
        modifier_keys = ['Ctrl', 'Alt', 'Shift', 'Cmd']
        sorted_keys = []
        
        # Add modifiers first in consistent order
        for mod in modifier_keys:
            if mod in pressed_keys:
                sorted_keys.append(mod)
        
        # Add non-modifier keys (sorted alphabetically)
        non_modifier_keys = []
        for key in pressed_keys:
            if key not in modifier_keys:
                non_modifier_keys.append(key)
        non_modifier_keys.sort()
        sorted_keys.extend(non_modifier_keys)
        
        return "+".join(sorted_keys)
    
    def is_stop_keybind_held():
        """Check if the stop keybind is currently held down"""
        try:
            settings = get_cached_settings()
            if not settings:
                return False
                
            stop_keybind = settings.get("stop_keybind", "F3")
            if not stop_keybind:
                return False
            
            # Parse the stop keybind to get individual keys
            stop_keys = stop_keybind.split("+")
            
            # Check if all keys in the stop keybind are currently pressed
            for key in stop_keys:
                if key not in pressed_keys:
                    return False
            return True
        except Exception as e:
            print(f"Error checking stop keybind: {e}")
            return False
    
    def on_press(key):
        nonlocal run, last_cleanup_time, stop_key_held, last_force_stop_check
        
        # Use lock to prevent race conditions
        with key_lock:
            try:
                # Periodic cleanup of stuck keys
                current_time = time.time()
                if current_time - last_cleanup_time > cleanup_interval:
                    # Clear all pressed keys to reset state
                    pressed_keys.clear()
                    last_cleanup_time = current_time
                
                # Get cached settings
                settings = get_cached_settings()
                start_keybind = settings.get("start_keybind", "F1")
                stop_keybind = settings.get("stop_keybind", "F3")
                # pause_keybind = settings.get("pause_keybind", "F2")
                
                # Convert key to string for comparison
                key_str = convert_key_to_string(key)
                pressed_keys.add(key_str)
                
                # Build current key combination
                current_combo = build_key_combination()
                
                # Don't start/stop macro if we're recording a keybind
                if is_recording_keybind():
                    return  # Ignore keybind during recording

                # Check for force stop (stop keybind held down)
                if is_stop_keybind_held():
                    if not stop_key_held:
                        stop_key_held = True
                    # Force stop immediately when stop keybind is held
                    if run.value != 0:  # Only if not already stopped
                        run.value = 0
                        # Update GUI immediately (optimistically show stopped state)
                        try:
                            import gui
                            gui.setRunState(3)  # Update GUI state optimistically to stopped
                            gui.toggleStartStop()  # Update UI immediately
                        except:
                            pass  # If gui is not ready, continue
                else:
                    stop_key_held = False

                # Add debouncing to prevent duplicate triggers
                current_time = time.time()
                
                if current_combo == start_keybind:
                    if run.value == 2: #already running
                        return
                    # Check debounce with error handling
                    try:
                        if current_time - last_trigger_time["start"] < debounce_duration:
                            return
                    except (TypeError, ValueError):
                        # Reset trigger time if there's a comparison error
                        last_trigger_time["start"] = 0.0
                    last_trigger_time["start"] = current_time
                    run.value = 1
                    # Update GUI immediately (optimistically show running state)
                    try:
                        import gui
                        gui.setRunState(2)  # Update GUI state optimistically to running
                        gui.toggleStartStop()  # Update UI immediately
                    except:
                        pass  # If gui is not ready, continue
                elif current_combo == stop_keybind and not stop_key_held:
                    if run.value == 3: #already stopped
                        return
                    # Check debounce with error handling
                    try:
                        if current_time - last_trigger_time["stop"] < debounce_duration:
                            return
                    except (TypeError, ValueError):
                        # Reset trigger time if there's a comparison error
                        last_trigger_time["stop"] = 0.0
                    last_trigger_time["stop"] = current_time
                    run.value = 0
                    # Update GUI immediately (optimistically show stopped state)
                    try:
                        import gui
                        gui.setRunState(3)  # Update GUI state optimistically to stopped
                        gui.toggleStartStop()  # Update UI immediately
                    except:
                        pass  # If gui is not ready, continue
                # elif current_combo == pause_keybind:
                #     print(f"Pause keybind detected! current_combo={current_combo}, pause_keybind={pause_keybind}, run.value={run.value}")
                #     # Check debounce with error handling
                #     try:
                #         if current_time - last_trigger_time["pause"] < debounce_duration:
                #             print("Debounce blocked pause")
                #             return
                #     except (TypeError, ValueError):
                #         # Reset trigger time if there's a comparison error
                #         last_trigger_time["pause"] = 0.0
                #     last_trigger_time["pause"] = current_time
                #     # Toggle between pause and resume
                #     if run.value == 2:  # Running -> Pause
                #         print("Setting run.value to 5 (pause request)")
                #         run.value = 5  # 5 = pause request
                #     elif run.value == 6:  # Paused -> Resume
                #         print("Setting run.value to 2 (resume)")
                #         run.value = 2  # 2 = running (resume)
                #     else:
                #         print(f"run.value is {run.value}, not 2 or 6, so no action taken")
            except Exception as e:
                # Log error but don't crash the listener
                print(f"Error in on_press: {e}")
                return
    
    def on_release(key):
        # Remove released key from pressed keys using optimized conversion
        with key_lock:
            try:
                key_str = convert_key_to_string(key)
                pressed_keys.discard(key_str)
                
                # Check if stop keybind is no longer held
                if not is_stop_keybind_held():
                    nonlocal stop_key_held
                    stop_key_held = False
            except Exception as e:
                # Log error but don't crash the listener
                print(f"Error in on_release: {e}")
                return

    # Start keyboard listener with error handling and recovery
    # On macOS, this must be called on the main thread
    def start_keyboard_listener():
        try:
            # Ensure we're on the main thread on macOS
            if sys.platform == "darwin":
                import threading
                current_thread = threading.current_thread()
                main_thread = threading.main_thread()
                if current_thread is not main_thread:
                    print("Warning: Keyboard listener should be started on main thread on macOS")
            
            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.start()
            return listener
        except Exception as e:
            print(f"Failed to start keyboard listener: {e}")
            # Try to restart after a short delay
            import threading
            def restart_listener():
                time.sleep(1)
                try:
                    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
                    listener.start()
                    print("Keyboard listener restarted successfully")
                except Exception as e2:
                    print(f"Failed to restart keyboard listener: {e2}")
            
            restart_thread = threading.Thread(target=restart_listener, daemon=True)
            restart_thread.start()
            return None
    
    # Don't start the listener here - it will be started after GUI launch on main thread
    # start_keyboard_listener()
    
    # Return the function so it can be called later on the main thread
    return start_keyboard_listener

if __name__ == "__main__":
    print("Loading gui...")
    global stopThreads, macroProc
    import gui
    import modules.screen.screenData as screenData
    from modules.controls.keyboard import keyboard as keyboardModule
    import modules.logging.log as logModule
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
    #4: disconnected (rejoin)
    manager = multiprocessing.Manager()
    run = multiprocessing.Value('i', 3)
    gui.setRunState(3)  # Initialize the global run state
    updateGUI = multiprocessing.Value('i', 0)
    skipTask = multiprocessing.Value('i', 0)  # 0 = don't skip, 1 = skip current task
    status = manager.Value(ctypes.c_wchar_p, "none")
    logQueue = manager.Queue()
    recentLogs = manager.list()  # Shared list to store recent log entries for discord bot
    initialMessageInfo = manager.dict()  # Shared dict for initial webhook message info
    start_keyboard_listener_fn = watch_for_hotkeys(run)
    logger = logModule.log(logQueue, False, None, False, blocking=True)

    disconnectCooldownUntil = 0 #only for running disconnect check on low performance

    #update settings for current profile
    currentProfile = settingsManager.getCurrentProfile()
    profileSettings = settingsManager.loadSettings()
    profileSettingsReference = settingsManager.readSettingsFile(os.path.join(settingsManager.getDefaultSettingsPath(), "settings.txt"))
    settingsManager.saveDict(os.path.join(settingsManager.getProfilePath(currentProfile), "settings.txt"), {**profileSettingsReference, **profileSettings})

    #update general settings for current profile
    generalsettings_path = os.path.join(settingsManager.getProfilePath(currentProfile), "generalsettings.txt")
    generalSettingsReference = settingsManager.readSettingsFile(os.path.join(settingsManager.getDefaultSettingsPath(), "generalsettings.txt"))
    try:
        generalSettings = settingsManager.readSettingsFile(generalsettings_path)
    except FileNotFoundError:
        # If generalsettings.txt doesn't exist, create it from defaults
        generalSettings = {}
        # Ensure the profile directory exists
        profile_dir = settingsManager.getProfilePath(currentProfile)
        os.makedirs(profile_dir, exist_ok=True)
    settingsManager.saveDict(generalsettings_path, {**generalSettingsReference, **generalSettings})

    #convert ahk pattern
    patterns_dir = settingsManager.getPatternsDir()
    if os.path.exists(patterns_dir):
        ahkPatterns = [x for x in os.listdir(patterns_dir) if ".ahk" in x]
        for pattern in ahkPatterns:
            pattern_path = os.path.join(patterns_dir, pattern)
            with open(pattern_path, "r") as f:
                ahk = f.read()
            f.close()
            try:
                python = ahkPatternToPython(ahk)
                print(f"Converted: {pattern}")
                patternName = pattern.rsplit(".", 1)[0].lower()
                output_path = os.path.join(patterns_dir, f"{patternName}.py")
                with open(output_path, "w") as f:
                    f.write(python)
                f.close()
            except:
                messageBox.msgBox(title="Failed to convert pattern", text=f"There was an error converting {pattern}. The pattern will not be used.")
    
    #setup stream class
    stream = cloudflaredStream()

    def onExit():
        stopApp()
        try:
            if discordBotProc and discordBotProc.is_alive():
                discordBotProc.terminate()
                discordBotProc.join()
        except NameError:
            pass
        
    def stopApp(page= None, sockets = None):
        global stopThreads
        global macroProc
        stopThreads = True
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
    
    # Start keyboard listener after GUI launch to ensure it's on the main thread (required on macOS)
    # This prevents TIS/TSM errors on macOS
    if start_keyboard_listener_fn:
        try:
            start_keyboard_listener_fn()
            print("Keyboard listener started successfully")
        except Exception as e:
            print(f"Failed to start keyboard listener after GUI launch: {e}")
    
    #use run.value to control the macro loop

    #check color profile
    if sys.platform == "darwin":
        try:
            colorProfileManager = DisplayColorProfile()
            currentProfileColor = colorProfileManager.getCurrentColorProfile()
            if not "sRGB" in currentProfileColor:
                try:
                    if messageBox.msgBoxOkCancel(title="Incorrect Color Profile", text=f"You current display's color profile is {currentProfileColor} but sRGB is required for the macro.\nPress 'Ok' to change color profiles"):
                        colorProfileManager.resetDisplayProfile()
                        colorProfileManager.setCustomProfile("/System/Library/ColorSync/Profiles/sRGB Profile.icc")
                        messageBox.msgBox(title="Color Profile Success", text="Successfully changed the current color profile to sRGB")

                except Exception as e:
                    messageBox.msgBox(title="Failed to change color profile", text=e)
        except Exception as e:
            pass
    
        #check screen recording permissions
        try:
            cg = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")
            cg.CGRequestScreenCaptureAccess.restype = ctypes.c_bool
            if not cg.CGRequestScreenCaptureAccess():
                messageBox.msgBox(title="Screen Recording Permission", text='Terminal does not have the screen recording permission. The macro will not work properly.\n\nTo fix it, go to System Settings -> Privacy and Security -> Screen Recording -> add and enable Terminal. After that, restart the macro')
        except AttributeError:
            pass
        #check full keyboard access
        try:
            result = subprocess.run(
                ["defaults", "read", "com.apple.universalaccess", "KeyboardAccessEnabled"],
                capture_output=True,
                text=True
            )
            value = result.stdout.strip()
            if value == "1":
                messageBox.msgBox(text = f"Full Keyboard Access is enabled. The macro will not work properly\
                    \nTo disable it, go to System Settings -> Accessibility -> Keyboard -> uncheck 'Full Keyboard Access'")
        except Exception as e:
            print("Error reading Full Keyboard Access:", e)

    discordBotProc = None
    prevDiscordBotToken = None
    prevRunState = run.value  # Track previous run state for GUI updates
    
    # Cache settings for main GUI loop to avoid reloading every 0.5 seconds
    gui_settings_cache = {}
    last_gui_settings_load = 0
    gui_settings_cache_duration = 1.0  # Reload settings every 1 second max

    while True:
        eel.sleep(0.5)
        
        # Get cached settings
        current_time = time.time()
        if current_time - last_gui_settings_load > gui_settings_cache_duration:
            gui_settings_cache = settingsManager.loadAllSettings()
            last_gui_settings_load = current_time
        setdat = gui_settings_cache

        #discord bot. Look for changes in the bot token
        currentDiscordBotToken = setdat.get("discord_bot_token", "")
        if setdat.get("discord_bot", False) and currentDiscordBotToken and currentDiscordBotToken.strip() and currentDiscordBotToken != prevDiscordBotToken:
            if discordBotProc is not None and discordBotProc.is_alive():
                print("Detected change in discord bot token, killing previous bot process")
                discordBotProc.terminate()
                discordBotProc.join()
            discordBotProc = multiprocessing.Process(target=discordBot, args=(currentDiscordBotToken, run, status, skipTask, recentLogs, initialMessageInfo, updateGUI), daemon=True)
            prevDiscordBotToken = currentDiscordBotToken
            discordBotProc.start()

        # Check if run state changed
        if run.value != prevRunState:
            # Check for resume (transition from paused to running)
            if prevRunState == 6 and run.value == 2:
                logger.webhook("Macro Resumed", "Existance Macro", "bright green")
            gui.setRunState(run.value)
            try:
                gui.toggleStartStop()  # Update UI
            except:
                pass  # If eel is not ready, continue
            prevRunState = run.value

        if run.value == 1:
            #create and set webhook obj for the logger
            logger.enableWebhook = setdat.get("enable_webhook", False)
            logger.webhookURL = setdat.get("webhook_link", "")
            logger.sendScreenshots = setdat.get("send_screenshot", True)
            stopThreads = False

            #reset hourly report data
            hourlyReport = HourlyReport()
            hourlyReport.resetAllStats()
            #stream
            def waitForStreamURL():
                #wait for up to 15 seconds for the public link
                for _ in range(150):
                    time.sleep(0.1)
                    if stream.publicURL:
                        logger.webhook("Stream Started", f'Stream URL: {stream.publicURL}', "purple")
                        
                        # If bot is enabled, populate initial message info for pinning the stream message
                        if setdat.get("discord_bot", False) and setdat.get("pin_stream_url", False):
                            import modules.logging.webhook as webhookModule
                            if webhookModule.last_message_id and webhookModule.last_channel_id:
                                initialMessageInfo['message_id'] = webhookModule.last_message_id
                                initialMessageInfo['channel_id'] = webhookModule.last_channel_id
                                initialMessageInfo['should_pin'] = True
                        return

                logger.webhook("", f'Stream could not start. Check terminal for more info', "red", ping_category="ping_critical_errors")

            streamLink = None
            if setdat.get("enable_stream", False):
                if stream.isCloudflaredInstalled():
                    logger.webhook("", "Starting Stream...", "light blue")
                    streamLink = stream.start(setdat.get("stream_resolution", 0.75))
                    Thread(target=waitForStreamURL, daemon=True).start()
                else:
                    messageBox.msgBox(text='Cloudflared is required for streaming but is not installed. Visit https://existance-macro.gitbook.io/existance-macro-docs/guides/optional-installations/stream-setup-installing-cloudflared for installation instructions', title='Cloudflared not installed')

            print("starting macro proc")
            #check if user enabled field drift compensation but sprinkler is not supreme saturator
            fieldSettings = settingsManager.loadFields()
            sprinkler = setdat["sprinkler_type"]
            for field in setdat["fields"]:
                if fieldSettings[field]["field_drift_compensation"] and setdat["sprinkler_type"] != "saturator":
                    messageBox.msgBox(title="Field Drift Compensation", text=f"You have Field Drift Compensation enabled for {field} field, \
                                    but you do not have Supreme Saturator as your sprinkler type in configs.\n\
				                    Field Drift Compensation requires you to own the Supreme Saturator.\n\
                                    Kindly disable field drift compensation if you do not have the Supreme Saturator")
                    break
            #check if blender is enabled but there are no items to craft
            validBlender = not setdat["blender_enable"] #valid blender set to false if blender is enabled, else its true since blender is disabled
            for i in range(1,4):
                if setdat[f"blender_item_{i}"] != "none" and (setdat[f"blender_repeat_{i}"] or setdat[f"blender_repeat_inf_{i}"]):
                    validBlender = True
            if not validBlender:
                messageBox.msgBox(title="Blender", text=f"You have blender enabled, \
                                    but there are no more items left to craft.\n\
				                    Check the 'repeat' setting on your blender items and reset blender data.")
            #macro proc
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, updateGUI, run, skipTask), daemon=True)
            macroProc.start()

            macro_version = settingsManager.getMacroVersion()
            logger.webhook("Macro Started", f'Existance Macro v{macro_version}\nDisplay: {screenInfo["display_type"]}, {screenInfo["screen_width"]}x{screenInfo["screen_height"]}', "purple")
            run.value = 2
            gui.setRunState(2)  # Update the global run state
            try:
                gui.toggleStartStop()  # Update UI
            except:
                pass  # If eel is not ready, continue
            try:
                gui.toggleStartStop()  # Update UI
            except:
                pass  # If eel is not ready, continue
        elif run.value == 0:
            if macroProc:
                # Stop macro and release all inputs first
                logger.webhook("Macro Stopped", "Existance Macro", "red")
                
                # Clear the initial message info for next start
                initialMessageInfo.clear()
                
                run.value = 3
                gui.setRunState(3)  # Update the global run state
                try:
                    gui.toggleStartStop()  # Update UI
                except:
                    pass  # If eel is not ready, continue
                
                # Stop all inputs and processes
                stopApp()
                
                # Generate and send final report AFTER stopping inputs
                try:
                    print("Generating final report...")
                    from modules.submacros.finalReport import FinalReport
                    import os
                    
                    # Create final report object
                    finalReportObj = FinalReport()
                    sessionStats = finalReportObj.generateFinalReport(setdat)
                    
                    # Check if report was generated successfully
                    if sessionStats and os.path.exists("finalReport.png"):
                        # Format session summary for webhook
                        sessionTime = sessionStats.get("total_session_time", 0)
                        hours = int(sessionTime / 3600)
                        minutes = int((sessionTime % 3600) / 60)
                        timeStr = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
                        
                        totalHoney = sessionStats.get("total_honey", 0)
                        avgHoneyPerHour = sessionStats.get("avg_honey_per_hour", 0)
                        
                        def millify(n):
                            """Format large numbers with suffixes"""
                            if n < 1000:
                                return str(int(n))
                            elif n < 1000000:
                                return f"{n/1000:.1f}K"
                            elif n < 1000000000:
                                return f"{n/1000000:.1f}M"
                            elif n < 1000000000000:
                                return f"{n/1000000000:.1f}B"
                            else:
                                return f"{n/1000000000000:.1f}T"
                        
                        # Add "Estimated" label if session was less than 1 hour
                        avgLabel = "Est. Avg/Hour" if sessionTime < 3600 else "Avg/Hour"
                        description = f"Runtime: {timeStr}\nTotal Honey: {millify(totalHoney)}\n{avgLabel}: {millify(avgHoneyPerHour)}"
                        
                        # Send final report webhook
                        logger.finalReport("Session Complete", description, "purple")
                        print("Final report sent successfully")
                    else:
                        print("Failed to generate final report - no data available")
                        
                except Exception as e:
                    print(f"Error generating final report: {e}")
                    import traceback
                    traceback.print_exc()
        elif run.value == 4: #disconnected
            if macroProc and macroProc.is_alive():
                macroProc.kill()
                macroProc.join()
            logger.webhook("","Disconnected", "red", "screen", ping_category="ping_disconnects")
            appManager.closeApp("Roblox")
            keyboardModule.releaseMovement()
            mouse.mouseUp()
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, updateGUI, run, skipTask), daemon=True)
            macroProc.start()
            run.value = 2
            gui.setRunState(2)  # Update the global run state
            try:
                gui.toggleStartStop()  # Update UI
            except:
                pass  # If eel is not ready, continue
        elif run.value == 5:  # Pause request
            # Send "attempting to pause" message first (same as Discord command)
            logger.webhook("Attempting to pause macro", "Waiting for current action to complete...", "yellow")
            gui.setRunState(5)  # Update GUI to show pausing state
            try:
                gui.toggleStartStop()  # Update UI
            except:
                pass
            # Wait for macro process to acknowledge pause (it will set run.value = 6)
            # The macro process releases its own inputs when it sees state 5
            # Give it up to 5 seconds for quick response
            pause_wait_start = time.time()
            paused_quickly = False
            while run.value == 5 and time.time() - pause_wait_start < 5:
                time.sleep(0.1)
                if run.value == 6:
                    paused_quickly = True
                    break
            
            # If didn't pause quickly, send checkpoint message
            if not paused_quickly and run.value == 5:
                logger.webhook("Pause request sent", "Macro will pause at the next checkpoint", "yellow")
            
            # Continue waiting up to 60 more seconds total
            while run.value == 5 and time.time() - pause_wait_start < 60:
                time.sleep(0.1)
            
            # If macro didn't acknowledge, force transition (safety fallback)
            if run.value == 5:
                keyboardModule.releaseMovement()
                mouse.mouseUp()
                run.value = 6
        elif run.value == 6 and prevRunState == 5:  # Macro just acknowledged pause
            # Now that macro has stopped its inputs, send the success webhook
            logger.webhook("Macro Paused", "Use F2 or /resume to continue", "orange")
            gui.setRunState(6)  # Update the global run state
            try:
                gui.toggleStartStop()  # Update UI
            except:
                pass  # If eel is not ready, continue
        # Note: run.value == 6 (paused) is handled in the macro process loop - it waits for resume
        
        #Check for crash
        if macroProc and not macroProc.is_alive() and hasattr(macroProc, "exitcode") and macroProc.exitcode is not None and macroProc.exitcode < 0:
            logger.webhook("","Macro Crashed", "red", "screen", ping_category="ping_critical_errors")
            macroProc.join()
            appManager.openApp("Roblox")
            keyboardModule.releaseMovement()
            mouse.mouseUp()
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, updateGUI, run, skipTask), daemon=True)
            macroProc.start()
            run.value = 2
            gui.setRunState(2)  # Update the global run state
            try:
                gui.toggleStartStop()  # Update UI
            except:
                pass  # If eel is not ready, continue

        #detect a new log message
        if not logQueue.empty():
            logData = logQueue.get()
            if logData["type"] == "webhook": #webhook
                msg = f"{logData['title']}<br>{logData['desc']}"

                # Add to recent logs list (keep last 20 entries)
                log_entry = {
                    'time': logData['time'],
                    'title': logData['title'],
                    'desc': logData['desc']
                }
                recentLogs.append(log_entry)
                # Keep only the last 20 entries
                if len(recentLogs) > 20:
                    recentLogs[:] = recentLogs[-20:]

            #add it to gui
            gui.log(logData["time"], msg, logData["color"])
        
        #detect if the gui needs to be updated
        if updateGUI.value:
            gui.updateGUI()
            updateGUI.value = 0
        
        if run.value == 2 and time.time() > disconnectCooldownUntil:
            img = adjustImage("./images/menu", "disconnect", screenInfo["display_type"])
            wmx, wmy, wmw, wmh = getWindowSize("roblox roblox")
            if locateImageOnScreen(img, wmx+wmw/3, wmy+wmh/2.8, wmw/2.3, wmh/5, 0.7):
                print("disconnected")
                run.value = 4
                disconnectCooldownUntil = time.time() + 300  # 5 min cooldown