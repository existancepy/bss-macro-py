import os
def runAppleScript(code):
    cmd = ''' osascript -e '{}' '''.format(code)
    os.system(cmd)