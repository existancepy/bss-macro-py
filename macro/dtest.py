import discord
import loadsettings
setdat = loadsettings.load()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.command(name="rejoin",description="rejoin the game")
async def rejoincmd(ctx):
    ctx.channel.send("Now attempting to rejoin")
    rejoin()


client.run(setdat['discord_bot_token'])
