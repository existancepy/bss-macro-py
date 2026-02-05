import ast
import os
import shutil
import json
import zipfile
import tempfile
from datetime import datetime

#returns a dictionary containing the settings
profileName = "a"
# Track profile changes for running macro processes
_profile_change_counter = 0

# File to store current profile persistence (defined after getProjectRoot)
CURRENT_PROFILE_FILE = None

def loadCurrentProfile():
    """Load the current profile from persistent storage"""
    global profileName
    try:
        if os.path.exists(CURRENT_PROFILE_FILE):
            with open(CURRENT_PROFILE_FILE, "r") as f:
                saved_profile = f.read().strip()
                if saved_profile and os.path.exists(getProfilePath(saved_profile)):
                    profileName = saved_profile
    except Exception as e:
        print(f"Warning: Could not load current profile: {e}")

def saveCurrentProfile():
    """Save the current profile to persistent storage"""
    try:
        with open(CURRENT_PROFILE_FILE, "w") as f:
            f.write(profileName)
    except Exception as e:
        print(f"Warning: Could not save current profile: {e}")

# Load the current profile when the module is imported (called at the end of the file)

# Get the project root directory (4 levels up from this file: src/modules/misc/settingsManager.py)
def getProjectRoot():
    """Get the project root directory path"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# File to store current profile persistence
CURRENT_PROFILE_FILE = os.path.join(getProjectRoot(), "src", "data", "user", "current_profile.txt")

# Helper functions for common paths
def getProfilesDir():
    """Get the profiles directory path"""
    return os.path.join(getProjectRoot(), "settings", "profiles")

def getProfilePath(profile_name=None):
    """Get the path to a specific profile directory"""
    if profile_name is None:
        profile_name = profileName
    return os.path.join(getProfilesDir(), profile_name)

def getDefaultSettingsPath():
    """Get the path to default settings directory"""
    return os.path.join(getProjectRoot(), "src", "data", "default_settings")

def getSettingsDir():
    """Get the settings directory path"""
    return os.path.join(getProjectRoot(), "settings")

def getPatternsDir():
    """Get the patterns directory path"""
    return os.path.join(getProjectRoot(), "settings", "patterns")

def getMacroVersion():
    """Get the macro version from version.txt file"""
    try:
        version_file = os.path.join(getProjectRoot(), "version.txt")
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                version = f.read().strip()
                return version if version else "1.0"
    except Exception as e:
        print(f"Warning: Could not read version.txt: {e}")
    return "1.0"

def listProfiles():
    """List all available profiles"""
    profiles_dir = getProfilesDir()
    if os.path.exists(profiles_dir):
        profiles = [d for d in os.listdir(profiles_dir) 
                   if os.path.isdir(os.path.join(profiles_dir, d)) and not d.startswith('.')]
        return sorted(profiles)
    return []

def getCurrentProfile():
    """Get the current profile name"""
    global profileName
    return profileName

def getProfileChangeCounter():
    """Get the profile change counter for detecting profile switches"""
    global _profile_change_counter
    return _profile_change_counter

def switchProfile(name):
    """Switch to a different profile"""
    global profileName
    profiles_dir = getProfilesDir()
    profile_path = os.path.join(profiles_dir, name)

    if not os.path.exists(profile_path) or not os.path.isdir(profile_path):
        return False, f"Profile '{name}' not found"

    # Check if required profile files exist
    settings_file = os.path.join(profile_path, "settings.txt")
    fields_file = os.path.join(profile_path, "fields.txt")
    generalsettings_file = os.path.join(profile_path, "generalsettings.txt")

    if not os.path.exists(settings_file):
        return False, f"Profile '{name}' is missing settings.txt file"

    if not os.path.exists(fields_file):
        return False, f"Profile '{name}' is missing fields.txt file"

    if not os.path.exists(generalsettings_file):
        return False, f"Profile '{name}' is missing generalsettings.txt file"

    profileName = name
    # Save the profile selection persistently
    saveCurrentProfile()
    # Increment the change counter to notify running processes
    global _profile_change_counter
    _profile_change_counter += 1

    # Sync the new profile's field settings to general settings
    initializeFieldSync()

    return True, f"Switched to profile: {name}"

def createProfile(name):
    """Create a new profile using default settings from settings/defaults/"""
    global profileName
    profiles_dir = getProfilesDir()

    # Sanitize the profile name
    name = name.strip().replace(' ', '_').lower()
    if not name:
        return False, "Profile name cannot be empty"

    # Check if profile already exists
    new_profile_path = os.path.join(profiles_dir, name)
    if os.path.exists(new_profile_path):
        return False, f"Profile '{name}' already exists"

    # Create the new profile directory
    try:
        os.makedirs(new_profile_path)

        # Copy default profile settings (fields.txt and settings.txt)
        default_profile_path = os.path.join(getProjectRoot(), "settings", "defaults", "profiles", "a")
        if os.path.exists(default_profile_path):
            for file_name in ["fields.txt", "settings.txt"]:
                src_file = os.path.join(default_profile_path, file_name)
                dst_file = os.path.join(new_profile_path, file_name)
                if os.path.exists(src_file):
                    shutil.copy2(src_file, dst_file)

        # Copy default generalsettings.txt
        default_generalsettings = os.path.join(getProjectRoot(), "settings", "defaults", "generalsettings.txt")
        if os.path.exists(default_generalsettings):
            dst_generalsettings = os.path.join(new_profile_path, "generalsettings.txt")
            shutil.copy2(default_generalsettings, dst_generalsettings)

        return True, f"Created profile: {name}"
    except Exception as e:
        # Clean up partial profile if creation failed
        if os.path.exists(new_profile_path):
            shutil.rmtree(new_profile_path)
        return False, f"Failed to create profile: {str(e)}"

def deleteProfile(name):
    """Delete a profile (cannot delete current or last profile)"""
    global profileName
    profiles_dir = getProfilesDir()
    
    # Cannot delete current profile
    if name == profileName:
        return False, "Cannot delete the currently active profile"
    
    # Cannot delete if it's the only profile
    profiles = listProfiles()
    if len(profiles) <= 1:
        return False, "Cannot delete the only remaining profile"
    
    profile_path = os.path.join(profiles_dir, name)
    if not os.path.exists(profile_path):
        return False, f"Profile '{name}' not found"
    
    try:
        shutil.rmtree(profile_path)
        return True, f"Deleted profile: {name}"
    except Exception as e:
        return False, f"Failed to delete profile: {str(e)}"

def renameProfile(old_name, new_name):
    """Rename a profile"""
    global profileName
    profiles_dir = getProfilesDir()
    
    # Sanitize the new name
    new_name = new_name.strip().replace(' ', '_').lower()
    if not new_name:
        return False, "New profile name cannot be empty"
    
    old_path = os.path.join(profiles_dir, old_name)
    new_path = os.path.join(profiles_dir, new_name)
    
    if not os.path.exists(old_path):
        return False, f"Profile '{old_name}' not found"
    
    if os.path.exists(new_path):
        return False, f"Profile '{new_name}' already exists"
    
    try:
        os.rename(old_path, new_path)
        # If we renamed the current profile, update the reference
        if old_name == profileName:
            profileName = new_name
        return True, f"Renamed profile from '{old_name}' to '{new_name}'"
    except Exception as e:
        return False, f"Failed to rename profile: {str(e)}"

def duplicateProfile(source_name, new_name):
    """Duplicate an existing profile with a new name"""
    profiles_dir = getProfilesDir()
    
    # Sanitize the new name
    new_name = new_name.strip().replace(' ', '_').lower()
    if not new_name:
        return False, "New profile name cannot be empty"
    
    source_path = os.path.join(profiles_dir, source_name)
    new_path = os.path.join(profiles_dir, new_name)
    
    if not os.path.exists(source_path):
        return False, f"Source profile '{source_name}' not found"
    
    if os.path.exists(new_path):
        return False, f"Profile '{new_name}' already exists"
    
    try:
        shutil.copytree(source_path, new_path)
        return True, f"Duplicated profile '{source_name}' as '{new_name}'"
    except Exception as e:
        return False, f"Failed to duplicate profile: {str(e)}"

def readSettingsFile(path):
    #get each line
    #read the file, format it to:
    #[[key, value], [key, value]]
    with open(path) as f:
        data = [[x.strip() for x in y.split("=", 1)] for y in f.read().split("\n") if y]
    f.close()
    #convert to a dict
    out = {}
    for k,v in data:
        try:
            out[k] = ast.literal_eval(v)
        except:
            #check if integer
            if v.isdigit():
                out[k] = int(v)
            elif v.replace(".","",1).isdigit():
                out[k] = float(v)
            out[k] = v
    return out

def saveDict(path, data):
    out = "\n".join([f"{k}={v}" for k,v in data.items()])
    with open(path, "w") as f:
        f.write(str(out))
    f.close()

#update one property of a setting
def saveSettingFile(setting,value, path):
    #get the dictionary
    data = readSettingsFile(path)
    #update the dictionary
    data[setting] = value
    #write it
    saveDict(path, data)

def removeSettingFile(setting, path):
    #get the dictionary
    data = readSettingsFile(path)
    #remove the setting if it exists
    if setting in data:
        del data[setting]
        #write it back
        saveDict(path, data)

def loadFields():
    fields_path = os.path.join(getProfilePath(), "fields.txt")
    with open(fields_path) as f:
        out = ast.literal_eval(f.read())
    f.close()
    
    # Auto-add missing goo settings for backward compatibility
    # This ensures users upgrading from older versions get the new goo functionality
    fieldsUpdated = False
    for field, settings in out.items():
        # Add missing goo settings if they don't exist
        if "goo" not in settings:
            settings["goo"] = False  # Default to disabled
            fieldsUpdated = True
        if "goo_interval" not in settings:
            settings["goo_interval"] = 3  # Default to 3 seconds (minimum allowed)
            fieldsUpdated = True
    
    # Save the updated fields if any were modified
    if fieldsUpdated:
        with open(fields_path, "w") as f:
            f.write(str(out))
        f.close()
    
    for field,settings in out.items():
        for k,v in settings.items():
            #check if integer
            if isinstance(v,str): 
                if v.isdigit(): out[field][k] = int(v)
                elif v.replace(".","",1).isdigit(): out[field][k] = float(v)
    return out

def saveField(field, settings):
    fieldsData = loadFields()
    fieldsData[field] = settings
    fields_path = os.path.join(getProfilePath(), "fields.txt")
    with open(fields_path, "w") as f:
        f.write(str(fieldsData))
    f.close()

def exportFieldSettings(field_name):
    """Export field settings as JSON string with metadata"""
    fields_data = loadFields()
    if field_name in fields_data:
        # Create export data with metadata
        export_data = {
            "metadata": {
                "field_name": field_name,
                "macro_version": getMacroVersion(),
                "export_date": datetime.now().isoformat()
            },
            "settings": fields_data[field_name]
        }
        return json.dumps(export_data, indent=2)
    else:
        raise ValueError(f"Field '{field_name}' not found in current profile")

def importFieldSettings(field_name, json_settings):
    """Import field settings from JSON string with backward compatibility"""
    try:
        data = json.loads(json_settings)
        
        # Handle new format with metadata
        if isinstance(data, dict) and "metadata" in data and "settings" in data:
            settings = data["settings"]
            metadata = data.get("metadata", {})
            exported_field = metadata.get("field_name", "unknown")
            macro_version = metadata.get("macro_version", "unknown")
        # Handle old format (direct settings object)
        else:
            settings = data
            exported_field = "unknown"
            macro_version = "unknown"
        
        # Validate that settings is a dictionary
        if not isinstance(settings, dict):
            raise ValueError("Invalid JSON format: expected object")

        # Check for missing patterns and replace with defaults
        missing_patterns = []
        available_patterns = getAvailablePatterns()

        if "shape" in settings:
            requested_pattern = settings["shape"]
            if requested_pattern not in available_patterns:
                # Replace with first available pattern (default)
                default_pattern = available_patterns[0] if available_patterns else "cornerxe_lol"
                settings["shape"] = default_pattern
                missing_patterns.append(f"'{requested_pattern}' → '{default_pattern}'")

        # Save the imported settings
        saveField(field_name, settings)

        # Return success with information about any pattern replacements and metadata
        result = {
            "success": True,
            "missing_patterns": missing_patterns,
            "imported_from_field": exported_field,
            "macro_version": macro_version
        }
        return result

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")

def getAvailablePatterns():
    """Get list of available pattern names"""
    patterns_dir = getPatternsDir()
    if os.path.exists(patterns_dir):
        return [f.replace(".py", "") for f in os.listdir(patterns_dir) if f.endswith(".py")]
    return []

def syncFieldSettings(setting, value):
    """Synchronize field settings from profile to general settings"""
    try:
        # Update the general settings file
        generalSettingsPath = os.path.join(getProfilePath(), "generalsettings.txt")
        generalData = readSettingsFile(generalSettingsPath)
        generalData[setting] = value
        saveDict(generalSettingsPath, generalData)
    except Exception as e:
        print(f"Warning: Could not sync field settings to general settings: {e}")

def syncFieldSettingsToProfile(setting, value):
    """Synchronize field settings from general to profile settings"""
    try:
        # Update the profile settings file
        profileSettingsPath = os.path.join(getProfilePath(), "settings.txt")
        profileData = readSettingsFile(profileSettingsPath)
        profileData[setting] = value
        saveDict(profileSettingsPath, profileData)
    except Exception as e:
        print(f"Warning: Could not sync field settings to profile settings: {e}")

def saveProfileSetting(setting, value):
    settings_path = os.path.join(getProfilePath(), "settings.txt")
    saveSettingFile(setting, value, settings_path)
    # Synchronize field settings with general settings
    if setting in ["fields", "fields_enabled"]:
        syncFieldSettings(setting, value)

def saveDictProfileSettings(dict):
    settings_path = os.path.join(getProfilePath(), "settings.txt")
    saveDict(settings_path, {**readSettingsFile(settings_path), **dict})

#increment a setting, and return the dictionary for the setting
def incrementProfileSetting(setting, incrValue):
    #get the dictionary
    settings_path = os.path.join(getProfilePath(), "settings.txt")
    data = readSettingsFile(settings_path)
    #update the dictionary
    data[setting] += incrValue
    #write it
    saveDict(settings_path, data)
    return data

def saveGeneralSetting(setting, value):
    generalsettings_path = os.path.join(getProfilePath(), "generalsettings.txt")
    saveSettingFile(setting, value, generalsettings_path)
    # Synchronize field settings with profile settings
    if setting in ["fields", "fields_enabled"]:
        syncFieldSettingsToProfile(setting, value)

def removeGeneralSetting(setting):
    generalsettings_path = os.path.join(getProfilePath(), "generalsettings.txt")
    removeSettingFile(setting, generalsettings_path)

def loadSettings():
    settings_path = os.path.join(getProfilePath(), "settings.txt")
    default_settings_path = os.path.join(getDefaultSettingsPath(), "settings.txt")
    try:
        settings = readSettingsFile(settings_path)
    except FileNotFoundError:
        print(f"Warning: Profile '{profileName}' settings file not found, using defaults")
        # Fall back to default settings if profile file is missing
        settings = readSettingsFile(default_settings_path)

    # Ensure fields and fields_enabled arrays have 5 elements
    defaultSettings = readSettingsFile(default_settings_path)
    defaultFields = defaultSettings.get("fields", ['pine tree', 'sunflower', 'dandelion', 'pine tree', 'sunflower'])
    defaultFieldsEnabled = defaultSettings.get("fields_enabled", [True, False, False, False, False])
    
    fields = settings.get("fields", [])
    fieldsEnabled = settings.get("fields_enabled", [])
    
    # Extend arrays to 5 elements if needed
    updated = False
    while len(fields) < 5:
        fields.append(defaultFields[len(fields)] if len(fields) < len(defaultFields) else defaultFields[-1])
        updated = True
    while len(fieldsEnabled) < 5:
        fieldsEnabled.append(defaultFieldsEnabled[len(fieldsEnabled)] if len(fieldsEnabled) < len(defaultFieldsEnabled) else False)
        updated = True
    
    if updated:
        settings["fields"] = fields
        settings["fields_enabled"] = fieldsEnabled
        saveDict(settings_path, settings)
    
    return settings

#return a dict containing all settings except field (general, profile, planters)
def loadAllSettings():
    # Auto-migrate profiles to have their own generalsettings.txt files
    migrateProfilesToGeneralSettings()

    generalsettings_path = os.path.join(getProfilePath(), "generalsettings.txt")
    try:
        generalSettings = readSettingsFile(generalsettings_path)
    except FileNotFoundError:
        # Fall back to global generalsettings if profile-specific one doesn't exist
        print(f"Warning: Profile '{profileName}' generalsettings file not found, using global generalsettings")
        generalSettings = readSettingsFile(generalsettings_path)

    # Migrate old boolean flags to new macro_mode setting
    migrated = False
    field_only = generalSettings.get("field_only_mode", False)
    quest_only = generalSettings.get("quest_only_mode", False)

    # Check if old settings exist (regardless of their value)
    if "field_only_mode" in generalSettings or "quest_only_mode" in generalSettings:
        if field_only and quest_only:
            # If both are somehow true, prioritize field mode
            generalSettings["macro_mode"] = "field"
        elif field_only:
            generalSettings["macro_mode"] = "field"
        elif quest_only:
            generalSettings["macro_mode"] = "quest"
        else:
            generalSettings["macro_mode"] = "normal"

        # Remove old settings
        if "field_only_mode" in generalSettings:
            del generalSettings["field_only_mode"]
            migrated = True
        if "quest_only_mode" in generalSettings:
            del generalSettings["quest_only_mode"]
            migrated = True

        # Save the migrated settings back to file
        if migrated:
            saveDict(generalsettings_path, generalSettings)
            print("Migrated old field_only_mode/quest_only_mode settings to new macro_mode setting")

    return {**loadSettings(), **generalSettings}

def initializeFieldSync():
    """Initialize field synchronization between profile and general settings"""
    try:
        settings_path = os.path.join(getProfilePath(), "settings.txt")
        generalsettings_path = os.path.join(getProfilePath(), "generalsettings.txt")
        try:
            profileData = readSettingsFile(settings_path)
        except FileNotFoundError:
            print(f"Warning: Profile '{profileName}' settings file not found during sync, skipping")
            return

        generalData = readSettingsFile(generalsettings_path)

        # Check if field settings exist in both files
        profileFields = profileData.get("fields", [])
        generalFields = generalData.get("fields", [])

        # If general settings has different fields, sync from profile to general
        if profileFields != generalFields and profileFields:
            generalData["fields"] = profileFields
            saveDict(generalsettings_path, generalData)

        # Sync fields_enabled as well
        profileFieldsEnabled = profileData.get("fields_enabled", [])
        generalFieldsEnabled = generalData.get("fields_enabled", [])

        if profileFieldsEnabled != generalFieldsEnabled and profileFieldsEnabled:
            generalData["fields_enabled"] = profileFieldsEnabled
            saveDict(generalsettings_path, generalData)
            
    except Exception as e:
        print(f"Warning: Could not initialize field synchronization: {e}")

def exportProfile(profile_name):
    """Export a profile to JSON content for browser download"""
    profiles_dir = getProfilesDir()
    profile_path = os.path.join(profiles_dir, profile_name)

    if not os.path.exists(profile_path):
        return False, f"Profile '{profile_name}' not found"

    # Read profile data
    try:
        settings_file = os.path.join(profile_path, "settings.txt")
        fields_file = os.path.join(profile_path, "fields.txt")
        generalsettings_file = os.path.join(profile_path, "generalsettings.txt")

        if not os.path.exists(settings_file) or not os.path.exists(fields_file) or not os.path.exists(generalsettings_file):
            return False, f"Profile '{profile_name}' is missing required files"

        settings_data = readSettingsFile(settings_file)
        fields_data = loadFields() if profile_name == getCurrentProfile() else ast.literal_eval(open(fields_file).read())
        generalsettings_data = readSettingsFile(generalsettings_file)

        # Create export data structure
        export_data = {
            "profile_name": profile_name,
            "export_date": datetime.now().isoformat(),
            "version": "1.0",
            "settings": settings_data,
            "fields": fields_data,
            "generalsettings": generalsettings_data
        }

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profile_{profile_name}_{timestamp}.json"

        # Return JSON content and filename
        json_content = json.dumps(export_data, indent=2, ensure_ascii=False)
        return True, json_content, filename

    except Exception as e:
        return False, f"Failed to export profile: {str(e)}"

def importProfile(import_path, new_profile_name=None):
    """Import a profile from a JSON file"""
    if not os.path.exists(import_path):
        return False, f"Import file '{import_path}' not found"

    try:
        # Read and validate import data
        with open(import_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)

        return _importProfileData(import_data, new_profile_name)
    except Exception as e:
        return False, f"Failed to import profile: {str(e)}"

def importProfileContent(json_content, new_profile_name=None):
    """Import a profile from JSON content string"""
    try:
        import_data = json.loads(json_content)
        return _importProfileData(import_data, new_profile_name)
    except json.JSONDecodeError:
        return False, "Invalid JSON content"
    except Exception as e:
        return False, f"Failed to import profile: {str(e)}"

def _importProfileData(import_data, new_profile_name=None):
    """Internal function to import profile data"""
    try:
        # Validate structure
        required_keys = ["profile_name", "settings", "fields", "generalsettings"]
        for key in required_keys:
            if key not in import_data:
                return False, f"Invalid import file: missing '{key}' key"

        # Determine new profile name
        if new_profile_name is None:
            original_name = import_data["profile_name"]
            new_profile_name = original_name
            counter = 1
            while os.path.exists(os.path.join(getProfilesDir(), new_profile_name)):
                new_profile_name = f"{original_name}_imported_{counter}"
                counter += 1

        # Sanitize profile name
        new_profile_name = new_profile_name.strip().replace(' ', '_').lower()
        if not new_profile_name:
            return False, "Profile name cannot be empty"

        # Check if profile already exists
        new_profile_path = os.path.join(getProfilesDir(), new_profile_name)
        if os.path.exists(new_profile_path):
            return False, f"Profile '{new_profile_name}' already exists"

        # Create profile directory
        os.makedirs(new_profile_path)

        # Write settings file
        settings_file = os.path.join(new_profile_path, "settings.txt")
        saveDict(settings_file, import_data["settings"])

        # Write fields file
        fields_file = os.path.join(new_profile_path, "fields.txt")
        with open(fields_file, 'w') as f:
            f.write(str(import_data["fields"]))

        # Write generalsettings file
        generalsettings_file = os.path.join(new_profile_path, "generalsettings.txt")
        saveDict(generalsettings_file, import_data["generalsettings"])

        return True, f"Profile imported successfully as '{new_profile_name}'"

    except Exception as e:
        return False, f"Failed to import profile: {str(e)}"

# Load the current profile when the module is imported
loadCurrentProfile()

#clear a file
def clearFile(filePath):
    open(filePath, 'w').close()

def migrateProfilesToGeneralSettings():
    """Migrate existing profiles to have their own generalsettings.txt files"""
    profiles_dir = getProfilesDir()
    global_generalsettings = os.path.join(getSettingsDir(), "generalsettings.txt")

    # Check if global generalsettings exists - if not, migration is already complete
    if not os.path.exists(global_generalsettings):
        return

    if not os.path.exists(profiles_dir):
        return

    # Read global generalsettings
    try:
        global_data = readSettingsFile(global_generalsettings)
    except FileNotFoundError:
        print("Warning: Global generalsettings.txt not found, cannot migrate profiles")
        return

    migration_performed = False

    # Iterate through all profiles
    for profile_name in listProfiles():
        profile_path = os.path.join(profiles_dir, profile_name)
        generalsettings_file = os.path.join(profile_path, "generalsettings.txt")

        # Skip if profile already has generalsettings.txt
        if os.path.exists(generalsettings_file):
            continue

        # Copy global generalsettings to profile
        try:
            shutil.copy2(global_generalsettings, generalsettings_file)
            print(f"Migrated generalsettings.txt for profile: {profile_name}")
            migration_performed = True
        except Exception as e:
            print(f"Warning: Failed to migrate generalsettings.txt for profile '{profile_name}': {e}")

    # Only print completion message and delete old file if migration was actually performed
    if migration_performed:
        print("Profile migration completed")

        # Delete the old global generalsettings file since all profiles now have their own copies
        try:
            os.remove(global_generalsettings)
            print("Removed old global generalsettings.txt file")
        except Exception as e:
            print(f"Warning: Failed to remove old global generalsettings.txt file: {e}")