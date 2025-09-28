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
            for command in synced:
                print(f"  - {command.name}: {command.description}")
        except Exception as e:
            print(f"Error syncing commands: {e}")
            import traceback
            traceback.print_exc()
    
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
    
    @bot.tree.command(name = "disablegoo", description = "Disable goo for a specific field")
    async def disable_goo(interaction: discord.Interaction, field: str):
        print("disablegoo command called")
        try:
            # Import the settings functions
            from modules.misc.settingsManager import loadFields, saveField
            
            # Load current field settings
            fieldSettings = loadFields()
            
            # Normalize field name (lowercase, handle spaces)
            fieldKey = field.lower().strip()
            
            # Check if field exists
            if fieldKey not in fieldSettings:
                await interaction.response.send_message(f"Field '{field}' not found. Available fields: {', '.join(fieldSettings.keys())}")
                return
            
            # Disable goo for the field
            fieldSettings[fieldKey]["goo"] = False
            
            # Save the updated settings
            saveField(fieldKey, fieldSettings[fieldKey])
            
            await interaction.response.send_message(f"✅ Goo disabled for field: {fieldKey.title()}")
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error disabling goo: {str(e)}")
    
    @bot.tree.command(name = "enablegoo", description = "Enable goo for a specific field")
    async def enable_goo(interaction: discord.Interaction, field: str):
        print("enablegoo command called")
        try:
            # Import the settings functions
            from modules.misc.settingsManager import loadFields, saveField
            
            # Load current field settings
            fieldSettings = loadFields()
            
            # Normalize field name (lowercase, handle spaces)
            fieldKey = field.lower().strip()
            
            # Check if field exists
            if fieldKey not in fieldSettings:
                await interaction.response.send_message(f"Field '{field}' not found. Available fields: {', '.join(fieldSettings.keys())}")
                return
            
            # Enable goo for the field
            fieldSettings[fieldKey]["goo"] = True
            
            # Save the updated settings
            saveField(fieldKey, fieldSettings[fieldKey])
            
            await interaction.response.send_message(f"✅ Goo enabled for field: {fieldKey.title()}")
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error enabling goo: {str(e)}")
    
    @bot.tree.command(name = "goostatus", description = "Check goo status for all fields")
    async def goo_status(interaction: discord.Interaction):
        print("goostatus command called")
        try:
            # Import the settings functions
            from modules.misc.settingsManager import loadFields

            # Load current field settings
            fieldSettings = loadFields()

            # Create status message
            statusMessage = "**Goo Status for All Fields:**\n"
            enabledFields = []
            disabledFields = []

            for fieldName, settings in fieldSettings.items():
                if settings.get("goo", False):
                    enabledFields.append(fieldName.title())
                else:
                    disabledFields.append(fieldName.title())

            if enabledFields:
                statusMessage += f"✅ **Enabled:** {', '.join(enabledFields)}\n"
            if disabledFields:
                statusMessage += f"❌ **Disabled:** {', '.join(disabledFields)}\n"

            await interaction.response.send_message(statusMessage)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error checking goo status: {str(e)}")

    @bot.tree.command(name = "streamurl", description = "Get the current stream URL")
    async def stream_url(interaction: discord.Interaction):
        try:
            # Read stream URL from file (use absolute path for reliability)
            import sys
            src_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            stream_url_file = os.path.join(src_dir, 'stream_url.txt')
            if os.path.exists(stream_url_file):
                with open(stream_url_file, 'r') as f:
                    stream_url = f.read().strip()
                if stream_url:
                    await interaction.response.send_message(f"🔗 **Current Stream URL:**\n{stream_url}")
                else:
                    await interaction.response.send_message("❌ No active stream URL found. Make sure streaming is enabled and running.")
            else:
                await interaction.response.send_message("❌ No active stream URL found. Make sure streaming is enabled and running.")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error getting stream URL: {str(e)}")
        
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
