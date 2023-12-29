import pyautogui as pag
import time
import os
import tkinter
import loadsettings
from pynput.keyboard import Key,Controller
from delay import sleep
keyboard = Controller()
def apdown(k):
    cmd = """
        osascript -e  'tell application "System Events" to key down "{}"'
    """.format(k)
    os.system(cmd)
def apup(k):
    cmd = """
        osascript -e  'tell application "System Events" to key up "{}"'
    """.format(k)
    os.system(cmd)

def apkey(k):
    if k.lower() == "space":
        cmd = """
            osascript -e  'tell application "System Events" to key down space'
        """
        os.system(cmd)
        time.sleep(0.08)
        cmd = """
            osascript -e  'tell application "System Events" to key up space'
        """
        os.system(cmd)
    else:
        cmd = """
            osascript -e  'tell application "System Events" to key down {}'
        """.format(k)
        os.system(cmd)
        time.sleep(0.08)
        cmd = """
            osascript -e  'tell application "System Events" to key up {}'
        """.format(k)
        os.system(cmd)
    
def aphold(k,t):
    ws = loadsettings.load()["walkspeed"]
    cmd = """
        osascript -e  'tell application "System Events" to key down {}'
    """.format(k)
    os.system(cmd)
    time.sleep(t*ws/28)
    cmd = """
        osascript -e  'tell application "System Events" to key up {}'
    """.format(k)
    os.system(cmd)

    
    
def hold(k,t,hastecomp = 1):
    settings = loadsettings.load()
    try:
        ws = settings['walkspeed']
    except:
        ws = 30
        webhook("","An error has occured when reading movespeed. Contact Existance with a screenshot of terminal at the point","red")
        print(settings)
        log(settings)
    if hastecomp:
        try:
            with open("haste.txt","r") as f:
                ws = float(f.read())
            f.close()
        except:
            pass
    keyboard.press(k)
    sleep(t*28/ws)
    keyboard.release(k)

def press(k):
    pag.keyDown(k)
    time.sleep(0.08)
    pag.keyUp(k)


        


