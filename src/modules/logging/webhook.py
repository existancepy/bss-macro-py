from discord_webhook import DiscordEmbed, DiscordWebhook
from requests.exceptions import SSLError, ConnectionError
def webhook(url, title, desc, time, color, imagePath = None, ping_user_id = None):
    webhook = DiscordWebhook(url = url,rate_limit_retry=True)
    
    # Add ping if user ID is provided
    if ping_user_id:
        webhook.content = f"<@{ping_user_id}>"
    
    if title:
        embed = DiscordEmbed(title="[{}] {}".format(time,title), description=desc, color=color)
    else:
        embed = DiscordEmbed(title="", description="[{}] {}".format(time,desc), color=color)
    #if to add image
    if imagePath:
        with open(imagePath, "rb") as f:
            webhook.add_file(file=f.read(), filename= "screenshot.png")
        f.close()
        embed.set_image(url='attachment://screenshot.png')
    # add embed object to webhook
    webhook.add_embed(embed)
    try:
        webhook.execute()
    except Exception as e:
        print(f"Webhook Error: {e}")