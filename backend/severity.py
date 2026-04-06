import cv2
import numpy as np

def detect_severity(image_path):

    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # detect brown/yellow infected spots
    lower = np.array([10,50,50])
    upper = np.array([35,255,255])

    mask = cv2.inRange(hsv, lower, upper)

    infected_pixels = np.sum(mask > 0)
    total_pixels = image.shape[0] * image.shape[1]

    percentage = (infected_pixels / total_pixels) * 100

    if percentage < 20:
        severity = "Mild"
    elif percentage < 50:
        severity = "Moderate"
    else:
        severity = "Severe"

    return severity, percentage