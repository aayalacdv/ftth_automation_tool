import time
from turtle import position
from position_manager import get_house_positions, get_real_positions, get_region_position
from screenshot_manager import get_region
import pyautogui

if __name__=="__main__": 
    get_region()
    time.sleep(0.25)
    region_position = get_region_position()
    house_positions = get_house_positions()

    real_positons = get_real_positions(region_position, house_positions)

    for pos in real_positons: 
        pyautogui.click(pos)
        time.sleep(0.25)
        

