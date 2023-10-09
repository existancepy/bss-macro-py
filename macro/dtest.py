import discord
import loadsettings
setdat = loadsettings.load()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('bsm'):
        args = message.content.split(" ")[1:]
        cmd = args[0]
        if cmd.lower() == "rejoin":
            message.channel.send("Now attempting to rejoin")
            rejoin()
        

client.run(setdat['discord_bot_token'])
