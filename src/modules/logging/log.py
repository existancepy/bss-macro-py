import time
import threading
import queue
import pyautogui as pag
from modules.screen.screenshot import screenshotScreen
import modules.logging.webhook as logWebhook

colors = {
    "red": "D22B2B",
    "light blue": "89CFF0",
    "bright green": "7CFC00",
    "light green": "98FB98",
    "dark brown": "5C4033",
    "brown": "D27D2D",
    "purple": "954cf5",
    "orange": "FFA500",
    "white": "FFFFFF",
    "yellow": "FFFF00",
}

mw, mh = pag.size()
newUI = False

def sendWebhook(url, title, desc, time, colorHex, ss=None, imagePath=None):
    screenshotRegions = {
        "screen": None,
        "honey-pollen": (mw/3.5, 23 if newUI else 0, mw/2.4, 40),
        "sticker": (200, 70, mw/2.5-200, mh/4),
        "blue": (mw*3/4, mh*2/3, mw//4, mh//3),
    }
    
    webhookImg = None
    if imagePath:
        webhookImg = imagePath
    elif ss:
        webhookImg = "webhookScreenshot.png"
        screenshotScreen(webhookImg, screenshotRegions[ss])
    logWebhook.webhook(url, title, desc, time, colorHex, webhookImg)
    print(f"[{time}] {title} {desc}")

class webhookQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def _process_queue(self):
        while True:
            # Wait for a message from the queue
            data = self.queue.get()
            if data is None:
                print("Webhook queue stopped.")
                break
            # Send the webhook
            sendWebhook(**data)
            self.queue.task_done()

    def add_to_queue(self, data):
        self.queue.put(data)

class log:
    def __init__(self, logQueue, enableWebhook, webhookURL, blocking=False):
        self.logQueue = logQueue
        self.webhookURL = webhookURL
        self.enableWebhook = enableWebhook
        self.blocking = blocking

        if not self.blocking:
            self.webhookQueue = webhookQueue()

    def log(self, msg):
        # Display in GUI or macro logs (to be implemented)
        pass

    def webhook(self, title, desc, color, ss=None, imagePath=None):
        # Update logs
        logData = {
            "type": "webhook",
            "time": time.strftime("%H:%M:%S", time.localtime()),
            "title": title,
            "desc": desc,
            "color": colors[color]
        }
        self.logQueue.put(logData)

        if not self.enableWebhook: return

        webhookData = {
            "url": self.webhookURL,
            "title": title,
            "desc": desc,
            "time": time.strftime("%H:%M:%S", time.localtime()),
            "colorHex": colors[color],
            "ss": ss,
            "imagePath": imagePath
        }

        # Add the webhook message to the queue
        if self.blocking:
            sendWebhook(**webhookData)
        else:
            self.webhookQueue.add_to_queue(webhookData)

    def hourlyReport(self, title, desc, color):
        if not self.enableWebhook: return
        logWebhook.webhook(self.webhookURL, title, desc, time.strftime("%H:%M:%S", time.localtime()), colors[color], "hourlyReport.png") 
