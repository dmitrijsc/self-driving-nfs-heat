import numpy as np
import cv2
import math, time

import framegrabber, getkeys, keys

keyboard = keys.Keys()

def preview_img(screen):

    w = "nfs-minimap"
    cv2.namedWindow(w)
    cv2.moveWindow(w, 4000, 800)
    cv2.imshow(w, screen)
    cv2.waitKey(1)

def process_minimap(screen):

    half_image = int(screen.shape[0] / 2)
    distance = 30

    yellowLowerBoundary = np.array([20, 100, 100])
    yellowUpperBoundary = np.array([40, 255, 255])

    mask = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(mask, yellowLowerBoundary, yellowUpperBoundary)
    mask = cv2.dilate(mask, np.ones((2,2), np.uint8))
    mask = cv2.erode(mask, np.ones((5,5), np.uint8))

    limit_mask = np.zeros_like(mask)
    lm_point = np.array([
        [half_image - distance, half_image - distance],
        [half_image - int(distance/3), half_image],
        [half_image + int(distance/3), half_image],
        [half_image + distance, half_image - distance]
    ])
    cv2.fillPoly(limit_mask, [lm_point], 255)
    mask = cv2.bitwise_and(limit_mask, mask)

    matches = np.argwhere(mask == 255)

    if np.sum(matches) > 0:

        keyboard.directKey('a', keyboard.key_release)
        keyboard.directKey('d', keyboard.key_release)

        target_value_x = round(np.mean(matches[:, 1]), 0)
        target_value_y = round(np.mean(matches[:, 0]), 0)

        x = target_value_x - half_image
        y = abs(half_image - target_value_y)
        h = round(math.sqrt(x*x + y*y) / abs(y) * distance, 2)

        direction = x < 0
        pace = round(h - math.sqrt(distance*distance), 2)

        print(x, y, h, direction, pace)

        if direction and (pace > 0.25):
            print("Left")
            keyboard.directKey('a')
        elif ~direction and (pace > 0.25):
            print("Right")
            keyboard.directKey('d')

    preview_img(mask)

def main():
    
    fg = framegrabber.FrameGrabber(0, 0, 2560, 1440, "Need for Speed™ Heat")

    for x in range(20000):

        screen = fg.grab()
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

        minimap = screen[927:1271, 170:514]

        process_minimap(minimap)
        # preview_img(minimap)

main()
