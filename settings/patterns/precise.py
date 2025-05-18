import mss
import numpy as np
import pyautogui
from pynput.mouse import Controller

def find_color_centroid(image_rgb, color_range_min, color_range_max, min_pixels_threshold=50):
    """
    Finds the centroid of pixels within a specified color range if enough pixels are found.

    Args:
        image_rgb (np.array): Image data as a NumPy array (RGB format).
        color_range_min (tuple): Minimum RGB values (R, G, B).
        color_range_max (tuple): Maximum RGB values (R, G, B).
        min_pixels_threshold (int): The minimum number of pixels required to calculate a centroid.

    Returns:
        tuple: (x, y) coordinates of the centroid if found and threshold met, otherwise None.
    """
    min_r, min_g, min_b = color_range_min
    max_r, max_g, max_b = color_range_max

    # Create boolean masks for each channel checking if pixels are within range
    r_mask = (image_rgb[:, :, 0] >= min_r) & (image_rgb[:, :, 0] <= max_r)
    g_mask = (image_rgb[:, :, 1] >= min_g) & (image_rgb[:, :, 1] <= max_g)
    b_mask = (image_rgb[:, :, 2] >= min_b) & (image_rgb[:, :, 2] <= max_b)

    # Combine masks to find pixels where all conditions are true
    combined_mask = r_mask & g_mask & b_mask

    # Find the indices (coordinates) of matching pixels
    # np.argwhere returns [[y1, x1], [y2, x2], ...]
    matching_pixels = np.argwhere(combined_mask)

    num_matching_pixels = matching_pixels.shape[0] # More direct way to get count

    if num_matching_pixels >= min_pixels_threshold:
        # Calculate the centroid (average position) of the matching pixels
        # matching_pixels[:, 0] contains y coordinates
        # matching_pixels[:, 1] contains x coordinates
        mean_y = np.mean(matching_pixels[:, 0])
        mean_x = np.mean(matching_pixels[:, 1])

        print(f"Found {num_matching_pixels} pixels. Centroid at (x={mean_x:.1f}, y={mean_y:.1f})")
        # Return centroid as (x, y) tuple of integers
        return (int(mean_x), int(mean_y))
    else:
        # Not enough pixels found
        if num_matching_pixels > 0:
            print(f"Found {num_matching_pixels} pixels, but less than threshold {min_pixels_threshold}.")
        return None

# --- Main Loop ---
mouse = Controller()
sct = mss.mss()

# Define the monitor area to capture.
# monitor[0] is the entire virtual screen.
# monitor[1] is typically the primary monitor. Adjust if needed.
try:
    monitor = sct.monitors[1]
    print(f"Monitoring screen: {monitor}")
except IndexError:
    print("Could not find primary monitor (index 1). Using entire screen (index 0).")
    monitor = sct.monitors[0]

# Define the color range to search for
# Example: A specific shade of purple
color_range_min = (195, 97, 250)
color_range_max = (205, 102, 255)
sat_color_min = (12, 207, 247)
sat_color_max = (24, 221, 255)
targ_color_min = (250, 200, 105)
targ_color_max = (255, 210, 110)
# Define the minimum number of pixels of the target color needed to trigger mouse movement
MIN_target_THRESHOLD = 700 # Adjust this value as needed
MIN_sat_THRESHOLD = 10

for _ in range(8):
    self.keyboard.press(rotup)
    
# 1. Take screenshot using mss for the specified monitor
sct_img = sct.grab(monitor)

# 2. Convert screenshot to NumPy array
# mss grabs images in BGRA format (Blue, Green, Red, Alpha)
img_bgra = np.array(sct_img)

# 3. Convert BGRA to RGB for color comparison
# Slicing removes the alpha channel, ::-1 reverses the BGR to RGB order
img_rgb = img_bgra[:, :, :3][:, :, ::-1]

# 4. Look for a cluster of pixels within the defined color range
centroid_location = find_color_centroid(img_rgb, color_range_min, color_range_max, MIN_target_THRESHOLD)
saturator_location = find_color_centroid(img_rgb, sat_color_min, sat_color_max, MIN_sat_THRESHOLD)
targ_location = find_color_centroid(img_rgb, targ_color_min, targ_color_max, MIN_target_THRESHOLD)
# 5. If a centroid is found (enough pixels detected), move the mouse cursor to its location
if centroid_location:
    # Coordinates from find_color_centroid are relative to the captured monitor area.
    # Calculate absolute screen coordinates for mouse movement.
    abs_x = monitor["left"] + centroid_location[0]
    abs_y = monitor["top"] + centroid_location[1]

    print(f"Sufficient pixels found. Moving mouse to centroid absolute: ({abs_x}, {abs_y})")
    mouse.position = ((abs_x)/2, (abs_y)/2)
    pyautogui.rightClick()
elif targ_location:
    # Coordinates from find_color_centroid are relative to the captured monitor area.
    # Calculate absolute screen coordinates for mouse movement.
    abs_x = monitor["left"] + targ_location[0]
    abs_y = monitor["top"] + targ_location[1]

    print(f"Sufficient pixels found. Moving mouse to targ absolute: ({abs_x}, {abs_y})")
    mouse.position = ((abs_x)/2, (abs_y)/2)
    pyautogui.rightClick()
elif saturator_location:
    abs_x = monitor["left"] + saturator_location[0]
    abs_y = monitor["top"] + saturator_location[1]
    mouse.position = ((abs_x)/2, (abs_y)/2)
    pyautogui.rightClick()
    print(f"Sufficient pixels found. Moving mouse to saturator absolute: ({abs_x}, {abs_y})")
else:
    # Log message if not enough pixels are found in the current frame
    print("Target color cluster not found or below threshold in this frame.") # Use debug to avoid flooding logs
