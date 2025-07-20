import os
import sys
import subprocess
if sys.platform == "win32":
    from ctypes import *

def msgBox(title, text):

    if sys.platform == "darwin":
        os.system(f'''osascript -e 'Tell application "System Events" to display dialog "{text}" with title "{title}"' ''')
    else:
        windll.user32.MessageBoxW(0, text, title, 0)

def msgBoxOkCancel(title, text):
    #message box with OK/Cancel buttons and callback functions
    
    if sys.platform == "darwin":
        #appleScript
        script = f'''
        tell application "System Events"
            try
                display dialog "{text}" with title "{title}" buttons {{"Cancel", "OK"}} default button "OK"
                return "OK"
            on error
                return "Cancel"
            end try
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, check=True)
            user_choice = result.stdout.strip()
            
            return user_choice == "OK"
            
        except subprocess.CalledProcessError:
            return False
    
    else:
        # Windows
        # MB_OKCANCEL = 1, MB_ICONQUESTION = 32
        result = windll.user32.MessageBoxW(0, text, title, 1 | 32)
        return result == 1