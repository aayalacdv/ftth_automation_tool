from asyncio.windows_events import NULL
import time
import selenium
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pyautogui
from image_recognition.position_manager import get_house_positions, get_real_positions, get_region_position
import win32gui

from image_recognition.screenshot_manager import get_region


class Helpers:

    def __init__(self) -> None:
        pass

    def add_splitter(self, driver) -> None:

        driver.find_element(
            by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[4]/div[1]').click()
        #cambiar el selector porque sino peta xdddd
        spl_count = int(driver.find_element(
            by=By.XPATH, value='//*[@id="ui-accordiontab-24"]/span[2]').text.split()[2][1])

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "app-networkclient-list .btn-success"))).click()

        network_client_type = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "apx-field1[label='Networkclient type'] select")))
        select = Select(network_client_type)

        option = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='splitter']")))
        select.select_by_value('splitter')

        WebDriverWait(driver, 30).until(EC.element_to_be_selected(option))

        input = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "apx-field1[label='Código'] input")))
        input.send_keys(f"SPL0{spl_count + 1}")

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[value='9']"))).find_element(by=By.XPATH, value='..').click()

        select_operador = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "apx-field1[label='Operador'] select")))
        select = Select(select_operador)

        digital_operador = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "option[value='xxxx-a2f9-6b2778fb-9be64d23-0646477c']")))
        select.select_by_value('xxxx-a2f9-6b2778fb-9be64d23-0646477c')
        WebDriverWait(driver, 30).until(
            EC.element_to_be_selected(digital_operador))

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ui-accordiontab-24-content"]/div/app-networkclient-list/app-networkclient/apx-form1/form/footer/button[1]'))).click()

    def delete_splitter(self, driver) -> None:
        driver.find_element(
            by=By.XPATH, value='//*[@id="frmdistributionpoint"]/form/article/div[2]/p-accordion/div/p-accordiontab[4]/div[1]').click()
        spl_count = int(driver.find_element(
            by=By.XPATH, value='//*[@id="ui-accordiontab-24"]/span[2]').text.split()[2][1])

        WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"app-networkclient-list table td")))
        spls = driver.find_elements(
            by=By.CSS_SELECTOR, value="app-networkclient-list table td")

        for element in spls:
            print(element.text)
            if len(element.text) == 5:
                if element.text[4] == str(spl_count):
                    element.click()
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'footer button .btn-danger'))).click()
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="btConfirmSi"]'))).click()

    def select_chamber_or_parent(self, driver):
        find_closest_element = driver.find_element(
            by=By.TAG_NAME, value='app-find-closest-element')
        child = find_closest_element.find_element(
            by=By.CLASS_NAME, value='form-control')
        select = Select(child)
        select.select_by_index(1)

    def click_joint_details(self, driver):
        accordion_clickable = False
        while accordion_clickable == False:
            try:
                accordion_clickable = WebDriverWait(driver, 100).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]/div[1]')))
                accordion_div = driver.find_element(
                    by=By.XPATH, value='//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]/div[1]')
                child = accordion_div.find_element(
                    by=By.TAG_NAME, value='a').click()
                accordion_clickable = True
            except:
                print('not clickable')

    def setup_operations_panel(self, driver):

        side_menu = driver.find_element(by=By.ID, value='divMenu')
        side_menu_toggler = driver.find_element(by=By.ID,  value='btShowMenu')

        # expand the side menu if needed
        if(side_menu.value_of_css_property('display') == 'none'):
            side_menu_toggler.click()

        try:
            operations_menu_wait = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/ul/li[3]/a')))
            operations_menu_toggler = driver.find_element(
                by=By.ID, value='menuOperacio')

            if(operations_menu_toggler.value_of_css_property('height') != 'auto'):
                return

            operations_menu = driver.find_element(
                by=By.XPATH, value='//*[@id="sidebar"]/ul/li[3]/a').click()

        except:
            print('Error locationg Element')

    def get_treenode_identifier(self, working_cluster, working_cluster_code) -> str:
        if working_cluster < 10:
            return f"{working_cluster_code}-CLUSTER 0{working_cluster}"

        return f"{working_cluster_code}-CLUSTER {working_cluster}"

    def scrape_layers(self, driver, working_town, working_cluster, working_cluster_code):

        # get nodes with layer info
        parent = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f".ui-treenode-content[aria-label='{working_town}']"))).find_element(by=By.XPATH, value='..')
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f".ui-treenode-content[aria-label='{working_town}'] .ui-tree-toggler"))).click()

        aria_label = self.get_treenode_identifier(
            working_cluster=working_cluster, working_cluster_code=working_cluster_code)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f".ui-treenode-selectable[aria-label='{aria_label}'] .ui-chkbox-box"))).click()

    def testing(self, driver) -> list:
        res = []

        uprns = driver.find_elements(
            by=By.CSS_SELECTOR, value="a[href^='#uprn']")

        parent = uprns[0].find_element(by=By.XPATH, value='./ancestor::div[3]')
        span = parent.find_element(by=By.CSS_SELECTOR, value=".type_count")

        # if the child coutn matches it means all of the houeses loaded correctly

        child_count = driver.execute_script(
            'return document.querySelector(".ng-star-inserted div").childElementCount')
        print(f" element count: {child_count}")

        res = [uprn.text for uprn in uprns]

        print(res)
        return res

    def scrape_uprns_from_map(self, driver):

        # get position of uprns on map
        get_region()
        time.sleep(0.25)
        region_position = get_region_position()
        house_positions = get_house_positions()

        real_positions = get_real_positions(region_position, house_positions)
        # create a list of uprns

        uprns = []
        for pos in real_positions:
            try:
                pyautogui.click(pos)
                time.sleep(0.5)

                # wait until popup visible
                uprn_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a[href^='#uprn']")))

                # get uprn code and adress
                res = [uprn.text for uprn in uprn_elements if uprn.text != '']

                uprns = uprns + res

            except:
                pass

        return uprns

    def scrape_uprn_from_cto_list(self, driver, uprn_list):

        # wait until table is visible
        uprn_table_wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="frmFndClient"]/form/article/table')))

        # get list by looping through tr elements
        uprn_table = driver.find_element(
            by=By.XPATH, value='//*[@id="frmFndClient"]/form/article/table')

        uprns = uprn_table.find_elements(by=By.TAG_NAME, value='tr')

        for tr in uprns:

            try:
                house = tr.find_element(by=By.TAG_NAME, value='td')

                if(house.text in uprn_list):
                    tr.click()
            except:
                pass

    def is_apx_active_window(self) -> bool:

        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)

        if active_window_name == 'APX - Digital Infrastructure - Google Chrome':
            return True

        return False
