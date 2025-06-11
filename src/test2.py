from modules.screen.imageSearch import templateMatch
import cv2
import mss
import numpy as np

# screen = cv2.imread("screen3.png", 0)
# image = cv2.imread("images/menu/cannon-retina.png", 0)

# # Define the scales to test
# scales = [1]

# # Try matching at each scale
# for scale in scales:
#     resized = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
#     result = templateMatch(resized, screen)
#     print(f"Scale {scale}: {result}")

def screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Full primary screen
        sct_img = sct.grab(monitor)
        return np.array(sct_img)[:, :, 0]  # Convert to grayscale

def generate_scales(start=0.40, stop=1.20, step=0.01):
    scales = []
    while start <= stop:
        scales.append(round(start, 3))
        start += step
    return scales

def auto_detect_scaling(template_path="images/menu/ebutton-retina.png"):
    import cv2
    import time
    import cv2
    import pyautogui
    import mss
    import numpy as np

    # Step 1: Show the image using default image viewer
    import subprocess, platform
    if platform.system() == "Darwin":
        subprocess.Popen(["open", template_path])
    elif platform.system() == "Windows":
        subprocess.Popen(["start", template_path], shell=True)
    else:
        subprocess.Popen(["xdg-open", template_path])

    # Step 2: Wait for window to open
    time.sleep(1)

    # Step 3: Screenshot
    screen = screenshot()  # From earlier mss-based function
    template = cv2.imread(template_path, 0)

    # Step 4: Match
    #could be done with gradient descent, but thats just overkill
    best_scale = 1
    score = 0
    st = time.time()
    for scale in generate_scales(0.4, 1.2, 0.01):
        print(f"{scale}/{1.20}")
        resized = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        _, max_val, _, max_loc = templateMatch(resized, screen)
        if max_val > score:
            best_scale = scale
            score = max_val

    print(f"[INFO] Best scale detected: {best_scale}, Match confidence: {score}")
    return scale

auto_detect_scaling()