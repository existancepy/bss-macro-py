import time
import os
import loadsettings
from discord_webhook import DiscordWebhook, DiscordEmbed
settings = loadsettings.load()
def webhook(title,desc,colour):
    colours = {
    "red":"D22B2B",
    "light blue":"89CFF0",
    "bright green": "7CFC00",
    "light green": "98FB98",
    "dark brown": "5C4033",
    "brown": "D27D2D"
    
    }
    if not settings['enable_discord_webhook']: return
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    webhook = DiscordWebhook(url=settings["discord_webhook_url"])
    # you can set the color as a decimal (color=242424) or hex (color='03b2f8') number
    if title:
        embed = DiscordEmbed(title="[{}] {}".format(current_time,title), description=desc, color=colours[colour])
    else:
        embed = DiscordEmbed(title=title, description="[{}] {}".format(current_time,desc), color=colours[colour])
        
    webhook.add_embed(embed)

    response = webhook.execute()
    print("[{}] {} - {}".format(current_time,title,desc))
        

