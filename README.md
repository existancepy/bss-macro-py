**Bee swarm python macro installation and instructions**

Made and tested on mac, currently untested for windows/linux
*Due to  the code, it is unlikely to work on windows/linux thanks to the retina display.*
I can release a window-compatible one, but ~im lazy~

**Installation**

Install python v3.9.5: https://www.python.org/downloads/release/python-395/
**Check "Add python to path"  in the installation window**

1. Create a folder anywhere (it will be where the macro files are stored)


2.Open terminal/command line
Optional: Create a python venv

3.Run the following command:

  *pip install pyautogui pillow opencv-python*

**Setup**

4. Download the files in the git repo into the folder made in step 1.
5. Go to settings.txt and edit the settings there. A more in-depth explaination of what each setting does is to come soon
6. Go to save.txt and edit the resolution. You can find it by clicking on the apple icon on the top bar menu -> about this mac -> displays
 *if you cant find save.txt, that means that I have updated the code. You can adjust the resolution at settings.txt
 
 **Launching the program**

7. Navigate to the folder created in step 1 using the "cd" command:

  *eg cd desktop/bee_swarm_macro*

8. run the program with the following command:

  *python e_macro.py*

*During the runtime, you may be prompted to enable certain permissions in your system and security settings. Do enable those.*
