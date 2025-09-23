from AppKit import NSWorkspace, NSScreen
from ApplicationServices import AXUIElementIsAttributeSettable, AXUIElementCreateApplication, kAXErrorSuccess, AXUIElementSetAttributeValue, AXUIElementCopyAttributeValue, AXValueCreate, kAXValueCGPointType, kAXValueCGSizeType, AXUIElementCopyAttributeNames
from Quartz import CGPoint, CGSize
from CoreFoundation import CFRelease
import objc
import ctypes

def set_fullscreen(pid, fullscreen: bool):
    app_ref = AXUIElementCreateApplication(pid)

    error, window_ref = AXUIElementCopyAttributeValue(app_ref, "AXMainWindow", None)
    if error != kAXErrorSuccess or not window_ref:
        print(f"Could not get main window, error code: {error}")
        return False

    # Try setting fullscreen state
    result = AXUIElementSetAttributeValue(window_ref, "AXFullScreen", objc.YES if fullscreen else objc.NO)
    return result == kAXErrorSuccess

def maximise_window(pid):
    app_ref = AXUIElementCreateApplication(pid)
    error, window_ref = AXUIElementCopyAttributeValue(app_ref, "AXMainWindow", None)
    error, attributes = AXUIElementCopyAttributeNames(window_ref, None)
    for x in attributes:
        error, res = AXUIElementIsAttributeSettable(window_ref, x, None)
        if res:
            print(x)
    pos = AXValueCreate(kAXValueCGPointType, CGPoint(0, 0))
    size = AXValueCreate(kAXValueCGSizeType, CGSize(99999, 99999))
    result = AXUIElementSetAttributeValue(window_ref, "AXPosition", pos)
    result = AXUIElementSetAttributeValue(window_ref, "AXSize", size)

# Find Roblox
workspace = NSWorkspace.sharedWorkspace()
for app in workspace.runningApplications():
    if app.localizedName() == "Roblox":
        pid = app.processIdentifier()
        success = maximise_window(pid)
        break
