import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from handle_input import handle_uprn_response


from helpers import Helpers
from remote_connection import RemoteConnection

helper = Helpers()


class ComponentCreator:

    def __init__(self, driver: webdriver.Chrome, working_town, working_cluster):

        self.driver = driver
        self.WORKING_CLUSTER = working_cluster
        self.WORKING_TOWN = working_town

    def create_joint_box(self, joint_box_code):
        try:
            print(f"Creating {joint_box_code}")
            # get the position for the joint box
            mouse_position = pyautogui.position()
            self.driver.get(
                'https://digitalinfra.apx-gis.net/#/spliceboxs.add')

            # place component on the right position
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.ID, 'frmConfirmAction')))
            time.sleep(0.5)
            pyautogui.doubleClick(mouse_position)

            # select the correct template
            select_template_wait = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/select')))
            select_template = Select(self.driver.find_element_by_xpath(
                '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/select'))
            select_template.select_by_value(joint_box_code)

            # select the correct layer
            layer_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button')))
            layer = self.driver.find_element_by_xpath(
                '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button').click()
            overlay_panel_wait = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
            upr_option_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/p-overlaypanel/div/div/p-tree/div/div/ul/p-treenode[6]/li/div/span/span')))
            helper.scrape_layers(
                self.driver, self.WORKING_TOWN, self.WORKING_CLUSTER)

            save_button = self.driver.find_element_by_xpath(
                '//*[@id="frmsplicebox"]/form/footer/button[1]').click()

            # status
            status_wait = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select')))
            status = Select(self.driver.find_element(
                by=By.XPATH, value='//*[@id="frmsplicebox"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
            designed_option = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='01']")))
            status.select_by_value('01')

            #details and address
            accordion_clickable = False
            while accordion_clickable == False:
                try:
                    accordion_clickable = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]')))
                    accordion_div = self.driver.find_element(
                        by=By.XPATH, value='//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]').click()
                    accordion_clickable = True
                except:
                    accordion_clickable = False
                    print("Wait until element is clickable")

            address_location_component_wait = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_all_elements_located((By.TAG_NAME, 'address-location')))
            address_location_component = self.driver.find_element(
                by=By.TAG_NAME, value='address-location')
            address_btn_wait = WebDriverWait(address_location_component, 100).until(
                EC.element_to_be_clickable((By.TAG_NAME, 'button')))
            address_btn = address_location_component.find_element(
                by=By.TAG_NAME, value='button').click()

            helper.select_chamber_or_parent(self.driver)

            time.sleep(0.5)
            save_button = self.driver.find_element_by_xpath(
                '//*[@id="frmsplicebox"]/form/footer/button[1]').click()
        except:
            self.driver = RemoteConnection.setup_connection()
            print("Something went wrogn creating joint box, restart :(")

    def create_pole_sb(self, pole_sb_template):

        try: 
            print(f'CREATING {pole_sb_template}') 
            # get sb position and open operations pannel
            mouse_position = pyautogui.position()

            self.driver.get('https://digitalinfra.apx-gis.net/#/distributionpoints.add')

            # place the sb on the right position
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.ID, 'frmConfirmAction')))
            time.sleep(0.5)
            pyautogui.doubleClick(mouse_position)

            # select the correct template
            select_template_wait = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select')))
            select_template = Select(self.driver.find_element_by_xpath(
                '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select'))
            select_template.select_by_value(pole_sb_template)

            # select the correct layer
            layer_wait = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button')))
            layer = self.driver.find_element_by_xpath(
                '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button').click()
            overlay_panel_wait = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
            upr_option_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/p-overlaypanel/div/div/p-tree/div/div/ul/p-treenode[6]/li/div/span/span')))
            helper.scrape_layers(
                self.driver, self.WORKING_TOWN, self.WORKING_CLUSTER)

            save_button = self.driver.find_element_by_xpath(
                '//*[@id="frmdistributionpoint"]/form/footer/button[1]').click()

            # status
            status_wait = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
            )
            status = Select(self.driver.find_element(
                by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
            designed_option = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='01']")))
            status.select_by_value('01')

            #details and address
            details_clickable = False
            while details_clickable == False:
                try:
                    details_wait = WebDriverWait(self.driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]')))
                    details = self.driver.find_element(
                        by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]').click()
                    details_clickable = True
                except:
                    print('not clickable yet')

            address_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button'))
            )
            address_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button').click()

            # select chamber
            helper.select_chamber_or_parent(self.driver)

            # select clients
            clients_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')))
            clients = self.driver.find_element(
                by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]').click()

            # select add button
            clients = self.driver.find_element(
                by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')
            add_button_wait = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.input-group-btn .glyphicon-plus')))
            add_button = clients.find_element(
                by=By.TAG_NAME, value='button').click()

            # uprn selection loop
            uprn_selection = True
            while uprn_selection:
                
                select_clients = handle_uprn_response()
                if select_clients: 
                    uprn_list = helper.scrape_uprns_from_map(self.driver)
                    helper.scrape_uprn_from_cto_list(
                        self.driver, uprn_list=uprn_list)

                else:
                    uprn_selection = False

        except: 
            self.driver = RemoteConnection.setup_connection()
            print('Something went wrong creating pole sb :(')

    def create_joint_chamber_sb(self, sb_template):
        try: 
            print(f'creating {sb_template}')
            mouse_position = pyautogui.position()

            self.driver.get('https://digitalinfra.apx-gis.net/#/distributionpoints.add')

            # place the sb on the right position
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.ID, 'frmConfirmAction')))
            time.sleep(0.5)
            pyautogui.doubleClick(mouse_position)

            # select the correct template
            select_template_wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select')))
            select_template = Select(self.driver.find_element_by_xpath(
                '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/select'))
            select_template.select_by_value(sb_template)

            # select the correct layer
            layer_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button')))
            layer = self.driver.find_element_by_xpath(
                '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/button').click()
            overlay_panel_wait = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
            upr_option_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[4]/div/div/app-find-layer/p-overlaypanel/div/div/p-tree/div/div/ul/p-treenode[6]/li/div/span/span')))
            helper.scrape_layers(
                self.driver, self.WORKING_TOWN, self.WORKING_CLUSTER)

            save_button = self.driver.find_element_by_xpath(
                '//*[@id="frmdistributionpoint"]/form/footer/button[1]').click()

            # status
            status_wait = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
            )
            status = Select(self.driver.find_element(
                by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/apx-field1[3]/div/div/apx-combo-codificador/select'))
            designed_option = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='01']")))
            status.select_by_value('01')

            #details and address
            details_clickable = False
            while details_clickable == False:
                try:
                    details_wait = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]')))
                    details = self.driver.find_element(
                        by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]').click()
                    details_clickable = True
                except:
                    print('not clickable yet')

            address_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button'))
            )
            address_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="distributionpoint_location"]/div/div/address-location/div/span/button').click()

            # select chamber
            helper.select_chamber_or_parent(self.driver)

            # installation permit
            installation_permit = Select(self.driver.find_element(
                by=By.XPATH, value='//*[@id="uf_distributionpoint_Installationpermit"]/select'))
            installation_permit.select_by_index(2)

            # select clients
            clients_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')))
            clients = self.driver.find_element(
                by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]').click()

            # select add button
            clients = self.driver.find_element(
                by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[2]')
            add_button_wait = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.input-group-btn .glyphicon-plus')))
            add_button = clients.find_element(
                by=By.TAG_NAME, value='button').click()

            # uprn selection loop
            uprn_selection = True
            while uprn_selection:
                
                select_clients = handle_uprn_response()
                if select_clients: 
                    uprn_list = helper.scrape_uprns_from_map(self.driver)
                    helper.scrape_uprn_from_cto_list(
                        self.driver, uprn_list=uprn_list)

                else:
                    uprn_selection = False

        except: 
            self.driver = RemoteConnection.setup_connection()
            print('Something went wrong creating joint box sb')