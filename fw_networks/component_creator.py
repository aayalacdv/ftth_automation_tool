import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from constants import SbCodes

from helpers import Helpers 

helper = Helpers()


class ComponentCreator : 

    def __init__(self, driver : webdriver.Chrome, working_town, working_cluster):

        self.driver = driver 
        self.WORKING_CLUSTER =  working_cluster
        self.WORKING_TOWN = working_town

    def create_joint_box(self, joint_box_code): 
    
        #get the position for the joint box 
         mouse_position = pyautogui.position()
         helper.setup_operations_panel(self.driver)

         #click on create joint box 
         create_joint_box_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuOperacio"]/ul/li[6]/a' )))
         create_joint_box = self.driver.find_element_by_xpath('//*[@id="menuOperacio"]/ul/li[6]/a').click()

         #place component on the right position  
         time.sleep(0.5)
         pyautogui.doubleClick(mouse_position)

         #select the correct template 
         select_template_wait = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/select')))
         select_template = Select(self.driver.find_element_by_xpath('//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/select'))
         select_template.select_by_value(joint_box_code)

        #TODO select the correct description 
         description_box = self.driver.find_element(by=By.XPATH, value='//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[2]/div/div/input').send_keys(joint_box_code)

         #select the correct layer
         layer_wait = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button' )))
         layer = self.driver.find_element_by_xpath('//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button').click()
         overlay_panel_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
         upr_option_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/p-overlaypanel/div/div/p-tree/div/div/ul/p-treenode[3]/li/div/span[2]/span')))
         helper.scrape_layers(self.driver,self.WORKING_TOWN,self.WORKING_CLUSTER)

         save_button = self.driver.find_element_by_xpath('//*[@id="frmsplicebox"]/form/footer/button[1]').click()

         #status
         status_wait = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select')))
         status = Select(self.driver.find_element(by=By.XPATH, value='//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
         status.select_by_value('01')

         #details and address
         accordion_clickable = False
         while accordion_clickable == False:
             try: 
                 accordion_clickable = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]' )))
                 accordion_div = self.driver.find_element(by=By.XPATH, value='//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]').click()
                 accordion_clickable = True
             except: 
                 accordion_clickable = False
                 print('not clickable') 

         address_location_component_wait = WebDriverWait(self.driver,100).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'address-location')))
         address_location_component = self.driver.find_element(by=By.TAG_NAME, value='address-location')
         address_btn_wait = WebDriverWait(address_location_component,100).until(EC.element_to_be_clickable((By.TAG_NAME,'button')))
         address_btn = address_location_component.find_element(by=By.TAG_NAME, value='button').click()

         helper.select_chamber_or_parent(self.driver)

         time.sleep(0.5)
         save_button = self.driver.find_element_by_xpath('//*[@id="frmsplicebox"]/form/footer/button[1]').click()

    def create_pole_sb(self,pole_sb_template): 

        #get sb position and open operations pannel 
        mouse_position = pyautogui.position()
        helper.setup_operations_panel(self.driver)

        #click on create cto
        create_cto_wait = WebDriverWait(self.driver,100).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuOperacio"]/ul/li[7]/a'))  )
        create_cto = self.driver.find_element_by_xpath('//*[@id="menuOperacio"]/ul/li[7]/a').click()

        #place the sb on the right position
        time.sleep(0.5)
        pyautogui.doubleClick(mouse_position)

        #select the correct template
        select_template_wait = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select')))
        select_template = Select(self.driver.find_element_by_xpath('//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select'))
        select_template.select_by_value('POLE SB 24 CLIENTS')

        

        #select the correct layer
        layer_wait = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button')))
        layer = self.driver.find_element_by_xpath('//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button').click() 
        overlay_panel_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
        upr_option_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/p-overlaypanel/div/div/p-tree/div/div/ul/p-treenode[2]/li/div/span[1]')))
        helper.scrape_layers(self.driver,self.WORKING_TOWN, self.WORKING_CLUSTER)

        save_button = self.driver.find_element_by_xpath('//*[@id="frmdistributionpoint"]/form/footer/button[1]').click()

        #status
        status_wait = WebDriverWait(self.driver, 100).until(
           EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
        )
        status = Select(self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
        status.select_by_value('01')

        #input the appropiate description
        description = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[2]/div/div/input').clear()
        description = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[2]/div/div/input').send_keys(pole_sb_template)

        #details and address 
        details_clickable = False
        while details_clickable == False: 
            try: 
                details_wait =  WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]')))
                details = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]').click()
                details_clickable = True
            except:
                print('not clickable yet')

        address_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button'))
        )
        address_button = self.driver.find_element(by=By.XPATH, value='//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button').click()

        #select chamber
        helper.select_chamber_or_parent(self.driver)

        #select pole type
        type_wait = WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "option[value='SB POLE']")))
        type_select = Select(self.driver.find_element(by=By.CSS_SELECTOR, value="apx-field1[label='Tipos'] select"))
        if( pole_sb_template == SbCodes.POLE_SB_24_CLIENTS):
            pole_sb_template = 'SB POLE'
        type_select.select_by_value(pole_sb_template)

         #select clients 
        clients_wait = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')))
        clients = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]').click()

        #select add button
        clients = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')
        add_button_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.input-group-btn .glyphicon-plus')))
        add_button = clients.find_element(by=By.TAG_NAME,value='button').click()

        #uprn selection loop
        uprn_selection = True
        while uprn_selection:
            
            select_clients = input('Seleccionar clientes?')
            if select_clients == 'y': 
                uprn_list = helper.scrape_uprns_from_map(self.driver)
                helper.scrape_uprn_from_cto_list(self.driver, uprn_list=uprn_list)

            elif select_clients == 'n':
                uprn_selection = False 




    def  create_joint_chamber_sb(self, sb_template):
        #get sb position and open operations pannel 
        mouse_position = pyautogui.position()
        helper.setup_operations_panel(driver=self.driver)
        #click on create cto
        create_cto_wait = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuOperacio"]/ul/li[7]/a'))  )
        create_cto = self.driver.find_element_by_xpath('//*[@id="menuOperacio"]/ul/li[7]/a').click()

        #place the sb on the right position 
        time.sleep(0.5)
        pyautogui.doubleClick(mouse_position)

        #select the correct template
        select_template_wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select')))
        select_template = Select(self.driver.find_element_by_xpath('//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select'))
        select_template.select_by_value(sb_template)

        #input the appropiate description
        description = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[2]/div/div/input').send_keys(sb_template)


        #select the correct layer
        layer_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button')))
        layer = self.driver.find_element_by_xpath('//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button').click() 
        overlay_panel_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
        upr_option_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/p-overlaypanel/div/div/p-tree/div/div/ul/p-treenode[2]/li/div/span[1]')))
        helper.scrape_layers(self.driver,self.WORKING_TOWN, self.WORKING_CLUSTER)


        save_button = self.driver.find_element_by_xpath('//*[@id="frmdistributionpoint"]/form/footer/button[1]').click()

        #status
        status_wait = WebDriverWait(self.driver, 100).until(
           EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
        )
        status = Select(self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
        status.select_by_value('01')

        #details and address 
        details_clickable = False
        while details_clickable == False: 
            try: 
                details_wait =  WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]')))
                details = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]').click()
                details_clickable = True
            except:
                print('not clickable yet')

        address_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button'))
        )
        address_button = self.driver.find_element(by=By.XPATH, value='//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button').click()

        #select type
        type_select = Select(self.driver.find_element(by=By.CSS_SELECTOR, value='apx-field1[label="Tipos"] select'))
        if sb_template == SbCodes.JOINT_CHAMBER_SB_MOS: 
            type_select.select_by_index(1)
        elif sb_template == SbCodes.JOINT_CHAMBER_SB_SAT: 
            type_select.select_by_index(2)
        elif sb_template == SbCodes.JOINT_CHAMBER_SB_12_CLIENTS: 
            type_select.select_by_index(3)

        #select chamber
        helper.select_chamber_or_parent(self.driver)

        #installation permit
        installation_permit = Select(self.driver.find_element(by=By.XPATH, value='//*[@id="uf_distributionpoint_Installationpermit"]/select'))
        installation_permit.select_by_index(2)

        #select clients 
        clients_wait = WebDriverWait(self.driver, 10).until( EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')))
        clients = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]').click()

        #select add button
        clients = self.driver.find_element(by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')
        add_button_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.input-group-btn .glyphicon-plus')))
        add_button = clients.find_element(by=By.TAG_NAME,value='button').click()

        #uprn selection loop
        uprn_selection = True
        while uprn_selection:
            
            select_clients = input('Seleccionar clientes?')
            if select_clients == 'y': 
                uprn_list = helper.scrape_uprns_from_map(self.driver)
                helper.scrape_uprn_from_cto_list(self.driver, uprn_list=uprn_list)

            elif select_clients == 'n':
                uprn_selection = False 







