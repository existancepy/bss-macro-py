# Navigate to honey storm location and summon it
# Credit to laganyt for the path
import sys
import os
# Add src to path if not already there
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)
from modules import macro
from datetime import timedelta
objectiveData = macro.mergedCollectData["honeystorm"]
cooldownSeconds = objectiveData[2]

self.runPath("collect/stockings")
self.keyboard.walk("a",1.25, False)
self.keyboard.walk("s",1.5)
self.keyboard.walk("d",0.45)
self.keyboard.walk("s",0.8)
reached = self.isBesideE(objectiveData[0])
if not reached:
    self.logger.webhook("", "Failed to reach Honey Storm summon point", "dark brown", "screen")
elif "(" in reached and ":" in reached:
    cd = self.cdTextToSecs(reached, True, cooldownSeconds)
    if cd:
        cooldownFormat = timedelta(seconds=cd)
        self.logger.webhook("", f"Honey Storm is on cooldown ({cooldownFormat} remaining)", "dark brown", "screen")
    else:
        # Execute honey storm actions - add small delay to ensure stability after cooldown check
        time.sleep(0.2)
        self.keyboard.press("e")
        time.sleep(0.5)
        self.keyboard.walk("s", 3)
        self.keyboard.walk("d", 2)
        for i in range(8):
            self.keyboard.walk("w", 2.25)
            self.keyboard.walk("d", 0.25)
            self.keyboard.walk("s", 2.25)
            self.keyboard.walk("d", 0.25)
else:
    # Execute honey storm actions
    self.keyboard.press("e")
    time.sleep(0.5)
    self.keyboard.walk("s", 3)
    self.keyboard.walk("d", 2)
    for i in range(8):
        self.keyboard.walk("w", 2.25)
        self.keyboard.walk("d", 0.25)
        self.keyboard.walk("s", 2.25)
        self.keyboard.walk("d", 0.25)
