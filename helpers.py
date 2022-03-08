from asyncio.windows_events import NULL
import time
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pyautogui
from image_recognition.position_manager import get_house_positions, get_real_positions, get_region_position

from image_recognition.screenshot_manager import get_region 


class Helpers: 

    def __init__(self) -> None:
        pass

    def select_chamber_or_parent(self, driver): 
        find_closest_element =  driver.find_element(by=By.TAG_NAME, value='app-find-closest-element')
        child = find_closest_element.find_element(by=By.CLASS_NAME, value='form-control')
        select = Select(child)
        select.select_by_index(1)


    def click_joint_details(self, driver): 
        accordion_clickable = False
        while accordion_clickable == False:
            try: 
                accordion_clickable = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]/div[1]' )))
                accordion_div = driver.find_element(by=By.XPATH, value='//*[@id="frmsplicebox"]/form/article/div[2]/p-accordion/div/p-accordiontab[1]/div[1]')
                child = accordion_div.find_element(by=By.TAG_NAME, value='a').click()
                accordion_clickable = True
            except: 
                print('not clickable') 



    def setup_operations_panel(self, driver): 

        side_menu = driver.find_element(by=By.ID, value='divMenu')
        side_menu_toggler = driver.find_element(by=By.ID,  value='btShowMenu')

        #expand the side menu if needed 
        if( side_menu.value_of_css_property('display') == 'none'): 
            side_menu_toggler.click()

        try: 
            operations_menu_wait = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/ul/li[3]/a')))
            operations_menu_toggler = driver.find_element(by=By.ID, value='menuOperacio')

            if(operations_menu_toggler.value_of_css_property('height') != 'auto'):  
               return

            operations_menu = driver.find_element(by=By.XPATH, value='//*[@id="sidebar"]/ul/li[3]/a').click()

        except: 
                print('Error locationg Element')    




    def scrape_layers(self, driver,working_town, working_cluster):

        #get nodes with layer info
        overlay_panel = driver.find_element(by=By.CLASS_NAME, value='ui-overlaypanel')
        tree_nodes = overlay_panel.find_elements(by=By.CLASS_NAME, value='ui-treenode-content')

        #extract layer info 
        for node in tree_nodes: 

                span = node.find_element(by=By.CLASS_NAME, value='ui-treenode-label')
                if(span.text == working_town): 
                    node.find_element(by=By.CLASS_NAME, value='ui-tree-toggler').click(); 

                    #wait for the cluster list to be visible
                    node_children_wait = WebDriverWait(driver,100).until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-treenode-children')))
                    node_children = driver.find_element(by=By.CLASS_NAME, value='ui-treenode-children')

                    #get the node content to find the cluster
                    node_content = node_children.find_elements(by=By.CLASS_NAME, value='ui-treenode-content')

                    for content in node_content: 
                        span_label = content.find_element(by=By.CLASS_NAME, value='ui-treenode-label')
                        label = span_label.find_element(by=By.TAG_NAME, value='span')
                        cluster = label.text.split()

                        try: 
                            if(int(cluster[1]) == working_cluster): 
                                cluster_checkbox = content.find_element(by=By.CLASS_NAME, value='ui-chkbox-box').click() 
                                return 
                        except:
                            pass
    
    def scrape_uprns_from_map(self, driver):
        
        #get position of uprns on map
        get_region()
        time.sleep(0.25)
        region_position = get_region_position()
        house_positions = get_house_positions()

        real_positions = get_real_positions(region_position, house_positions)
        #create a list of uprns 
        uprns = []

        for pos in real_positions: 
            try: 
                pyautogui.click(pos)
                time.sleep(0.5)

                #wait until popup visible 
                popup_wait = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'leaflet-popup-content-wrapper')))

                #get uprn code and adress 
                popup = driver.find_element(by=By.CLASS_NAME, value='leaflet-popup-content-wrapper')
                a = popup.find_element(by=By.TAG_NAME, value='a')

                uprns.append(a.text)

            except: 
               pass

        return uprns

    def scrape_uprn_from_cto_list(self, driver, uprn_list):
        
        #wait until table is visible
        uprn_table_wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="frmFndClient"]/form/article/table')))

        #get list by looping through tr elements 
        uprn_table = driver.find_element(by=By.XPATH, value='//*[@id="frmFndClient"]/form/article/table')

        uprns = uprn_table.find_elements(by=By.TAG_NAME, value='tr')

        for tr in uprns: 

            try: 
                house = tr.find_element(by=By.TAG_NAME, value='td')
                
                if(house.text in uprn_list): 
                    tr.click()
            except:
                pass



