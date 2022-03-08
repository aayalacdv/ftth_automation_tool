import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def get_region_position(): 

    img_rgb = cv.imread('./image_recognition/screen.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('./image_recognition/region/region.png',0)

    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    return max_loc


def get_house_positions(): 
    
    img_rgb = cv.imread('./image_recognition/region/region.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('./image_recognition/template/template.PNG',0)
    
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    
    threshold = 0.42
    xloc, yloc = np.where( res >= threshold)
    
    rectangles = []
    for (x,y) in zip(yloc, xloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        
    
    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.2)
    positions = []
    
    for (x, y, w, h) in rectangles: 
        cv.rectangle(img_rgb, (x, y), (x + w, y + h), (0,0,255), 2)
        positions.append((x,y))

    cv.imwrite('./image_recognition/res.png',img_rgb) 
    return positions


def get_real_positions(region_position, house_positions): 
    
    real_postions = []
    max_x, maxY = region_position 

    for (x,y) in house_positions: 
        real_postions.append((x + max_x, y + maxY))

    return real_postions


