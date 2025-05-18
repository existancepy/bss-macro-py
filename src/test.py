import pyautogui
import tkinter as tk
import threading
import time

class ClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        # Make the window always on top
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-topmost", 1)

        # UI Elements
        self.select_points_button = tk.Button(root, text="Select Points", command=self.select_points)
        self.select_points_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.start_button = tk.Button(root, text="Start Clicking", command=self.start_clicking, state=tk.DISABLED)
        self.start_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.stop_button = tk.Button(root, text="Stop Clicking", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.is_clicking = False
        self.thread = None
        self.pos1 = None
        self.pos2 = None

        # Coordinate labels
        self.first_pos_label = tk.Label(root, text="First Position: Not selected")
        self.first_pos_label.grid(row=3, column=0, padx=10, pady=10)

        self.second_pos_label = tk.Label(root, text="Second Position: Not selected")
        self.second_pos_label.grid(row=3, column=1, padx=10, pady=10)

        # Status label to display current action
        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.instructions_label = tk.Label(root, text="Click on two points to select positions.")
        self.instructions_label.grid(row=5, column=0, columnspan=2, pady=10)

        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', self.start_clicking_key)
        self.root.bind('<Control-q>', self.stop_clicking_key)

    def update_status(self, message):
        """ Updates the UI to show the current action. """
        self.status_label.config(text=f"Status: {message}")
        self.root.update_idletasks()

    def countdown(self, seconds, reason):
        """ Displays a countdown timer in the status label. """
        for i in range(seconds, 0, -1):
            if not self.is_clicking:
                return
            self.update_status(f"{reason}... {i} sec")
            time.sleep(1)

    def select_points(self):
        self.pos1 = None
        self.pos2 = None
        self.update_status("Selecting first position...")
        self.root.after(1000, self.wait_for_first_click)

    def wait_for_first_click(self):
        self.pos1 = pyautogui.position()
        self.first_pos_label.config(text=f"First Position: {self.pos1}")
        self.update_status("First position selected. Select second position.")
        self.root.after(1000, self.wait_for_second_click)

    def wait_for_second_click(self):
        self.pos2 = pyautogui.position()
        self.second_pos_label.config(text=f"Second Position: {self.pos2}")
        self.update_status("Both positions selected. Ready to start.")
        self.start_button.config(state=tk.NORMAL)

    def start_clicking(self):
        self.is_clicking = True
        self.thread = threading.Thread(target=self.click_forever)
        self.thread.daemon = True
        self.thread.start()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_clicking(self):
        self.is_clicking = False
        # if self.thread:
        #     self.thread.join()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Idle")

    def start_clicking_key(self, event=None):
        self.start_clicking()

    def stop_clicking_key(self, event=None):
        self.stop_clicking()

    def click_forever(self):
        last_second_position_time = time.time() - 60  # Ensures first second position click happens after 1 min
        pyautogui.press('shift')

        while self.is_clicking:
            if self.pos1:
                self.update_status("Clicking first position...")
                pyautogui.doubleClick(self.pos1)
                time.sleep(0.2)

                self.update_status("Moving right (D)...")
                pyautogui.keyDown('d')
                time.sleep(0.5)
                pyautogui.keyUp('d')

                self.update_status("Moving left (A)...")
                pyautogui.keyDown('a')
                time.sleep(1.0)
                pyautogui.keyUp('a')

                self.update_status("Jumping...")
                pyautogui.keyDown('space')
                time.sleep(0.11)
                pyautogui.keyUp('space')

                self.update_status("Tapping A...")
                pyautogui.press('a', presses=5)

                self.countdown(10, "Attacking")  # First wait (previously 9s, now 20s)

                self.update_status("Despawning and healing...")
                pyautogui.press('a', presses=8)

                self.countdown(9, "Healing")  # Second wait (previously 15s, now 9s)

                if self.pos2 and (time.time() - last_second_position_time >= 900):
                    self.update_status("Clicking second position...")
                    pyautogui.doubleClick(self.pos2)
                    last_second_position_time = time.time()

                time.sleep(0.5)

        self.update_status("Idle")

root = tk.Tk()
app = ClickerApp(root)
root.mainloop()