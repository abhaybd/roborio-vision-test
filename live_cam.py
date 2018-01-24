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

def reverse_bytes(img):
    return img[:,:,::-1]

cv2.namedWindow('Image')

print('Starting live feed.')
while running:
    r, img = cam.read()
    if r:
        rgb = reverse_bytes(img)
        drawn_img = np.asarray(yolo.draw_pred(rgb))
        bgr = reverse_bytes(drawn_img)
        cv2.imshow('Image', bgr)
        cv2.waitKey(1)