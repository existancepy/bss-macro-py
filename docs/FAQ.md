# FAQ
This page contains frequently asked questions pertaining to the macro

### 1. Are there any in-game requirements to using this macro?
Yes. Since the macro primarily uses the red cannon for moving around, you'll need to have the red cannon unlocked with the hang glider equipped

### 2. How do I macro while my macbook's lid closed?
You can disable mac's auto sleep feature with this command
*(Note: you'll need to enter your password, which won't be displayed)*
```console
sudo pmset disablesleep 1
```
You can re-enable sleep with this command:
```console
sudo pmset disablesleep 0
```

### 3. Does the macro damage my mac?

Not directly. However, your mac's battery and performance may suffer over time
- Battery:
  Since running the macro for long periods of time requires your mac to be plugged in, this can lead to overcharging which decreases the battery's lifespan. This degradation can be slwoed down by enabling optimized battery charging in the mac's system settings.
- Performance:
  Like all electronics, your mac will slow down over time due to wear and tear, and this process is accelerated when running the macro for long periods.

### 4. How do I add patterns to the macro?
 - You can add the pattern file to the settings -> patterns<br>
*The pattern file can either be a python file (.py) or an autohotkey file (.ahk)*
- After adding the file in, restart the macro

### 5. Can I use natro patterns with this macro?
Yes, the macro is able to convert natro ahk patterns into python ones. Refer to #4 to see how to import a pattern

### 6. Are natro settings the same as this macro's?
Yes, this macro was designed to match natro's gather settings

