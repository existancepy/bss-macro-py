
# Bee Swarm Python Macro

Made and tested on mac, currently untested for windows/linux.



## Features

- Gathering for all fields
- Gather patterns: e_lol/squares/snake/spiral
- GUI for setup
- Automatic calibration
- Disconnect check + auto reconnect
- Discord webhook
- Field Drift Compensation
- Wealth clock and dispenser collections
- Bug runs + Stump Snail

## In-Game Requirements
- Glider 
- Access to the red canon


## Social Links
- Discord: https://discord.gg/FTB8b2vB6y (Thanks to kay for setting it up)



## Setting up the environment

### MacOS lower than 10.13

1. Install [python 3.8](https://www.python.org/downloads/release/python-380/)

2. Open Terminal

**For M1 Macs**
 - Go to finder -> applications -> utilities -> right click terminal -> get info -> enable "open using rosetta"

 **You can open terminal through 2 ways:**
 - cmd + space to bring up spotlight, search "terminal" and hit enter
 - finder -> applications -> utilities -> terminal

    
3. In Terminal, enter the following command:
```bash
pip3 install opencv-python==4.1.2.30
```
Wait for it to finish installing, then enter:
```bash
pip3 install pyautogui pillow python-imagesearch discord-webhook discord.py
```

### MacOS lower than 12.0 (10.13 - 12.0)

1. Install [python 3.8](https://www.python.org/downloads/release/python-380/)

2. Open Terminal

**For M1 Macs**

 - Go to finder -> applications -> utilities -> right click terminal -> get info -> enable "open using rosetta"

 **You can open terminal through 2 ways:**
 - cmd + space to bring up spotlight, search "terminal" and hit enter
 - finder -> applications -> utilities -> terminal

    
3. In Terminal, enter the following command:
```bash
pip3 install opencv-python==4.3.0.36
```
Wait for it to finish installing, then enter:
```bash
pip3 install pyautogui pillow python-imagesearch discord-webhook discord.py
```

### MacOS 12.0 and higher

1. Install [python 3.9.5](https://www.python.org/downloads/release/python-395/)

2. Open Terminal

**For M1 Macs**

 - Go to finder -> applications -> utilities -> right click terminal -> get info -> enable "open using rosetta"

 **You can open terminal through 2 ways:**
 - cmd + space to bring up spotlight, search "terminal" and hit enter
 - finder -> applications -> utilities -> terminal

    
3. In Terminal, enter the following command:
```bash
pip3 install pyautogui pillow opencv-python python-imagesearch discord-webhook keyboard discord.py
```


    
## Macro Installation
1. Download the files in this github repo (Code -> download zip)




![App Screenshot](https://cdn.discordapp.com/attachments/1065032948119769121/1065033447963373690/Screen_Shot_2023-01-17_at_5.png)

2. Locate the zip file in your finder and drag it to the desktop.

3. Go to the desktop and double click on the zip file. It should create a new folder called *"bss-macro-py-main"*

4. In terminal, enter these two commands one by one:

```bash
cd desktop/bss-macro-py-main
python3 e_macro.py
```




## Permissions

- In system preferences -> Security and privacy -> privacy 

Ensure that terminal has following permissions:

- Full Disk Access
- Screen Recording
- Accessibility
- Automation -> tick the "system events" checkbox under "terminal"
*Note: Terminal might not show up in automation until the macro is ran*

- Play roblox in fullscreen


## Exiting the macro
1. Tab out/close out of Roblox
2. Tap on terminal and press Ctrl + C

## Re-running the macro
Enter the following commands into terminal:

```bash
cd desktop/bss-macro-py-main
```

and
```bash
python3 e_macro.py
```
## Setting up the discord bot

1. Go to [discord applications](https://discord.com/developers/applications)

2. Click on “New Application” (top right)

3. Put in a name, tick the checkbox and create

4. Copy the application id (it is required later)

5. In the “settings” sidebar, click on bot -> add bot

6. Scroll down to “Privileged Gateway Intents” and check “Message Content Intent”

7. Edit and copy in the following link into a web browser:

8. https://discord.com/oauth2/authorize?client_id=<your application id from step 4>&permissions=68608&scope=bot

9. Add your bot to the server and ensure that it has permissions to view the channels you want to use it in

10. Returning back to the application page, click on reset token -> copy

11. Launch the macro and copy the token into the calibration section.

### Discord Bot commands

- Format: <prefix> <command>
- Prefix: !b
- Commands:
    1. rejoin
    2. screenshot

- *Example: !b rejoin*


## Bugs and Fixes

#### Cannon Not Detected

1. Go to cannon
2. Take a picture of the bottom right "E" button (Use Cmd + Shift + 4 for a cropped Screenshot)
EXAMPLE: 
![App Screenshot](https://cdn.discordapp.com/attachments/1065054819942932590/1065056204549791744/eb.png)

3. Rename the bottom right "eb.png"
4. Open the folder (Step 6 in installing-macro) . Find and Open the images folder.
5. Depending on your display, open up one of the folders that say "Built-in" or "Built-in retina display" (to check this, go to About Mac, and press display) 
6. Drag and replace the new photo into the built-in/retina display folder. 


**Note: on version 1.23 or later, theres a setting to adjust the sensitivity of the e button detection**

1. In calibration, select "cv2" as the e button detection type. 
2. You can adjust the threshold, a decimal from 0.0 to 1.0 
1.0 means exact match (100% of pixels must match), 0.5 means only 50% of pixels must match, and 0.0 means 0% of pixels must match.

(You can refer to the terminal when the macro is trying to find the canon. Look at the "trying to find eb.png" lines, where max_val is the pixel match%)

Using that, you can figure out a good threshold value to use

#### "Not authorised to send Apple events to System Events"

1. System Preferences -> Security and Privacy -> Privacy -> Automation (you may need to scroll down)

2. Select the checkbox next to the "System Events" for the terminal

#### Enable dictation menu is brought up during the macro

1. System preferences -> keyboard -> shortcuts -> app shortcuts

2. Click the '+' sign and put roblox as the application

3. Under Menu Title, input 'Start Dictation…' 

4. You can set the shortcut to whatever you want.

I set mine as *Option + Command + D*
![App Screenshot](https://i.imgur.com/x84eB89.png)

5. Add it


#### "mach-o file, but is an incompatible architecture (have 'arm64e', need 'x86_64')" 

For M1 Macs,

1. close terminal
2. Go to finder -> application -> terminal
3. Right click terminal -> get info
4. Check the checkbox Open using Rosetta
5. relaunch terminal 
6. Run the following commands:

``` bach 
pip3 uninstall opencv-python pillow numpy
pip3 install opencv-python pillow numpy
```



## Acknowledgements

- For the enable dictation fix: https://www.dofus.com/en/forum/1151-general-problems-solutions/339448-issue-with-macos-keyboard-keys

- Natro Macro for inspiration 

