import sys
import re
import os
import subprocess
from modules.misc.appleScript import runAppleScript
import pygetwindow as gw
import pyautogui as pag
from ApplicationServices import AXUIElementIsAttributeSettable, AXUIElementCreateApplication, kAXErrorSuccess, AXUIElementSetAttributeValue, AXUIElementCopyAttributeValue, AXValueCreate, kAXValueCGPointType, kAXValueCGSizeType, AXUIElementCopyAttributeNames
from Quartz import CGPoint, CGSize
from CoreFoundation import CFRelease
mw,mh = pag.size()

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        #send the alt key. For some reason this is required to make it run consistently
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self._handle) #switch to window
        win32gui.ShowWindow(self._handle, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(self._handle, win32con.SW_MAXIMIZE)
    

def isAppOpenMac(app="roblox"):
    tmp = os.popen("ps -Af").read()
    return app in tmp[:]

def openAppMac(app="Roblox"):
    if not isAppOpenMac(app): return False
    runAppleScript('activate application "{}"'.format(app))
    subprocess.run(["open", "-a", app])
    workspace = NSWorkspace.sharedWorkspace()
    for runningApp in workspace.runningApplications():
        if runningApp.localizedName() == app:
            runningApp.activateWithOptions_(1 << 1)
            break
    return True

def isAppOpenWindows(name):
    w = WindowMgr()
    w.find_window(None, "Roblox")
    try:
        return True
    except:
        return False
    
def openAppWindows(name):
    w = WindowMgr()
    w.find_window(None, "Roblox")
    try:
        w.set_foreground()
        return True
    except:
        return False
        

def openDeeplink(link):
    if sys.platform == "darwin":
        subprocess.call(["open", link])
    else:
        os.system(f'start "" "{link}"')

def closeApp(app):
    if sys.platform == "darwin":
        subprocess.call(["pkill", app])
        cmd = """
            osascript -e 'quit application "Roblox"'
        """
        os.system(cmd)
    else:
        if app.lower() == "roblox":
            app = "RobloxPlayerBeta"
        #taskkill /IM RobloxPlayerBeta.exe
        #app += ".exe"
        os.system(f"START /wait taskkill /f /im {app}.exe")

def getWindowSize(windowName):
    windows = gw.getAllTitles()
    for win in windows:
        if windowName.lower() in win.lower():
            windowGeometry = gw.getWindowGeometry(win)
            if windowGeometry:
                return windowGeometry
    #window not found, most likely also fullscreen (but unfocused)
    return 0,0,mw,mh

def setAppFullscreenMac(app="Roblox", fullscreen=True):
    workspace = NSWorkspace.sharedWorkspace()
    for runningApp in workspace.runningApplications():
        if runningApp.localizedName() == app:
            pid = runningApp.processIdentifier()
            break
    else:
        return
    
    appRef = AXUIElementCreateApplication(pid)
    _, windowRef = AXUIElementCopyAttributeValue(appRef, "AXMainWindow", None)
    AXUIElementSetAttributeValue(windowRef, "AXFullScreen", fullscreen)

def maximiseAppWindowMac(app="Roblox"):
    workspace = NSWorkspace.sharedWorkspace()
    for runningApp in workspace.runningApplications():
        if runningApp.localizedName() == app:
            pid = runningApp.processIdentifier()
            break
    else:
        return
    
    appRef = AXUIElementCreateApplication(pid)
    _, windowRef = AXUIElementCopyAttributeValue(appRef, "AXMainWindow", None)
    _, attributes = AXUIElementCopyAttributeNames(windowRef, None)
    pos = AXValueCreate(kAXValueCGPointType, CGPoint(0, 0))
    size = AXValueCreate(kAXValueCGSizeType, CGSize(mw, mh))
    AXUIElementSetAttributeValue(windowRef, "AXPosition", pos)
    AXUIElementSetAttributeValue(windowRef, "AXSize", size)

if sys.platform == "darwin":
    from AppKit import NSWorkspace
    openApp = openAppMac
    isAppOpen = isAppOpenMac
    maximiseAppWindow = maximiseAppWindowMac
    setAppFullscreen = setAppFullscreenMac
else:
    import win32gui, win32con,  win32com.client
    openApp = openAppWindows
    isAppOpen = isAppOpenWindows
    
    def maximiseAppWindowWindows(app="Roblox"):
        """Windows implementation for maximizing app window"""
        w = WindowMgr()
        w.find_window(None, app)
        try:
            w.set_foreground()
        except:
            pass
    
    def setAppFullscreenWindows(app="Roblox", fullscreen=True):
        """Windows implementation for setting app fullscreen"""
        # Windows fullscreen handling is typically done through window state
        # This is a placeholder implementation
        w = WindowMgr()
        w.find_window(None, app)
        try:
            if fullscreen:
                win32gui.ShowWindow(w._handle, win32con.SW_MAXIMIZE)
            else:
                win32gui.ShowWindow(w._handle, win32con.SW_RESTORE)
        except:
            pass
    
    maximiseAppWindow = maximiseAppWindowWindows
    setAppFullscreen = setAppFullscreenWindows
