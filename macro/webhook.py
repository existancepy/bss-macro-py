import time
import os
import loadsettings
from discord_webhook import DiscordWebhook, DiscordEmbed
import pyautogui
from PIL import ImageGrab
from io import BytesIO
from logpy import log
import mss
def screenshot(x,y,w,h):
    with mss.mss() as sct:
        filename = sct.shot(output='screenshot.png')
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img
    
def webhook(title,desc,colour,ss=0,hr=0):
    dwurl = loadsettings.load()["discord_webhook_url"]
    sendscreenshot = loadsettings.load()['send_screenshot']
    enable = loadsettings.load()["enable_discord_webhook"]
    colours = {
    "red":"D22B2B",
    "light blue":"89CFF0",
    "bright green": "7CFC00",
    "light green": "98FB98",
    "dark brown": "5C4033",
    "brown": "D27D2D"
    
    }
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("[{}] {} - {}".format(current_time,title,desc))
    log("[{}] {} - {}".format(current_time,title,desc))
    if not enable: return
    webhook = DiscordWebhook(url=dwurl,rate_limit_retry=True)
    # you can set the color as a decimal (color=242424) or hex (color='03b2f8') number
    if title:
        embed = DiscordEmbed(title="[{}] {}".format(current_time,title), description=desc, color=colours[colour])
    else:
        embed = DiscordEmbed(title=title, description="[{}] {}".format(current_time,desc), color=colours[colour])
    if ss and sendscreenshot:
        with mss.mss() as sct:
            filename = sct.shot(output='screenshot.png')
        with open(filename, "rb") as f:
            webhook.add_file(file=f.read(), filename=filename)
        f.close()
        embed.set_image(url=f'attachment://{filename}')
        os.remove(filename)
    if hr:
        log("trying to send hourly report")
        with open("hourlyReport-resized.png", "rb") as f:
            webhook.add_file(file=f.read(), filename='hourlyReport-resized.png')
        f.close()
        embed.set_image(url='attachment://hourlyReport-resized.png')
        #os.remove('hourlyReport.png')
    webhook.add_embed(embed)
    try:
        response = webhook.execute()
    except Exception as e: print(e)
    
        

