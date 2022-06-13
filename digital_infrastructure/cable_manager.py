from ast import Or
from operator import not_
from remote_connection import RemoteConnection
from pydoc import Helper
from cv2 import exp
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from constants import CableCodes

from helpers import Helpers

ORIGIN_ID_XPATH = '//*[@id="frmcable"]/form/article/div[2]/app-location/apx-field1[2]/div/div/div[1]/app-find-closest-element/select'
DEST_ID_XPATH = '//*[@id="frmcable"]/form/article/div[2]/app-location/apx-field1[2]/div/div/div[2]/app-find-closest-element/select'

helper = Helpers()

class CableManager: 

    def __init__(self, driver, working_cluster, working_town_code, working_town):
        self.driver = driver
        self.working_cluster = working_cluster
        self.woring_town_code = working_town_code
        self.workign_town = working_town
        pass
        
    def get_cable_id(self, origin, destination):

        #cluster number is greater than 9
        if self.working_cluster / 10 >= 1: 
            return f'{self.woring_town_code}-CL0{self.working_cluster}-{origin}-{destination}'
        
        #return alternative id otherwise
        return f'{self.woring_town_code}-CL00{self.working_cluster}-{origin}-{destination}'
        

    def automate_cable_form(self, cable_template): 

        # try: 

            self.driver.get('https://digitalinfra.apx-gis.net/#/newCable')


            form_wait = WebDriverWait(self.driver, 600).until(EC.visibility_of_element_located((By.XPATH, ORIGIN_ID_XPATH )))
            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-find-closest-element select option")))

            origin = ''
            origin_option = None
            destination = ''
            destinantion_option = None

            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, ORIGIN_ID_XPATH)))
            select_origin = Select(self.driver.find_element(by=By.XPATH, value=ORIGIN_ID_XPATH))

            for i in range(1,len(select_origin.options)): 
                selection = select_origin.options[i].text.split(':')
                if len(selection) == 1: 
                    origin_option = select_origin.options[i]
                    select_origin.select_by_index(i)
                    WebDriverWait(self.driver, 30).until(EC.element_to_be_selected, origin_option)
                    origin = select_origin.options[i].text.split(' ')[0] 
                    break

            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, DEST_ID_XPATH)))
            select_dest = Select(self.driver.find_element(by=By.XPATH, value = DEST_ID_XPATH))

            for i in range(1,len(select_dest.options)): 
                selection = select_dest.options[i].text.split(':')
                if len(selection) == 1: 
                    destionation_option = select_dest.options[i]
                    select_dest.select_by_index(i)
                    WebDriverWait(self.driver, 30).until(EC.element_to_be_selected, destinantion_option)
                    destination = select_dest.options[i].text.split(' ')[0] 
                    break

            #input cable id
            id_container = self.driver.find_element(by=By.XPATH, value='//*[@id="frmcable"]/form/article/div[2]/apx-field1[1]/div/div/input')
            id = self.get_cable_id(origin=origin, destination=destination)
            id_container.clear()
            id_container.send_keys(id)

            #select the template according to cable size
            template = Select(self.driver.find_element(by=By.XPATH, value='//*[@id="frmcable"]/form/article/div[2]/apx-field1[4]/div/div/select'))
            template.select_by_value(cable_template) 


            #select layer
            layer_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmcable"]/form/article/div[2]/apx-field1[5]/div/div/app-find-layer/button')))
            layer = self.driver.find_element_by_xpath('//*[@id="frmcable"]/form/article/div[2]/apx-field1[5]/div/div/app-find-layer/button').click() 
            overlay_panel_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
            #upr_option_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frmcable"]/form/article/div[2]/apx-field1[5]/div/div/app-find-layer/p-overlaypanel/div/div/p-tree/div/div/ul/p-treenode[4]/li/div/div/div/span')))
            helper.scrape_layers(self.driver,self.workign_town, self.working_cluster)

            save_button = self.driver.find_element_by_xpath('//*[@id="frmcable"]/form/footer/button[1]').click()

            #cable details
            not_clickable = True
            while not_clickable: 
                try: 
                    details_wait = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"p-accordiontab[header='Cable Details'] span")))
                    details = self.driver.find_element(by=By.CSS_SELECTOR, value="p-accordiontab[header='Cable Details'] span").click()
                    not_clickable = False
                except: 
                    pass

                
            size_wait = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"apx-field1[label='Size'] input")))
            size = self.driver.find_element(by= By.CSS_SELECTOR, value= "apx-field1[label='Size'] input")

            cable_size = size.get_attribute('value')
            print(cable_size)
            tubes = int(int(cable_size)/ 10)
            print(tubes)

            size_wait = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"apx-field1[label='Tubes'] input")))
            tubes_input = self.driver.find_element(by=By.CSS_SELECTOR, value="apx-field1[label='Tubes'] input")
            tubes_input.send_keys(tubes) 

            if cable_template == CableCodes.CABLE_48_FO_ULW or cable_template == CableCodes.CABLE_12_FO_ULW: 

                WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"apx-field1[label='Comentarios'] textarea")))
                comments = self.driver.find_element(by=By.CSS_SELECTOR, value="apx-field1[label='Comentarios'] textarea")
                comments.send_keys('AERIAL')

            save_button = self.driver.find_element_by_xpath('//*[@id="frmcable"]/form/footer/button[1]').click()

        # except: 
        #     self.driver = RemoteConnection.setup_connection()
        #     print('Eror creating cable')



    