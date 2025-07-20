#!/usr/bin/env python3

import AppKit
import ColorSync
import os
import CoreFoundation
import urllib.parse

class DisplayColorProfile:
    #color profile manager for macos
    def __init__(self):
        # ColorSync constants
        self.DEVICE_CLASS = ColorSync.kColorSyncDisplayDeviceClass
        self.DEFAULT_PROFILE = ColorSync.kColorSyncDeviceDefaultProfileID
        
    def getMainDisplayId(self):
        main_screen = AppKit.NSScreen.mainScreen()
        device_description = main_screen.deviceDescription()
        display_id = device_description[AppKit.NSDeviceDescriptionKey("NSScreenNumber")]
        return display_id
    
    def getDisplayUUID(self, display_id):
        uuid_ref = ColorSync.CGDisplayCreateUUIDFromDisplayID(display_id)
        if uuid_ref:
            return uuid_ref
        return None
    
    def resetDisplayProfile(self):
        display_id = self.getMainDisplayId()
        
        uuid = self.getDisplayUUID(display_id)
        if not uuid:
            raise Exception("Failed to get display UUID")
        
        # Create reset profile dictionary (setting to None removes custom profile)
        reset_dict = {self.DEFAULT_PROFILE: None}
        
        try:
            ColorSync.ColorSyncDeviceSetCustomProfiles(self.DEVICE_CLASS, uuid, reset_dict)
            return True
        except Exception as e:
            raise Exception(f"Failed to reset display profile: {e}")
    
    def setCustomProfile(self, profile_path):
        display_id = self.getMainDisplayId()
        
        uuid = self.getDisplayUUID(display_id)
        if not uuid:
            raise Exception("Failed to get display UUID")
        
        #check if profile file exists
        import os
        if not os.path.exists(profile_path):
            raise FileNotFoundError(f"Could not get profile path: {profile_path}")
        
        #create profile URL
        profile_url = CoreFoundation.CFURLCreateFromFileSystemRepresentation(
            None,
            profile_path.encode('utf-8'),
            len(profile_path.encode('utf-8')),
            False
        )
        
        if not profile_url:
            raise Exception("Failed to create profile URL")
        
        custom_dict = {self.DEFAULT_PROFILE: profile_url}
        
        try:
            ColorSync.ColorSyncDeviceSetCustomProfiles(self.DEVICE_CLASS, uuid, custom_dict)
            return True
        except Exception as e:
            raise Exception(f"Failed to set custom profile: {e}")
    
    def getCurrentColorProfile(self):
        display_id = self.getMainDisplayId()
        uuid = self.getDisplayUUID(display_id)
        
        try:
            device_info = ColorSync.ColorSyncDeviceCopyDeviceInfo(
                self.DEVICE_CLASS,
                uuid
            )
            if not "CustomProfiles" in device_info:
                return "System Default"
            profile_path = device_info["CustomProfiles"]["1"]
            #check if its a NSURL object
            if hasattr(profile_path, 'path'):
                profile_path = profile_path.path()
            else:
                profile_path = str(profile_path)

            profile_name = urllib.parse.unquote(profile_path.split("/")[-1])
            return profile_name

        except Exception as e:
            print(f"Failed to get current profile: {e}")
            return None