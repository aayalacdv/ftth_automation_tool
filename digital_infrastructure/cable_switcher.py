from encodings import search_function
from pydoc import Helper
from cable_manager import CableManager
from constants import CableCodes, JointBoxCodes, SbCodes, Towns 
from component_creator import ComponentCreator
from remote_connection import RemoteConnection
from helpers import Helpers 
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


if __name__ == '__main__': 

    WORKING_TOWN = Towns.CARLTON
    WORKING_CLUSTER = 8

    ORIGIN_ID_XPATH = '//*[@id="frmcable"]/form/article/div[2]/app-location/apx-field1[2]/div/div/div[1]/app-find-closest-element/select'
    DEST_ID_XPATH = '//*[@id="frmcable"]/form/article/div[2]/app-location/apx-field1[2]/div/div/div[2]/app-find-closest-element/select'

    driver = RemoteConnection.setup_connection()

    def get_cable_id(origin, destination):

        return f'CHT-CL008-{origin}-{destination}'
        

    def change_cable_label():   
        id_field = driver.find_element(by=By.CSS_SELECTOR, value="apx-field1[label='Id'] input")
        old_id = id_field.get_attribute('value')
        id_field.clear() 

        select_origin = Select(driver.find_element(by=By.XPATH, value=ORIGIN_ID_XPATH))
        select_dest = Select(driver.find_element(by=By.XPATH, value = DEST_ID_XPATH))

        origin = ''
        destination = ''


        for i in range(1,len(select_origin.options)): 
            selection = select_origin.options[i].text.split(':')
            if len(selection) == 1: 
                select_origin.select_by_index(i)
                origin = select_origin.options[i].text.split(' ')[0] 
                break

        for i in range(1,len(select_dest.options)): 
            selection = select_dest.options[i].text.split(':')
            if len(selection) == 1: 
                select_dest.select_by_index(i)
                destination = select_dest.options[i].text.split(' ')[0] 
                break

        #input cable id
        id_container = driver.find_element(by=By.XPATH, value='//*[@id="frmcable"]/form/article/div[2]/apx-field1[1]/div/div/input')
        id = get_cable_id(origin=origin, destination=destination)
        id_container.clear()
        id_container.send_keys(id)

            

        save_btn = driver.find_element(by=By.XPATH, value='//*[@id="frmcable"]/form/footer/button[1]').click()

    while(1): 

        action = input('Presiona tecla para cambiar etiqueta\n') 
        change_cable_label()