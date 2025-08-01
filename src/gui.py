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
def getPatterns():
    return [x.replace(".py","") for x in os.listdir("../settings/patterns") if ".py" in x]

@eel.expose
def clearManualPlanters():
    settingsManager.clearFile("./data/user/manualplanters.txt")
    
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

def updateGUI():
    settings = settingsManager.loadAllSettings()
    eel.loadInputs(settings)
    eel.loadTasks()

def toggleStartStop():
    eel.toggleStartStop()

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
        eel.start('index.html',app_mode = True,block = False, cmdline_args=["--incognito", "--new-window"])
    except EnvironmentError:
        msgBox(title = "error", text = "Google Chrome could not be found. Ensure that:\
     \n1. Google Chrome is installed\nGoogle chrome is in the applications folder (open the google chrome dmg file. From the pop up, drag the icon into the folder)")