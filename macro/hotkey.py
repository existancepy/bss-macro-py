from pynput import keyboard
import subprocess
import _thread

def on_press(key):
    if hasattr(key, "char") and key.char == ('z'):
        _thread.interrupt_main()
        return False

try:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:
        while True:
            pass
except KeyboardInterrupt:
    print("lol")


