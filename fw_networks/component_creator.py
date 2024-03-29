import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from constants import SbCodes
from custom_wait_conditions import element_text_not_null
from handle_input import handle_uprn_response

from remote_connection import RemoteConnection



class ComponentCreator:

    def __init__(self, driver: webdriver.Chrome, working_town, working_cluster, working_town_code, helper):

        self.driver = driver
        self.WORKING_CLUSTER = working_cluster
        self.WORKING_TOWN = working_town
        self.WORKING_TOWN_CODE = working_town_code
        self.helper = helper


    def create_joint_box(self, joint_box_code):

        # try:
        print(f"Creating {joint_box_code}")
        # get the position for the joint box
        mouse_position = pyautogui.position()
        self.driver.get(
            'https://fwnetworks.apx-gis.net/#/spliceboxs.add')

        # place component on the right position
        WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.ID, 'frmConfirmAction')))
        time.sleep(0.5)
        pyautogui.doubleClick(mouse_position)

        template_option = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"apx-field1[label='Template'] select option[value='{joint_box_code}']")))
        select_web_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "apx-field1[label='Template'] select")))
        select_template = Select(select_web_element)
        select_template.select_by_value(joint_box_code)
        WebDriverWait(self.driver, 30).until(EC.element_located_to_be_selected(
            (By.CSS_SELECTOR, f"apx-field1[label='Template'] select option[value='{joint_box_code}']")))

        layer_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "apx-field1[label='Layer'] app-find-layer button"))).click()
        overlay_panel_wait = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
        self.helper.scrape_layers(
            self.driver, self.WORKING_TOWN, self.WORKING_CLUSTER, working_cluster_code=self.WORKING_TOWN_CODE)

        save_button = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'footer button.btn-success'))).click()

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

        description_input = self.driver.find_element(
            by=By.CSS_SELECTOR, value="apx-field1[label='Description'] input")
        description_input.clear()
        description_input .send_keys(joint_box_code)

        location_button = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'address-location button')))
        self.driver.execute_script("arguments[0].click();", location_button)
        location_input = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'address-location input')))

        WebDriverWait(self.driver, 30).until(
            element_text_not_null(location_input))

        self.helper.select_chamber_or_parent(self.driver)

        # status
        # wait firts for the option, the select it
        designed_option = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "apx-combo-codificador select option[value='01']")))
        status_web_element = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'apx-combo-codificador select')))
        status = Select(status_web_element)
        status.select_by_value('01')
        # Wait until option is selected
        WebDriverWait(self.driver, 30).until(
            EC.element_located_to_be_selected((By.CSS_SELECTOR, "apx-combo-codificador select option[value='01']")))

        time.sleep(0.5)
        save_button = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'footer button.btn-success'))).click()

        # except:
        #     self.driver = RemoteConnection.setup_connection()
        #     print("Something went wrogn creating joint box, restart :(")

    def create_pole_sb(self, pole_sb_template):

        try:
            print(f'CREATING {pole_sb_template}')
            # get sb position and open operations pannel
            mouse_position = pyautogui.position()

            self.driver.get(
                'https://fwnetworks.apx-gis.net/#/distributionpoints.add')

            # place the sb on the right position
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, 'frmConfirmAction')))
            time.sleep(0.5)
            pyautogui.doubleClick(mouse_position)

            # select the correct template
            select_option = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"apx-field1[label='Template'] select option[value='{pole_sb_template}']")))
            select_component = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "apx-field1[label='Template'] select")))
            select_template = Select(select_component)
            select_template.select_by_value(pole_sb_template)
            WebDriverWait(self.driver, 100).until(
                EC.element_to_be_selected(select_option))

            layer_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "apx-field1[label='Layer'] app-find-layer button"))).click()
            overlay_panel_wait = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
            self.helper.scrape_layers(
                self.driver, self.WORKING_TOWN, self.WORKING_CLUSTER, working_cluster_code=self.WORKING_TOWN_CODE)

            save_button = self.driver.find_element(
                by=By.CSS_SELECTOR, value='footer .btn-success').click()

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

            # status

            location_button = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'address-location button')))
            self.driver.execute_script(
                "arguments[0].click();", location_button)
            location_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'address-location input')))

            WebDriverWait(self.driver, 30).until(
                element_text_not_null(location_input))

            # select chamber
            self.helper.select_chamber_or_parent(self.driver)


            designed_option = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "apx-combo-codificador select option[value='01']")))
            status_web_element = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'apx-combo-codificador select')))
            status = Select(status_web_element)
            status.select_by_value('01')

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
                    uprn_list = self.helper.scrape_uprns_from_map(self.driver)
                    self.helper.scrape_uprn_from_cto_list(
                        self.driver, uprn_list=uprn_list)

                else:
                    uprn_selection = False

        except:
            self.driver = RemoteConnection.setup_connection()
            print('Something went wrong creating pole sb :(')

    def create_joint_chamber_sb(self, sb_template):
        try:
            # print the box to the user
            print(f'creating {sb_template}')
            mouse_position = pyautogui.position()

            # go to the url to avoid random shit
            self.driver.get(
                'https://fwnetworks.apx-gis.net/#/distributionpoints.add')

            # place the sb on the right position
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, 'frmConfirmAction')))
            time.sleep(0.5)
            pyautogui.doubleClick(mouse_position)

            # select the template
            # select the correct template
            select_option = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"apx-field1[label='Template'] select option[value='{sb_template}']")))
            select_component = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "apx-field1[label='Template'] select")))
            select_template = Select(select_component)
            select_template.select_by_value(sb_template)
            WebDriverWait(self.driver, 100).until(
                EC.element_to_be_selected(select_option))

            layer_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "apx-field1[label='Layer'] app-find-layer button"))).click()
            overlay_panel_wait = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ui-overlaypanel')))
            self.helper.scrape_layers(
                self.driver, self.WORKING_TOWN, self.WORKING_CLUSTER, working_cluster_code=self.WORKING_TOWN_CODE)

            save_button = self.driver.find_element(
                by=By.CSS_SELECTOR, value='footer .btn-success').click()

            #details and address
            details_clickable = False
            while details_clickable == False:
                try:
                    details_wait = WebDriverWait(self.driver, 100).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "p-accordiontab[header='Details'] a")))
                    details = self.driver.find_element(
                        by=By.CSS_SELECTOR, value="p-accordiontab[header='Details'] a").click()
                    details_clickable = True
                except:
                    print('not clickable yet')

            location_button = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'address-location button')))
            self.driver.execute_script(
                "arguments[0].click();", location_button)
            location_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'address-location input')))

            WebDriverWait(self.driver, 30).until(
                element_text_not_null(location_input))

            # select chamber
            self.helper.select_chamber_or_parent(self.driver)

            designed_option = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "apx-combo-codificador select option[value='01']")))
            status_web_element = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'apx-combo-codificador select')))
            status = Select(status_web_element)
            status.select_by_value('01')

            # put description field and type
            description_field = self.driver.find_element(
                by=By.CSS_SELECTOR, value='apx-field1[label="Description"] input')
            description_field.clear()
            description_field.send_keys(sb_template)

            select_type = Select(self.driver.find_element(
                by=By.CSS_SELECTOR, value='apx-field1[label="Type"] select'))
            if sb_template == SbCodes.JOINT_CHAMBER_SB_MOS:
                select_type.select_by_value('JOINT CHAMBER SB 12 MOS')
            elif sb_template == SbCodes.JOINT_CHAMBER_SB_SAT:
                select_type.select_by_value('JOINT CHAMBER SB 12 SAT')

            # installation permit
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#uf_distributionpoint_Installationpermit select'))
            )
            installation_permit = Select(self.driver.find_element(
                by=By.CSS_SELECTOR, value='#uf_distributionpoint_Installationpermit select'))

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "option[value='Civil work required']"))
            )

            installation_permit.select_by_value('Civil work required')

            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_selected(self.driver.find_element(
                    by=By.CSS_SELECTOR, value="option[value='Civil work required']"))
            )

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
                    uprn_list = self.helper.scrape_uprns_from_map(self.driver)
                    self.helper.scrape_uprn_from_cto_list(
                        self.driver, uprn_list=uprn_list)

                else:
                    uprn_selection = False

        except:
            self.driver = RemoteConnection.setup_connection()
            print('Something went wrong creating joint box sb')
