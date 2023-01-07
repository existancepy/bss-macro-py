**Bee swarm python macro installation and instructions**

Made and tested on mac, currently untested for windows/linux
*Due to  the code, it is unlikely to work on windows/linux thanks to the retina display.*
I can release a window-compatible one, but ~im lazy~

**Set your display resolution to default and colour profile to colour LCD. For roblox, play in fullscreen and set the graphics quality to 1**

**Installation**


0. Install python v3.9.5: https://www.python.org/downloads/release/python-395/
**Check "Add python to path"  in the installation window**

1. Create a folder anywhere (it will be where the macro files are stored)


2.Open terminal/command line
   Optional: Create a python venv
   

3.Run the following command:
   *pip install pyautogui pillow opencv-python python-imagesearch discord-webhook*


**Setup**

4. Download the files in the git repo into the folder made in step 1.
5. Go to settings.txt and edit the settings there. A more in-depth explaination of what each setting does is to come soon
6. Go to save.txt and edit the resolution. You can find it by clicking on the apple icon on the top bar menu -> about this mac -> displays
 *if you cant find save.txt, that means that I have updated the code. You can adjust the resolution at settings.txt*
 
 **Launching the program**

7. Navigate to the folder created in step 1 using the "cd" command:

   *eg cd desktop/bee_swarm_macro*

8. run the program with the following command:

   *python e_macro.py*

*During the runtime, you may be prompted to enable certain permissions in your system and security settings. Do enable those.*

Credits:

Natro macro for some of the image assets and techniques

**Exiting the macro:**
Tab out of roblox and press ctrl z to quit (not cmd z)

**Settings explaination:**

- Hive number: Its a number from 1-6 that represents which hive you claimed. 1 is the hive closest to the canon, 6 is the furthest.
- walkspeed: The player walkspeed (without haste). It can be found in the in-game settings.
- gifted_vicious_bee: (yes/no). It uses gifted vicious bee's mob respawn time reduction in the calculations
- enable_discord_webhook: Uses discord webhook to send status updates. (yes/no). Check out [discord webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) to setup a discord webhook
- discord_webhook_url: discord webhook url
- gather_enable: if you want to enable gathering. The program will not gather if its set to "no" (yes/no).
- gather_field: The field you want to gather from.
- gather_pattern: The movement pattern that you want to gather with.
- gather_size: Affects the overall area that is covered by the player when gathering (S,M,L).
- gather_width: Affects the overall area that is covered by the player when gathering.
- gather_time: How long you want to gather for (in minutes).
- pack: How full you want your backpack to be (in percentage).
- before_gather_turn: which direction you want to turn upon reaching the field and before gathering.
- turn_times: how many times you want to turn in the direction specified by before_gather_turn.
- return_to_hive: how you want to return to hive (reset/walk/whirligig).
- whirligig_slot: the hotbar slot your whirligig is in. This is only used if you set the return_to_hive to "whirligig".
- stump_snail: if you want to enable killing stump snail afk. The program will prioritise killing stump snail before doing anything else (yes/no). **Make sure that stump snail is alive when selecting this**

**Bugs and fixes:**


1. The player keeps rotating at the hive before walking
   - The code is not able to detect the hive. To fix this, take a screenshot of the hive area under your hotbar. Reset your character, then press "." 4        times, pgup (fn+ up arrow) until you cant go up anymore. Than press "o" until you stop zooming out. 
   - Disable your shift lock switch and using cmd+shift+4, take a screenshot of the area under your hotbar. 
   - Here is an example: https://imgur.com/a/pvWYaWP You can take the screenshot anywhere in the red box. Try to keep the screenshot small                    https://imgur.com/a/FlcxKVl
   - Replace hive1.png in the images folder with your new image

2. The dock is brought up during the macro, interrupting the key inputs.
   - This can be solved by manually clicking on the screen when the macro is ran



