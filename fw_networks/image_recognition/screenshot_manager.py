import time
import pyautogui 
import cv2 as cv 

drawing = False 

def get_region(): 

    #take the screenshot and open it with the mause callback 
    screenshot = pyautogui.screenshot() 
    screenshot.save('./image_recognition/screen.png')

    ix,iy = -1,-1

    #get the screenshot
    img = cv.imread('./image_recognition/screen.png')

    #variable to store the points of the region 
    region = []

    running = True

    # mouse callback function
    def draw_shape(event,x,y,flags,param):
        global ix,iy,drawing
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            ix,iy = x,y
        elif event == cv.EVENT_MOUSEMOVE:
            if drawing == True:
                cv.rectangle(img, (ix,iy) ,(x,y) ,(0,255,255),-1)

        elif event == cv.EVENT_LBUTTONUP:
            drawing = False
            region.append((ix, iy,  x - ix, y - iy))
            cv.rectangle(img,(ix,iy),(x,y),(0,255,255),-1)
            cv.destroyAllWindows()
            time.sleep(3)
            running = False

    #bind the mouse callback to the window
    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_shape)

    #get the screen region 
    while running:
        cv.imshow('image',img)
        if cv.waitKey(10) == 27:
            break
        if len(region) != 0: 
            running = False

    
    cv.destroyAllWindows()
    #take the screenshot of the region 
    pyautogui.screenshot('./image_recognition/region/region.png', region=region[0])

