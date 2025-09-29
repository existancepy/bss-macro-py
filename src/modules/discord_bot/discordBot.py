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
import json
import ast
import time
from datetime import datetime, timedelta

# Import settings manager functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'misc'))
import settingsManager

# Global settings cache to avoid frequent file reads
_settings_cache = {}
_cache_timestamp = 0
_cache_duration = 5  # seconds

def get_cached_settings():
    """Get settings with caching to improve performance"""
    global _settings_cache, _cache_timestamp
    current_time = time.time()

    if current_time - _cache_timestamp > _cache_duration or not _settings_cache:
        _settings_cache = settingsManager.loadAllSettings()
        _cache_timestamp = current_time

    return _settings_cache

def clear_settings_cache():
    """Clear the settings cache"""
    global _settings_cache, _cache_timestamp
    _settings_cache = {}
    _cache_timestamp = 0

def update_setting(setting_key, value):
    """Update a specific setting"""
    try:
        # Convert string values to appropriate types
        if isinstance(value, str):
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)

        settingsManager.saveGeneralSetting(setting_key, value)
        clear_settings_cache()
        return True, f"✅ Successfully updated {setting_key} to {value}"
    except Exception as e:
        return False, f"❌ Error updating setting: {str(e)}"

def update_profile_setting(setting_key, value):
    """Update a profile-specific setting"""
    try:
        # Convert string values to appropriate types
        if isinstance(value, str):
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)

        settingsManager.saveProfileSetting(setting_key, value)
        clear_settings_cache()
        return True, f"✅ Successfully updated {setting_key} to {value}"
    except Exception as e:
        return False, f"❌ Error updating profile setting: {str(e)}"

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

    # === COMPREHENSIVE SETTINGS MANAGEMENT COMMANDS ===

    @bot.tree.command(name="settings", description="View current macro settings")
    async def view_settings(interaction: discord.Interaction):
        """View current macro settings"""
        await interaction.response.defer()

        try:
            settings = get_cached_settings()

            # Create embed for better formatting
            embed = discord.Embed(title="📋 Current Macro Settings", color=0x00ff00)

            # Group settings by category
            categories = {
                "🎯 **Core Settings**": ["fields_enabled", "fields"],
                "💰 **Collectibles**": ["wealth_clock", "blueberry_dispenser", "strawberry_dispenser", "royal_jelly_dispenser", "treat_dispenser"],
                "🐛 **Mob Runs**": ["ladybug", "rhinobeetle", "scorpion", "mantis", "spider", "werewolf", "coconut_crab", "stump_snail"],
                "🌱 **Planters**": ["planters_mode", "auto_max_planters", "auto_preset"],
                "📊 **Quests**": ["polar_bear_quest", "honey_bee_quest", "bucko_bee_quest", "riley_bee_quest"],
                "🔧 **Advanced**": ["Auto_Field_Boost", "mondo_buff", "stinger_hunt", "blender_enable"]
            }

            for category, keys in categories.items():
                section_content = []
                for key in keys:
                    if key in settings:
                        value = settings[key]
                        if isinstance(value, list):
                            value = ", ".join([str(v) for v in value])
                        elif isinstance(value, bool):
                            value = "✅" if value else "❌"
                        section_content.append(f"**{key}:** {value}")

                if section_content:
                    embed.add_field(name=category, value="\n".join(section_content), inline=False)

            embed.set_footer(text="Use specific commands to modify individual settings")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"❌ Error retrieving settings: {str(e)}")


    # === FIELD CONFIGURATION COMMANDS ===

    @bot.tree.command(name="fields", description="View field configuration")
    async def view_fields(interaction: discord.Interaction):
        """View current field configuration"""
        await interaction.response.defer()

        try:
            settings = get_cached_settings()
            field_list = settings.get("fields", [])
            fields_enabled = settings.get("fields_enabled", [])

            embed = discord.Embed(title="🌾 Field Configuration", color=0x00ff00)

            enabled_fields = []
            disabled_fields = []

            for i, field_name in enumerate(field_list):
                is_enabled = i < len(fields_enabled) and fields_enabled[i]

                if is_enabled:
                    enabled_fields.append(f"**{field_name.title()}**")
                else:
                    disabled_fields.append(field_name.title())

            if enabled_fields:
                embed.add_field(name="✅ **Enabled Fields**", value="\n".join(enabled_fields), inline=False)
            if disabled_fields:
                embed.add_field(name="❌ **Disabled Fields**", value=", ".join(disabled_fields), inline=False)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"❌ Error retrieving field settings: {str(e)}")

    async def field_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for currently active field names"""
        settings = get_cached_settings()
        field_list = settings.get("fields", [])
        choices = []

        for field in field_list:
            if current.lower() in field.lower():
                choices.append(app_commands.Choice(name=field.title(), value=field.lower().replace(" ", "_")))

        return choices[:25]  # Discord limit is 25 choices

    async def all_fields_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for all possible field names"""
        # All possible field names in the game
        all_possible_fields = [
            "sunflower", "dandelion", "mushroom", "blue_flower", "clover", "strawberry",
            "spider", "bamboo", "pineapple", "stump", "cactus", "pumpkin", "pine_tree",
            "rose", "mountain_top", "pepper", "coconut"
        ]
        choices = []

        for field in all_possible_fields:
            display_name = field.replace("_", " ").title()
            if current.lower() in field.lower() or current.lower() in display_name.lower():
                choices.append(app_commands.Choice(name=display_name, value=field))

        return choices[:25]  # Discord limit is 25 choices

    async def quest_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for quest names"""
        quests = ["polar_bear", "honey_bee", "bucko_bee", "riley_bee"]
        choices = []

        for quest in quests:
            if current.lower() in quest.lower():
                choices.append(app_commands.Choice(name=quest.replace("_", " ").title(), value=quest))

        return choices[:25]

    async def collectible_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for collectible names"""
        collectibles = [
            "wealth_clock", "blueberry", "strawberry", "coconut", "royal_jelly", "ant_pass",
            "treat", "glue", "honeystorm"
        ]
        choices = []

        for collectible in collectibles:
            display_name = collectible.replace("_", " ").title()
            if current.lower() in collectible.lower():
                choices.append(app_commands.Choice(name=display_name, value=collectible))

        return choices[:25]

    async def mob_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for mob names"""
        mobs = ["ladybug", "rhinobeetle", "scorpion", "mantis", "spider", "werewolf", "coconut_crab", "stump_snail"]
        choices = []

        for mob in mobs:
            display_name = mob.replace("_", " ").title()
            if current.lower() in mob.lower():
                choices.append(app_commands.Choice(name=display_name, value=mob))

        return choices[:25]

    async def planter_mode_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for planter modes"""
        modes = [
            app_commands.Choice(name="Disabled", value="0"),
            app_commands.Choice(name="Manual", value="1"),
            app_commands.Choice(name="Auto", value="2")
        ]
        return modes

    async def use_when_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for hotbar use_when options"""
        options = [
            app_commands.Choice(name="Never", value="never"),
            app_commands.Choice(name="Always", value="always"),
            app_commands.Choice(name="Field", value="field"),
            app_commands.Choice(name="Quest", value="quest")
        ]
        return options

    async def format_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for time format options"""
        formats = [
            app_commands.Choice(name="Seconds", value="secs"),
            app_commands.Choice(name="Minutes", value="mins"),
            app_commands.Choice(name="Hours", value="hours")
        ]
        return formats

    async def boolean_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Auto-complete function for boolean values"""
        booleans = [
            app_commands.Choice(name="True", value="true"),
            app_commands.Choice(name="False", value="false")
        ]
        return booleans

    @bot.tree.command(name="enablefield", description="Enable a specific field")
    @app_commands.describe(field="Field name to enable")
    @app_commands.autocomplete(field=field_autocomplete)
    async def enable_field(interaction: discord.Interaction, field: str):
        """Enable a specific field"""
        try:
            field = field.lower().replace(" ", "_")
            settings = get_cached_settings()

            # Get the fields list and fields_enabled array
            field_list = settings.get("fields", [])
            fields_enabled = settings.get("fields_enabled", [])

            # Normalize field names for comparison
            normalized_fields = [f.lower().replace(" ", "_") for f in field_list]

            if field not in normalized_fields:
                await interaction.response.send_message(f"❌ Field '{field}' not found. Available fields: {', '.join([f.replace('_', ' ').title() for f in normalized_fields])}")
                return

            # Find the field index
            field_index = normalized_fields.index(field)

            # Update fields_enabled list
            if field_index < len(fields_enabled):
                fields_enabled[field_index] = True
                update_setting("fields_enabled", fields_enabled)
                await interaction.response.send_message(f"✅ Enabled field: {field_list[field_index].title()}")
            else:
                await interaction.response.send_message(f"❌ Field index out of range")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error enabling field: {str(e)}")

    @bot.tree.command(name="disablefield", description="Disable a specific field")
    @app_commands.describe(field="Field name to disable")
    async def disable_field(interaction: discord.Interaction, field: str):
        """Disable a specific field"""
        try:
            field = field.lower().replace(" ", "_")
            settings = get_cached_settings()

            # Get the fields list and fields_enabled array
            field_list = settings.get("fields", [])
            fields_enabled = settings.get("fields_enabled", [])

            # Normalize field names for comparison
            normalized_fields = [f.lower().replace(" ", "_") for f in field_list]

            if field not in normalized_fields:
                await interaction.response.send_message(f"❌ Field '{field}' not found. Available fields: {', '.join([f.replace('_', ' ').title() for f in normalized_fields])}")
                return

            # Find the field index
            field_index = normalized_fields.index(field)

            # Update fields_enabled list
            if field_index < len(fields_enabled):
                fields_enabled[field_index] = False
                update_setting("fields_enabled", fields_enabled)
                await interaction.response.send_message(f"✅ Disabled field: {field_list[field_index].title()}")
            else:
                await interaction.response.send_message(f"❌ Field index out of range")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error disabling field: {str(e)}")

    @bot.tree.command(name="swapfield", description="Swap one field for another")
    @app_commands.describe(current="Current field to replace (e.g., pine_tree)", new="New field to use (e.g., rose)")
    @app_commands.autocomplete(current=field_autocomplete, new=all_fields_autocomplete)
    async def swap_field(interaction: discord.Interaction, current: str, new: str):
        """Swap one field for another in the active fields list"""
        try:
            current_field = current.lower().replace(" ", "_")
            new_field = new.lower().replace(" ", "_")

            settings = get_cached_settings()

            # Get the fields list and fields_enabled array
            field_list = settings.get("fields", [])
            fields_enabled = settings.get("fields_enabled", [])

            # Normalize field names for comparison
            normalized_fields = [f.lower().replace(" ", "_") for f in field_list]

            # Check if current field exists
            if current_field not in normalized_fields:
                available = ', '.join([f.replace('_', ' ').title() for f in normalized_fields])
                await interaction.response.send_message(f"❌ Current field '{current}' not found. Available fields: {available}")
                return

            # Find the field index
            field_index = normalized_fields.index(current_field)

            # Update the field in the list
            original_field_name = field_list[field_index]
            field_list[field_index] = new_field

            # Save the updated fields list
            update_setting("fields", field_list)

            await interaction.response.send_message(f"✅ Swapped field: **{original_field_name.title()}** → **{new_field.replace('_', ' ').title()}**")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error swapping field: {str(e)}")

    # === QUEST MANAGEMENT COMMANDS ===

    @bot.tree.command(name="quests", description="View quest configuration")
    async def view_quests(interaction: discord.Interaction):
        """View current quest configuration"""
        try:
            settings = get_cached_settings()

            quest_settings = {
                "🐻 **Polar Bear**": settings.get("polar_bear_quest", False),
                "🍯 **Honey Bee**": settings.get("honey_bee_quest", False),
                "🐝 **Bucko Bee**": settings.get("bucko_bee_quest", False),
                "🎯 **Riley Bee**": settings.get("riley_bee_quest", False),
                "💧 **Use Gumdrops**": settings.get("quest_use_gumdrops", False)
            }

            embed = discord.Embed(title="📜 Quest Configuration", color=0x00ff00)

            for quest, enabled in quest_settings.items():
                status = "✅ Enabled" if enabled else "❌ Disabled"
                embed.add_field(name=quest, value=status, inline=True)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error retrieving quest settings: {str(e)}")

    @bot.tree.command(name="enablequest", description="Enable a specific quest")
    @app_commands.describe(quest="Quest name to enable (polar_bear, honey_bee, bucko_bee, riley_bee)")
    @app_commands.autocomplete(quest=quest_autocomplete)
    async def enable_quest(interaction: discord.Interaction, quest: str):
        """Enable a specific quest"""
        quest_mapping = {
            "polar_bear": "polar_bear_quest",
            "honey_bee": "honey_bee_quest",
            "bucko_bee": "bucko_bee_quest",
            "riley_bee": "riley_bee_quest"
        }

        quest_key = quest_mapping.get(quest.lower())
        if not quest_key:
            await interaction.response.send_message("❌ Invalid quest name. Use: polar_bear, honey_bee, bucko_bee, or riley_bee")
            return

        success, message = update_setting(quest_key, True)
        await interaction.response.send_message(message)

    @bot.tree.command(name="disablequest", description="Disable a specific quest")
    @app_commands.describe(quest="Quest name to disable (polar_bear, honey_bee, bucko_bee, riley_bee)")
    @app_commands.autocomplete(quest=quest_autocomplete)
    async def disable_quest(interaction: discord.Interaction, quest: str):
        """Disable a specific quest"""
        quest_mapping = {
            "polar_bear": "polar_bear_quest",
            "honey_bee": "honey_bee_quest",
            "bucko_bee": "bucko_bee_quest",
            "riley_bee": "riley_bee_quest"
        }

        quest_key = quest_mapping.get(quest.lower())
        if not quest_key:
            await interaction.response.send_message("❌ Invalid quest name. Use: polar_bear, honey_bee, bucko_bee, or riley_bee")
            return

        success, message = update_setting(quest_key, False)
        await interaction.response.send_message(message)

    # === COLLECTIBLES MANAGEMENT COMMANDS ===

    @bot.tree.command(name="collectibles", description="View collectibles configuration")
    async def view_collectibles(interaction: discord.Interaction):
        """View current collectibles configuration"""
        try:
            settings = get_cached_settings()

            collectible_settings = {
                "🕒 **Wealth Clock**": settings.get("wealth_clock", False),
                "🫐 **Blueberry Dispenser**": settings.get("blueberry_dispenser", False),
                "🍓 **Strawberry Dispenser**": settings.get("strawberry_dispenser", False),
                "🥥 **Coconut Dispenser**": settings.get("coconut_dispenser", False),
                "👑 **Royal Jelly Dispenser**": settings.get("royal_jelly_dispenser", False),
                "🎫 **Ant Pass Dispenser**": settings.get("ant_pass_dispenser", False),
                "🍬 **Treat Dispenser**": settings.get("treat_dispenser", False),
                "🧪 **Glue Dispenser**": settings.get("glue_dispenser", False),
                "🟧 **Honey Storm**": settings.get("honeystorm", False)
            }

            embed = discord.Embed(title="🎁 Collectibles Configuration", color=0x00ff00)

            enabled = []
            disabled = []

            for collectible, is_enabled in collectible_settings.items():
                if is_enabled:
                    enabled.append(collectible)
                else:
                    disabled.append(collectible)

            if enabled:
                embed.add_field(name="✅ **Enabled**", value="\n".join(enabled), inline=False)
            if disabled:
                embed.add_field(name="❌ **Disabled**", value="\n".join(disabled), inline=False)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error retrieving collectible settings: {str(e)}")

    @bot.tree.command(name="enablecollectible", description="Enable a specific collectible")
    @app_commands.describe(collectible="Collectible name to enable")
    @app_commands.autocomplete(collectible=collectible_autocomplete)
    async def enable_collectible(interaction: discord.Interaction, collectible: str):
        """Enable a specific collectible"""
        collectible_mapping = {
            "wealth_clock": "wealth_clock",
            "blueberry": "blueberry_dispenser",
            "strawberry": "strawberry_dispenser",
            "coconut": "coconut_dispenser",
            "royal_jelly": "royal_jelly_dispenser",
            "ant_pass": "ant_pass_dispenser",
            "treat": "treat_dispenser",
            "glue": "glue_dispenser",
            "honeystorm": "honeystorm"
        }

        collectible_key = collectible_mapping.get(collectible.lower().replace(" ", "_"))
        if not collectible_key:
            await interaction.response.send_message("❌ Invalid collectible name")
            return

        success, message = update_setting(collectible_key, True)
        await interaction.response.send_message(message)

    @bot.tree.command(name="disablecollectible", description="Disable a specific collectible")
    @app_commands.describe(collectible="Collectible name to disable")
    @app_commands.autocomplete(collectible=collectible_autocomplete)
    async def disable_collectible(interaction: discord.Interaction, collectible: str):
        """Disable a specific collectible"""
        collectible_mapping = {
            "wealth_clock": "wealth_clock",
            "blueberry": "blueberry_dispenser",
            "strawberry": "strawberry_dispenser",
            "coconut": "coconut_dispenser",
            "royal_jelly": "royal_jelly_dispenser",
            "ant_pass": "ant_pass_dispenser",
            "treat": "treat_dispenser",
            "glue": "glue_dispenser",
            "honeystorm": "honeystorm"
        }

        collectible_key = collectible_mapping.get(collectible.lower().replace(" ", "_"))
        if not collectible_key:
            await interaction.response.send_message("❌ Invalid collectible name")
            return

        success, message = update_setting(collectible_key, False)
        await interaction.response.send_message(message)

    # === PLANTER MANAGEMENT COMMANDS ===
    '''
    @bot.tree.command(name="planters", description="View planter configuration")
    async def view_planters(interaction: discord.Interaction):
        """View current planter configuration"""
        try:
            settings = get_cached_settings()

            embed = discord.Embed(title="🌱 Planter Configuration", color=0x00ff00)

            # Planter mode
            mode = settings.get("planters_mode", 0)
            mode_text = {0: "Disabled", 1: "Manual", 2: "Auto"}.get(mode, "Unknown")
            embed.add_field(name="🎛️ **Mode**", value=mode_text, inline=True)

            # Auto planter settings
            if mode == 2:
                embed.add_field(name="🔢 **Max Planters**", value=settings.get("auto_max_planters", 3), inline=True)
                embed.add_field(name="🎨 **Preset**", value=settings.get("auto_preset", "blue"), inline=True)

                # Show priority settings
                priority_text = []
                for i in range(5):
                    nectar = settings.get(f"auto_priority_{i}_nectar", "none")
                    min_val = settings.get(f"auto_priority_{i}_min", 0)
                    if nectar != "none":
                        priority_text.append(f"#{i+1}: {nectar} ({min_val}%)")

                embed.add_field(name="📊 **Nectar Priorities**", value="\n".join(priority_text) if priority_text else "None", inline=False)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error retrieving planter settings: {str(e)}")

    @bot.tree.command(name="setplantermode", description="Set planter mode (0=disabled, 1=manual, 2=auto)")
    @app_commands.describe(mode="Planter mode (0=disabled, 1=manual, 2=auto)")
    @app_commands.autocomplete(mode=planter_mode_autocomplete)
    async def set_planter_mode(interaction: discord.Interaction, mode: int):
        """Set planter mode"""
        if mode not in [0, 1, 2]:
            await interaction.response.send_message("❌ Invalid mode. Use 0 (disabled), 1 (manual), or 2 (auto)")
            return

        success, message = update_setting("planters_mode", mode)
        await interaction.response.send_message(message)

    @bot.tree.command(name="setmaxplanters", description="Set maximum number of auto planters")
    @app_commands.describe(count="Maximum number of planters (1-3)")
    async def set_max_planters(interaction: discord.Interaction, count: int):
        """Set maximum number of auto planters"""
        if count < 1 or count > 3:
            await interaction.response.send_message("❌ Count must be between 1 and 3")
            return

        success, message = update_setting("auto_max_planters", count)
        await interaction.response.send_message(message)
    '''
    # === MOB RUN COMMANDS ===

    @bot.tree.command(name="mobs", description="View mob run configuration")
    async def view_mobs(interaction: discord.Interaction):
        """View current mob run configuration"""
        try:
            settings = get_cached_settings()

            mob_settings = {
                "🐞 **Ladybug**": settings.get("ladybug", False),
                "🪲 **Rhinobeetle**": settings.get("rhinobeetle", False),
                "🦂 **Scorpion**": settings.get("scorpion", False),
                "🦗 **Mantis**": settings.get("mantis", False),
                "🕷️ **Spider**": settings.get("spider", False),
                "🐺 **Werewolf**": settings.get("werewolf", False),
                "🦀 **Coconut Crab**": settings.get("coconut_crab", False),
                "🐌 **Stump Snail**": settings.get("stump_snail", False)
            }

            embed = discord.Embed(title="🐛 Mob Run Configuration", color=0x00ff00)

            enabled = []
            disabled = []

            for mob, is_enabled in mob_settings.items():
                if is_enabled:
                    enabled.append(mob)
                else:
                    disabled.append(mob)

            if enabled:
                embed.add_field(name="✅ **Enabled**", value="\n".join(enabled), inline=False)
            if disabled:
                embed.add_field(name="❌ **Disabled**", value="\n".join(disabled), inline=False)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error retrieving mob settings: {str(e)}")

    @bot.tree.command(name="enablemob", description="Enable a specific mob run")
    @app_commands.describe(mob="Mob name to enable")
    @app_commands.autocomplete(mob=mob_autocomplete)
    async def enable_mob(interaction: discord.Interaction, mob: str):
        """Enable a specific mob run"""
        mob_mapping = {
            "ladybug": "ladybug",
            "rhinobeetle": "rhinobeetle",
            "scorpion": "scorpion",
            "mantis": "mantis",
            "spider": "spider",
            "werewolf": "werewolf",
            "coconut_crab": "coconut_crab",
            "stump_snail": "stump_snail"
        }

        mob_key = mob_mapping.get(mob.lower().replace(" ", "_"))
        if not mob_key:
            await interaction.response.send_message("❌ Invalid mob name")
            return

        success, message = update_setting(mob_key, True)
        await interaction.response.send_message(message)

    @bot.tree.command(name="disablemob", description="Disable a specific mob run")
    @app_commands.describe(mob="Mob name to disable")
    @app_commands.autocomplete(mob=mob_autocomplete)
    async def disable_mob(interaction: discord.Interaction, mob: str):
        """Disable a specific mob run"""
        mob_mapping = {
            "ladybug": "ladybug",
            "rhinobeetle": "rhinobeetle",
            "scorpion": "scorpion",
            "mantis": "mantis",
            "spider": "spider",
            "werewolf": "werewolf",
            "coconut_crab": "coconut_crab",
            "stump_snail": "stump_snail"
        }

        mob_key = mob_mapping.get(mob.lower().replace(" ", "_"))
        if not mob_key:
            await interaction.response.send_message("❌ Invalid mob name")
            return

        success, message = update_setting(mob_key, False)
        await interaction.response.send_message(message)

    '''
    # === PROFILE MANAGEMENT COMMANDS ===

    @bot.tree.command(name="profiles", description="List available profiles")
    async def list_profiles(interaction: discord.Interaction):
        """List available profiles"""
        try:
            profiles_dir = "../settings/profiles"
            if os.path.exists(profiles_dir):
                profiles = [d for d in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, d))]
                if profiles:
                    embed = discord.Embed(title="📁 Available Profiles", color=0x00ff00)
                    embed.add_field(name="Profiles", value="\n".join(f"• `{p}`" for p in profiles), inline=False)
                    embed.set_footer(text="Use /switchprofile <name> to switch profiles")
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("❌ No profiles found")
            else:
                await interaction.response.send_message("❌ Profiles directory not found")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error listing profiles: {str(e)}")

    @bot.tree.command(name="currentprofile", description="Show current profile")
    async def current_profile(interaction: discord.Interaction):
        """Show current profile"""
        try:
            current_profile = settingsManager.profileName
            await interaction.response.send_message(f"📁 **Current Profile:** `{current_profile}`")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error getting current profile: {str(e)}")

    @bot.tree.command(name="switchprofile", description="Switch to a different profile")
    @app_commands.describe(profile="Profile name to switch to")
    async def switch_profile(interaction: discord.Interaction, profile: str):
        """Switch to a different profile"""
        try:
            profiles_dir = "../settings/profiles"
            profile_path = os.path.join(profiles_dir, profile)

            if not os.path.exists(profile_path) or not os.path.isdir(profile_path):
                await interaction.response.send_message(f"❌ Profile '{profile}' not found")
                return

            # Update the profile name in settingsManager
            settingsManager.profileName = profile
            clear_settings_cache()

            await interaction.response.send_message(f"✅ Switched to profile: `{profile}`")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error switching profile: {str(e)}")
    '''
    
    @bot.tree.command(name="help", description="Show available commands")
    async def help_command(interaction: discord.Interaction):
        """Show available commands"""
        embed = discord.Embed(title="🤖 BSS Macro Discord Bot", description="Available Commands:", color=0x0099ff)

        embed.add_field(name="🔧 **Basic Controls**", value="`/ping` - Check if bot is online\n`/start` - Start the macro\n`/stop` - Stop the macro\n`/rejoin` - Make macro rejoin game\n`/screenshot` - Get screenshot\n`/settings` - View current settings", inline=False)

        embed.add_field(name="🌾 **Field Management**", value="`/fields` - View field configuration\n`/enablefield <field>` - Enable a field\n`/disablefield <field>` - Disable a field\n`/swapfield <current> <new>` - Swap one field for another (new can be any field)", inline=False)

        embed.add_field(name="📜 **Quest Management**", value="`/quests` - View quest configuration\n`/enablequest <quest>` - Enable a quest\n`/disablequest <quest>` - Disable a quest", inline=False)

        embed.add_field(name="🎁 **Collectibles**", value="`/collectibles` - View collectibles\n`/enablecollectible <item>` - Enable collectible\n`/disablecollectible <item>` - Disable collectible", inline=False)

        # embed.add_field(name="🌱 **Planters**", value="`/planters` - View planter config\n`/setplantermode <mode>` - Set planter mode\n`/setmaxplanters <count>` - Set max planters", inline=False)

        embed.add_field(name="🐛 **Mob Runs**", value="`/mobs` - View mob configuration\n`/enablemob <mob>` - Enable mob run\n`/disablemob <mob>` - Disable mob run", inline=False)

        # embed.add_field(name="📁 **Profile Management**", value="`/profiles` - List available profiles\n`/currentprofile` - Show current profile\n`/switchprofile <name>` - Switch profile", inline=False)

        embed.add_field(name="📊 **Status & Monitoring**", value="`/status` - Get macro status\n`/battery` - Check battery status\n`/streamurl` - Get stream URL", inline=False)

        await interaction.response.send_message(embed=embed)

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
