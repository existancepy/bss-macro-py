import time
import os
import loadsettings
from discord_webhook import DiscordWebhook, DiscordEmbed
import pyautogui
import PIL
from io import BytesIO
def webhook(title,desc,colour,ss=0):
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
    if not enable: return
    webhook = DiscordWebhook(url=dwurl,rate_limit_retry=True)
    # you can set the color as a decimal (color=242424) or hex (color='03b2f8') number
    if title:
        embed = DiscordEmbed(title="[{}] {}".format(current_time,title), description=desc, color=colours[colour])
    else:
        embed = DiscordEmbed(title=title, description="[{}] {}".format(current_time,desc), color=colours[colour])
    if ss and set:
        screenshot = PIL.ImageGrab.grab()
        screenshot.convert('RGB').save("screenshot.jpg")
        with open("screenshot.jpg", "rb") as f:
            webhook.add_file(file=f.read(), filename='screenshot.jpg')
        f.close()
        embed.set_image(url='attachment://screenshot.jpg')
        os.remove('screenshot.jpg')
    webhook.add_embed(embed)
    try:
        response = webhook.execute()
    except Exception as e: print(e)
        

