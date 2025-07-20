import discord
try:
    from discord import app_commands
except ImportError:
    print("discord bot not supported")
from discord.ext import commands
from modules.screen.screenshot import screenshotRobloxWindow
import io
from modules.misc.messageBox import msgBox
from modules.misc.appManager import closeApp
import subprocess
import sys
import os

def discordBot(token, run, status):
    bot = commands.Bot(command_prefix="!b", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("Bot is Ready!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)
    
    @bot.tree.command(name = "ping", description = "Check if the bot is online")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
    
    @bot.tree.command(name = "screenshot", description = "Send a screenshot of your screen")
    async def screenshot(interaction: discord.Interaction):
        await interaction.response.defer()
        img = screenshotRobloxWindow()
        with io.BytesIO() as imageBinary:
            img.save(imageBinary, "PNG")
            imageBinary.seek(0)
            await interaction.followup.send(file = discord.File(fp=imageBinary, filename="screenshot.png"))

    @bot.tree.command(name = "start", description = "Start")
    async def stop(interaction: discord.Interaction):
        if run.value == 2: 
            await interaction.response.send_mesasge("Macro is already running")
            return 
        run.value = 1
        await interaction.response.send_message("Starting Macro")

    @bot.tree.command(name = "stop", description = "Stop the macro")
    async def stop(interaction: discord.Interaction):
        if run.value == 3: 
            await interaction.response.send_mesasge("Macro is already stopped")
            return 
        run.value = 0
        await interaction.response.send_message("Stopping Macro")
        
    @bot.tree.command(name = "rejoin", description = "Make the macro rejoin the game.")
    async def rejoin(interaction: discord.Interaction):
        run.value = 4
        await interaction.response.send_message("Macro is rejoining")

    @bot.tree.command(name = "amulet", description = "Choose to keep or replace an amulet")
    @app_commands.describe(option = "keep or replace an amulet")
    async def amulet(interaction: discord.Interaction, option: str):
        if run.value != 2:
            await interaction.response.send_message("Macro is not running")
        option = option.lower()
        keepAlias = ["k", "keep"]
        replaceAlias = ["r", "replace"]
        if not option in keepAlias and not option in replaceAlias:
            await interaction.response.send_message("Unknown option. Enter either `keep` or `replace`")
        
        elif status.value != "amulet_wait":
            await interaction.response.send_message("There is no amulet to keep or replace")
            return
        elif option in keepAlias:
            status.value = "amulet_keep"
            await interaction.response.send_message("Keeping amulet")
        elif option in replaceAlias:
            status.value = "amulet_replace"
            await interaction.response.send_message("Replacing amulet")

    @bot.tree.command(name = "battery", description = "Get your current battery status")
    async def battery(interaction: discord.Interaction):
        try:
            if sys.platform == "darwin":
                output = subprocess.check_output(["pmset", "-g", "batt"], text=True)
                for line in output.split("\n"):
                    if "InternalBattery" in line:
                        parts = line.split("\t")[-1].split(";")
                        percent = parts[0].strip()
                        status = parts[1].strip()
                        await interaction.response.send_message(f"Battery is at {percent} and is currently {status}.")
                        return
                    
            elif sys.platform == "win32":
                output = subprocess.check_output(["wmic", "path", "Win32_Battery", "get", "EstimatedChargeRemaining, BatteryStatus"], text=True)
                lines = output.strip().split("\n")
                if len(lines) > 1:
                    # Parse the output
                    data = lines[1].split()
                    percent = data[0]  # First column is the battery percentage
                    status = "charging" if data[1] == "2" else "not charging"  # Status column
                    await interaction.response.send_message(f"Battery is at {percent}% and is currently {status}.")
            
            await interaction.response.send_message("Battery information not found.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")
    
    @bot.tree.command(name = "close", description = "Close the macro and roblox")
    async def battery(interaction: discord.Interaction):
        closeApp("Roblox")
        os._exit(1)
        
    '''
    @bot.tree.command(name = "hourly report", description = "Send the hourly report")
    async def hourlyReport(interaction: discord.Interaction):
        await interaction.response.defer()
        generateHourlyReport()
        await interaction.followup.send(file = discord.File("hourlyReport.png"))
    '''
        
    #start bot
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print("Incorrect Bot Token", "The discord bot token you entered is invalid.")
