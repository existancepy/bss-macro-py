from discord_webhook import DiscordEmbed, DiscordWebhook
from requests.exceptions import SSLError, ConnectionError

# Global variable to store message ID for pinning
last_message_id = None
last_channel_id = None

def webhook(url, title, desc, time, color, imagePath = None, ping_user_id = None, time_format=24):
    global last_message_id, last_channel_id
    
    # Check if URL is provided
    if not url or not url.strip():
        print(f"Warning: Webhook URL is empty. Skipping webhook message: {title} {desc}")
        return None
    
    webhook = DiscordWebhook(url = url,rate_limit_retry=True)
    
    # Add ping if user ID is provided
    if ping_user_id:
        webhook.content = f"<@{ping_user_id}>"
    
    # Format time based on preference
    if time_format == 12:
        try:
            # Parse the time string and convert to 12-hour format
            from datetime import datetime
            time_obj = datetime.strptime(time, "%H:%M:%S")
            formatted_time = time_obj.strftime("%I:%M:%S %p")
        except:
            formatted_time = time  # fallback to original if parsing fails
    else:
        formatted_time = time

    if title:
        embed = DiscordEmbed(title="[{}] {}".format(formatted_time,title), description=desc, color=color)
    else:
        embed = DiscordEmbed(title="", description="[{}] {}".format(formatted_time,desc), color=color)
    #if to add image
    if imagePath:
        with open(imagePath, "rb") as f:
            webhook.add_file(file=f.read(), filename= "screenshot.png")
        f.close()
        embed.set_image(url='attachment://screenshot.png')
    # add embed object to webhook
    webhook.add_embed(embed)
    try:
        response = webhook.execute()
        # Store message ID and channel ID for potential pinning
        if response and hasattr(response, 'json'):
            response_data = response.json()
            last_message_id = response_data.get('id')
            last_channel_id = response_data.get('channel_id')
        return response
    except Exception as e:
        print(f"Webhook Error: {e}")
        return None