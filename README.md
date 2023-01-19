**Bee swarm python macro installation and instructions**

Made and tested on mac, currently untested for windows/linux
*Due to  the code, it is unlikely to work on windows/linux thanks to the retina display.*
I can release a window-compatible one, but ~im lazy~

**Set your display resolution to default and colour profile to colour LCD. For roblox, play in fullscreen and set the graphics quality to 1**

There's a discord server now! Thanks to kay ;)#6148 for setting it up

https://discord.gg/PwUMDp8c

Better instructions and fixes


**Installation**


0. Install python v3.9.5: https://www.python.org/downloads/release/python-395/
**Check "Add python to path"  in the installation window**

1. Create a folder anywhere (it will be where the macro files are stored)

**For M1 Macs**
- close terminal
- Go to finder -> application -> terminal
- Right click terminal  -> get info 
- Check the checkbox Open using Rosetta
- relaunch terminal

2.Open terminal/command line
   (Optional: Create a python venv)
   

3.Run the following command:
   *pip3 install pyautogui pillow opencv-python python-imagesearch discord-webhook keyboard discord.py*

   *Or python3 -m pip install pyautogui pillow opencv-python python-imagesearch discord-webhook keyboard discord.py*

**Setup**

4. Download the files in the git repo into the folder made in step 1.
 
 **Launching the program**

5. Navigate to the folder created in step 1 using the "cd" command:

   *eg cd desktop/bee_swarm_macro*

6. run the program with the following command:

   *python3 e_macro.py*


*During the runtime, you may be prompted to enable certain permissions in your system and security settings. Do enable those.*

**Calibration**

 - System settings permissions: 
   Currently, it seems like you have to give terminal permissions under the accessibility and screen recording sections. Do let me know if there is any  permissions I missed

- Check out 1. and 4. of the "bugs and fixes section" below. I highly recommend doing the fixes even if you may not seem to encounter the problem.
  *So far, everyone who has messaged  me has encountered hive issues (whether they realised it or not), so I recommend re-configuring the hive as stated    in 1.*



Credits:

Natro macro for some of the techniques

**Exiting the macro:**
Ensure the terminal window is focused and press ctrl c to quit (not cmd c)

**Setting up a discord bot**

1. Go to https://discord.com/developers/applications
2. Click on “New Application” (top right)
3. Put in the name, tick the checkbox and create
4. Copy the application id (it is required later)
5. In the “settings” sidebar, click on bot -> add bot 
6. Scroll down to “Privileged Gateway Intents” and check “Message Content Intent”
7. Edit and copy  in the following link into a web browser:
8. https://discord.com/oauth2/authorize?client_id=<your application id from step 4>&permissions=68608&scope=bot
9. Add your bot to the server and ensure that it has permissions to view the channels you want to use it in
10. Returning back to the application page, click on reset token -> copy
11. Launch the macro and copy the token into the calibration section.

Discord bot commands:

Format: <prefix> <command>
Prefix: !b
Commands: rejoin (forces the character to rejoin the game), 
                    screenshot (sends a screenshot of the screen)
*Example: !b rejoin*


**Bugs and fixes:**


1. The player keeps rotating at the hive before walking
   - The code is not able to detect the hive. To fix this, take a screenshot of the hive area under your hotbar. Reset your character, then press "." 4        times, then press pgup (fn+ up arrow) until you cant go up anymore. Than press "o" until you stop zooming out. 
   - Disable your shift lock switch and using cmd+shift+4, take a screenshot of the area under your hotbar. 
   - Here is an example: https://imgur.com/a/pvWYaWP You can take the screenshot anywhere in the red box. Try to keep the screenshot small                    https://imgur.com/a/FlcxKVl
   - Replace hive1.png in the images folder with your new image
   - Ensure that you have give terminal permissions to screen recording

2. The dock is brought up during the macro, interrupting the key inputs.
   - This can be solved by manually clicking on the screen when the macro is ran
3. *ImportError:dlopen...Symbol not found/import cv2* in the terminal when the code is ran.
   - This is most likely caused by an outdated macOS version. For a work around, check out https://github.com/existancepy/bss-macro-py-no-cv2
   - A better fix would just be to update your mac OS software
4. Enable dictionary menu is brought up during the macro
   - Fix:  system preferences -> keyboard -> shortcuts -> app shortcuts
   - click the '+' sign and put roblox as the application
   - Under Menu Title, input 'Start Dictation…'  without the single quotes of course. The three periods are actually an ellipsis, which is one character which you can type by pressing option and the [ ; ] key, or just copy and paste what I typed above. 
   - I set the shortcut to Option + Command + E for that one.
   - Add it
   - Reference image: https://imgur.com/a/hzbsM5e
   - Credit: https://www.dofus.com/en/forum/1151-general-problems-solutions/339448-issue-with-macos-keyboard-keys

