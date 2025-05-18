import cv2
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
import numpy as np
import imagehash

def templateMatch(smallImg, bigImg):
    res = cv2.matchTemplate(bigImg, smallImg, cv2.TM_CCOEFF_NORMED)
    return cv2.minMaxLoc(res)

# def templateMatch(smallImg, bigImg, scale=0.5):
#     small_resized = cv2.resize(smallImg, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
#     big_resized = cv2.resize(bigImg, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
#     res = cv2.matchTemplate(big_resized, small_resized, cv2.TM_CCOEFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#     # scale back to original coordinates
#     return min_val, max_val, (int(min_loc[0] / scale), int(min_loc[1] / scale)), (int(max_loc[0] / scale), int(max_loc[1] / scale))

def locateImageOnScreen(target, x,y,w,h, threshold = 0):
    screen = mssScreenshot(x,y,w,h)
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    _, max_val, _, max_loc = templateMatch(target, screen)
    if max_val < threshold: return None
    return (max_val, max_loc)

#used for locating templates with transparency
#this is done by template matching with the gray color space

def locateTransparentImage(target, screen, threshold):
    screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)
    target = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)
    _, max_val, _, max_loc = templateMatch(target, screen)
    if max_val < threshold: return None
    return (max_val, max_loc)
    
def locateTransparentImageOnScreen(target, x,y,w,h, threshold = 0):
    screen = mssScreenshotNP(x,y,w,h)
    return locateTransparentImage(target, screen, threshold)


def similarHashes(hash1, hash2, threshold):
    return hash1-hash2 < threshold

def locateImageWithMaskOnScreen(image, mask, x,y,w,h, threshold=0):
    screen = mssScreenshotNP(x,y,w,h)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

    # do masked template matching and save correlation image
    res = cv2.matchTemplate(screen, image, cv2.TM_CCORR_NORMED, mask=mask)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val < threshold: return None
    return (max_val, max_loc)

def findColorObjectHSL(img, hslRange, kernel=None, mode="point", best=1, draw=False):
    """
    Quickly find objects of a specific color in the HSL range.

    Args:
        img (numpy.ndarray): Input image in BGR format.
        hslRange (list): HSL range [(H_min, S_min, L_min), (H_max, S_max, L_max)].
        kernel (numpy.ndarray): Kernel for erosion (optional).
        mode (str): "point" to return center of bounding box, "box" to return bounding boxes.
        best (int): Number of top contours to return (default 1).
        draw (bool): Whether to draw bounding boxes on the image.

    Returns:
        tuple or list: Coordinates of the center or bounding boxes.
    """
    # Convert HSL range to OpenCV's HLS format
    hLow, sLow, lLow = hslRange[0][0] / 2, hslRange[0][1] / 100 * 255, hslRange[0][2] / 100 * 255
    hHigh, sHigh, lHigh = hslRange[1][0] / 2, hslRange[1][1] / 100 * 255, hslRange[1][2] / 100 * 255

    # Fast conversion to HLS and thresholding
    binary_mask = cv2.inRange(
        cv2.cvtColor(img, cv2.COLOR_BGR2HLS),
        np.array([hLow, lLow, sLow], dtype=np.uint8),
        np.array([hHigh, lHigh, sHigh], dtype=np.uint8)
    )

    if kernel is not None:
        binary_mask = cv2.erode(binary_mask, kernel, iterations=1)

    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None
    
    if best > 1:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:best]

    results = []
    for contour in (contours if best > 1 else [max(contours, key=cv2.contourArea)]):
        x, y, w, h = cv2.boundingRect(contour)
        results.append((x + w // 2, y + h // 2) if mode == "point" else (x, y, w, h))
        if draw:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if draw:
        cv2.imshow("Result", img)
        cv2.waitKey(0)

    return results if best > 1 else results[0]

def findColorObjectRGB(img, rgbTarget, variance=0, kernel=None, mode="point", best=1, draw=False):
    """
    Quickly find objects of a specific color in the RGB range with variance.

    Args:
        img (numpy.ndarray): Input image in BGR format.
        rgbTarget (tuple): Target RGB color (R, G, B), values 0-255.
        variance (int): Allowed variation (0-255) for each color component.
        kernel (numpy.ndarray): Kernel for erosion (optional).
        mode (str): "point" to return center of bounding box, "box" to return bounding boxes.
        best (int): Number of top contours to return (default 1).
        draw (bool): Whether to draw bounding boxes on the image.

    Returns:
        tuple or list: Coordinates of the center or bounding boxes.
    """
    
    # Convert image from BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Compute lower and upper bounds
    lower_bound = np.clip(np.array(rgbTarget) - variance, 0, 255).astype(np.uint8)
    upper_bound = np.clip(np.array(rgbTarget) + variance, 0, 255).astype(np.uint8)
    
    # Thresholding to create a binary mask
    binary_mask = cv2.inRange(imgRGB, lower_bound, upper_bound)
    
    if kernel is not None:
        binary_mask = cv2.erode(binary_mask, kernel, iterations=1)
    
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    if best > 1:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:best]
    
    results = []
    for contour in (contours if best > 1 else [max(contours, key=cv2.contourArea)]):
        x, y, w, h = cv2.boundingRect(contour)
        results.append((x + w // 2, y + h // 2) if mode == "point" else (x, y, w, h))
        if draw:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    if draw:
        cv2.imshow("Result", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return results if best > 1 else results[0]


def fastFeatureMatching(haystack, needle):

    # Load images (downscale for speed if needed)
    img1 = needle
    img2 = haystack

    # Downscale images to speed up processing (adjust scale factor as needed)

    # Use ORB for keypoint detection and descriptor extraction
    orb = cv2.ORB_create(nfeatures=500, scoreType=cv2.ORB_FAST_SCORE)  

    # Detect keypoints and compute descriptors
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Use FLANN-based matcher for faster approximate matching
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
    search_params = dict(checks=80) 
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Perform knnMatch
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for x in matches:
        if len(x) != 2: continue
        m, n = x
        if m.distance < 0.7 * n.distance:
            good.append(m)

    # If there are enough good matches, find the object's location
    if len(good) < 5:
        return None
    
    # Extract location of good matches
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # Find homography
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)


    if M is None:
        return None
    #homography is found
    h, w = img1.shape
    pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    # Calculate and display center of the bounding box
    center_x = int(np.mean(dst[:, 0, 0]))
    center_y = int(np.mean(dst[:, 0, 1]))
    return (center_x, center_y)