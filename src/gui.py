import eel
from modules.misc.messageBox import msgBox
import webbrowser
import modules.misc.settingsManager as settingsManager
import os
from modules.misc.update import update as updateFunc
import sys
import platform
import zipfile
import requests
from io import BytesIO
import ast
import json
import webbrowser
import time

eel.init('webapp')
run = None
@eel.expose
def openLink(link):
    webbrowser.open(link, autoraise = True)
    
@eel.expose
def start():
    if run.value == 2: return #already running
    run.value = 1
    
@eel.expose
def stop():
    if run.value == 3: return #already stopped
    run.value = 0

@eel.expose
def pause():
    if run.value != 2: return #only pause if running
    run.value = 5  # 5 = pause request

@eel.expose
def resume():
    if run.value != 6: return #only resume if paused
    run.value = 2  # 2 = running (resume)

@eel.expose
def getPatterns():
    return [x.replace(".py","") for x in os.listdir("../settings/patterns") if ".py" in x]

@eel.expose
def clearManualPlanters():
    settingsManager.clearFile("./data/user/manualplanters.txt")

@eel.expose
def getManualPlanterData():
    with open("./data/user/manualplanters.txt", "r") as f:
        planterDataRaw = f.read()
    if planterDataRaw.strip():
        return ast.literal_eval(planterDataRaw)
    else: 
        return ""
    
@eel.expose
def getAutoPlanterData():
    with open("./data/user/auto_planters.json", "r") as f:
        return json.load(f)

@eel.expose
def clearAutoPlanters():
    data = {
        "planters": [
            {
                "planter": "",
                "nectar": "",
                "field": "",
                "harvest_time": 0,
                "nectar_est_percent": 0
            },
            {
                "planter": "",
                "nectar": "",
                "field": "",
                "harvest_time": 0,
                "nectar_est_percent": 0
            },
            {
                "planter": "",
                "nectar": "",
                "field": "",
                "harvest_time": 0,
                "nectar_est_percent": 0
            }
        ],
        "nectar_last_field": {
            "comforting": "",
            "refreshing": "",
            "satisfying": "",
            "motivating": "",
            "invigorating": ""
        }
    }
    with open("./data/user/auto_planters.json", "w") as f:
        json.dump(data, f, indent=3)
    
@eel.expose
def clearBlender():
    blenderData = {
        "item": 1,
        "collectTime": 0
    }
    with open("data/user/blender.txt", "w") as f:
        f.write(str(blenderData))
    f.close()

@eel.expose
def clearAFB():
    AFBData = {
        "AFB_dice_cd": 0,
        "AFB_glitter_cd": 0,
        "AFB_limit": 0
    }

    # convert to format like in timings.txt
    data_str = "\n".join([f"{key}={value}" for key, value in AFBData.items()])

    with open("data/user/AFB.txt", "w") as f:
        f.write(data_str)

@eel.expose
def resetFieldToDefault(field_name):
    """Reset a field's settings to the default values"""
    try:
        # Load default field settings
        with open("data/default_settings/fields.txt", "r") as f:
            default_fields = ast.literal_eval(f.read())

        # Get the default settings for the specified field
        if field_name in default_fields:
            default_settings = default_fields[field_name]
            # Save the default settings for this field
            settingsManager.saveField(field_name, default_settings)
            return True
        else:
            print(f"Warning: Field '{field_name}' not found in default settings")
            return False
    except Exception as e:
        print(f"Error resetting field to default: {e}")
        return False

@eel.expose
def exportFieldSettings(field_name):
    """Export field settings as JSON string"""
    try:
        return settingsManager.exportFieldSettings(field_name)
    except Exception as e:
        print(f"Error exporting field settings: {e}")
        return None

@eel.expose
def importFieldSettings(field_name, json_settings):
    """Import field settings from JSON string"""
    try:
        return settingsManager.importFieldSettings(field_name, json_settings)
    except Exception as e:
        print(f"Error importing field settings: {e}")
        return False
        
@eel.expose
def getMacroVersion():
    """Get the macro version from version.txt"""
    return settingsManager.getMacroVersion()

@eel.expose
def update():
    updateFunc()
    eel.closeWindow()
    sys.exit()

def log(time = "", msg = "", color = ""):
    eel.log(time, msg, color)

eel.expose(settingsManager.loadFields)
eel.expose(settingsManager.saveField) 
eel.expose(settingsManager.loadSettings)
eel.expose(settingsManager.loadAllSettings)
eel.expose(settingsManager.saveProfileSetting)
eel.expose(settingsManager.saveGeneralSetting)
eel.expose(settingsManager.saveDictProfileSettings)
eel.expose(settingsManager.initializeFieldSync)

# Profile management functions
eel.expose(settingsManager.listProfiles)
eel.expose(settingsManager.getCurrentProfile)
eel.expose(settingsManager.switchProfile)
eel.expose(settingsManager.createProfile)
eel.expose(settingsManager.deleteProfile)
eel.expose(settingsManager.renameProfile)
eel.expose(settingsManager.duplicateProfile)
eel.expose(settingsManager.exportProfile)
eel.expose(settingsManager.importProfile)
eel.expose(settingsManager.importProfileContent)

def updateGUI():
    settings = settingsManager.loadAllSettings()
    eel.loadInputs(settings)
    eel.loadTasks()

def toggleStartStop():
    eel.toggleStartStop()

# Global variable to store run state
# 0=stop request, 1=start request, 2=running, 3=stopped, 4=disconnected, 5=pause request, 6=paused
_run_state = 3

def setRunState(state):
    global _run_state
    _run_state = state

def getRunState():
    return _run_state

# Expose functions to eel
eel.expose(getRunState)
eel.expose(setRunState)

def launch():

    #download chromium
    # chromiumPath = os.path.abspath("chrome-mac/Chromium.app")
    # arch = platform.machine()
    # macVersion, _, _ = platform.mac_ver()
    # macVersion = float('.'.join(macVersion.split('.')[:2]))
    
    # chromiumDownloadURL = None
    # if arch == "arm64":
    #     chromiumDownloadURL = "https://storage.googleapis.com/chromium-browser-snapshots/Mac_Arm/1489261/chrome-mac.zip"
    # elif macVersion >= 11:
    #     chromiumDownloadURL = "https://storage.googleapis.com/chromium-browser-snapshots/Mac/1489261/chrome-mac.zip"

    # if chromiumDownloadURL and not os.path.isdir(chromiumPath):
    #     print("Downloading Chromium...")
    #     req = requests.get(chromiumDownloadURL)
    #     zipf= zipfile.ZipFile(BytesIO(req.content))
    #     zipf.extractall("")

    #     os.system(f"xattr -cr {chromiumPath}")
    #     os.chmod(chromiumPath, 0o755)
    #     os.system(f"chmod -R u+rx {chromiumPath}")
    #     os.system('export GOOGLE_API_KEY="no"')
    #     os.system('export GOOGLE_DEFAULT_CLIENT_ID="no"')
    #     os.system('export GOOGLE_DEFAULT_CLIENT_SECRET="no"')


    # if chromiumDownloadURL:
    #     eel.browsers.set_path("chrome", os.path.join(chromiumPath, "Contents/MacOS/Chromium"))

    # try:
    #     eel.start('index.html',app_mode = True,block = False, cmdline_args=["--incognito", "--new-window", "--disable-infobars"])
    # except EnvironmentError:
    #     print("Chrome/Chromium could not be found. You can access the macro at: http://localhost:8000/")
    #     eel.start('index.html', block=False)
    # #     msgBox(title = "error", text = "Google Chrome could not be found. Ensure that:\
    # #  \n1. Google Chrome is installed\nGoogle chrome is in the applications folder (open the google chrome dmg file. From the pop up, drag the icon into the folder)")
    
    try:
        eel.start('index.html', mode = "chrome", app_mode = True, block = False, cmdline_args=["--incognito", "--app=http://localhost:8000"])
    except EnvironmentError:
        try:
            eel.start('index.html', mode = "chrome-app", app_mode = True, block = False, cmdline_args=["--incognito", "--app=http://localhost:8000"])
        except EnvironmentError:
            print("Chrome/Chromium could not be found. Opening in default browser...")
            eel.start('index.html', block=False, mode=None)
            time.sleep(2)
            webbrowser.open("http://localhost:8000/", new=2)
