from asyncio.windows_events import NULL
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pyautogui
import win32gui
from image_recognition.position_manager import get_house_positions, get_real_positions, get_region_position

from image_recognition.screenshot_manager import get_region


class Helpers:

    def __init__(self, is_ext=False, num_ext=1) -> None:
        self.is_ext = is_ext
        self.num_ext = num_ext


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
        if self.is_ext: 
            return f"{working_cluster_code}-EXT 0{self.num_ext}"

        if working_cluster < 10:
            return f"{working_cluster_code}-CLUSTER 0{working_cluster}"

        return f"{working_cluster_code}-CLUSTER {working_cluster}"


    def scrape_layers(self, driver, working_town, working_cluster, working_cluster_code):
        # get nodes with layer info
        parent = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f".ui-treenode-content[aria-label='{working_town}']"))).find_element(by=By.XPATH, value='..')
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, f".ui-treenode-content[aria-label='{working_town}'] .ui-tree-toggler")))
        driver.execute_script(
            f'''document.querySelectorAll(".ui-treenode-content[aria-label='{working_town}'] .ui-tree-toggler")[0].click()''')

        aria_label = self.get_treenode_identifier(
            working_cluster=working_cluster, working_cluster_code=working_cluster_code)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f".ui-treenode-selectable[aria-label='{aria_label}'] .ui-chkbox-box"))).click()

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
                popup_wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'leaflet-popup-content-wrapper')))

                # get uprn code and adress
                popup = driver.find_element(
                    by=By.CLASS_NAME, value='leaflet-popup-content-wrapper')
                a = popup.find_element(by=By.TAG_NAME, value='a')

                uprns.append(a.text)

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
