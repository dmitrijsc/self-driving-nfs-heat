import numpy as np
import cv2
import math, time

import framegrabber, getkeys, keys

keyboard = keys.Keys()

def preview_img(screen, firstTime):

    w = "nfs-minimap"

    if firstTime:
        cv2.namedWindow(w)
        cv2.moveWindow(w, 4000, 800)

    cv2.imshow(w, screen)
    cv2.waitKey(100)

def process_minimap(screen):

    half_image = int(screen.shape[0] / 2)
    distance = 30

    yellowLower = np.array([80, 150, 150])
    yellowUpper = np.array([100, 255, 255])

    mask = cv2.cvtColor(screen, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(mask, yellowLower, yellowUpper)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
    mask = cv2.erode(mask, np.ones((5, 5), np.uint8))

    limit_mask = np.zeros_like(mask)
    lm_points = np.array([
        [half_image-30 * 2, half_image - distance],
        [half_image-10*2, half_image], 
        [half_image+10*2, half_image], 
        [half_image + 30*2, half_image - distance]
    ])
    cv2.fillPoly(limit_mask, [lm_points], 255)
    mask = cv2.bitwise_and(limit_mask, mask)

    matches = np.argwhere(mask == 255)

    if np.sum(matches) != 0:

        keyboard.directKey("d", keyboard.key_release)
        keyboard.directKey("a", keyboard.key_release)

        target_values = matches[(matches[:, 0] < half_image) == (matches[:, 0] > half_image - distance)]

        if np.sum(target_values) == 0:
            return

        # target_value_y = round(np.mean(target_values[1:10][:, 0]), 0)
        #target_value_x = round(np.mean(target_values[1:10][:, 1]), 0)

        target_value_y = round(np.mean(target_values[:, 0]), 0)
        target_value_x = round(np.mean(target_values[:, 1]), 0)

        x = target_value_x - half_image
        y = target_value_y - (half_image - distance)
        h = round(math.sqrt(x*x + y*y) / abs(y) * distance, 2)

        direction = x < 0
        pace = round(h - math.sqrt(distance*distance))

        print(x, y, h, direction, pace)

        if direction and (pace > 0):
            print("left")
            keyboard.directKey("a")
        elif ~direction and (pace > 0):
            print("right")
            keyboard.directKey("d")

    preview_img(mask, False)

def main():

    for x in range(5):
        print(x)
        time.sleep(1)

    fg = framegrabber.FrameGrabber(0, 0, 2560, 1440, "Need for Speed™ Heat")

    for x in range(1000):

        if 'Z' in getkeys.key_check():
            keyboard.directKey("w", keyboard.key_release)
            keyboard.directKey("s", keyboard.key_release)
            keyboard.directKey("d", keyboard.key_release)
            keyboard.directKey("a", keyboard.key_release)
            return

        screen = fg.grab()
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        
        minimap = screen[927:1271, 170:514]

        process_minimap(minimap)
        # preview_img(minimap, x == 0)

main()
