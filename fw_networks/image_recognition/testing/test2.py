import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyautogui


drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

img = cv.imread('screen_cropped.png')
img2 = img.copy()
initial_postion = ''
running = True
region = []


# mouse callback function
def draw_shape(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv.rectangle(img,(ix,iy),(x,y),(255,255,255),-1)
                cv.addWeighted(img, 0.1 , img2, 1 - 0.1, 0, img2)
            else:
                cv.circle(img,(x,y),5,(0,0,255),1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv.rectangle(img,(ix,iy),(x,y),(255,255,255),-1)
            cv.addWeighted(img, 0.05 , img2, 1 - 0.05, 0, img2)
        else:
            cv.circle(img,(x,y),5,(0,0,255),1)

# Create a black image, a window and bind the function to window
cv.namedWindow('image')
cv.setMouseCallback('image',draw_shape)

while running:
    cv.imshow('image',img2)
    cv.waitKey(0)
    cv.destroyAllWindows()
    break
 

pyautogui.screenshot('region.png', region=region[0])
