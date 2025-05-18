import os
import sys
if sys.platform == "win32":
    from ctypes import *
def msgBox(title, text):

    if sys.platform == "darwin":
        os.system(f'''osascript -e 'Tell application "System Events" to display dialog "{text}" with title "{title}"' ''')
    else:
        windll.user32.MessageBoxW(0, text, title, 0)