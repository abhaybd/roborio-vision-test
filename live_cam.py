import cv2
import threading
import yolo
import numpy as np


cam = cv2.VideoCapture(0)

running = True

def close_feed():
    input('Press enter to stop feed.')
    global running
    running = False
    cam.release()
    cv2.destroyAllWindows()

thread = threading.Thread(target = close_feed, args = ())
thread.daemon = True
thread.start()

def bgr_to_rgb(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

def rgb_to_bgr(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

cv2.namedWindow('Image')

print('Starting live feed.')
while running:
    r, img = cam.read()
    if r:
        rgb = bgr_to_rgb(img)
        drawn_img = np.asarray(yolo.draw_pred(rgb))
        bgr = rgb_to_bgr(drawn_img)
        cv2.imshow('Image', bgr)
        cv2.waitKey(1)