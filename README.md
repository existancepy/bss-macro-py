
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


