from cable_manager import CableManager
from constants import  Towns 
from component_creator import ComponentCreator
from handle_input import handle_input
from selenium.webdriver.common.by import By
from helpers import Helpers
from remote_connection import RemoteConnection

WORKING_TOWN = Towns.CARNFORTH
WORKING_CLUSTER = 1 
keep_open = False 
WORKING_TOWN_CODE = 'CAR'

if __name__ == '__main__': 

    try: 
        driver = RemoteConnection.setup_connection()
        creator = ComponentCreator(driver=driver, working_town=WORKING_TOWN, working_cluster=WORKING_CLUSTER, working_town_code=WORKING_TOWN_CODE)
        cable_manager = CableManager(driver=driver, working_cluster=WORKING_CLUSTER, working_town_code=WORKING_TOWN_CODE, working_town=WORKING_TOWN) 
        helper = Helpers()

        keep_open = True 
    except: 
        print('Error conncting to browser :(')
    print('Start designing')
    


    while keep_open: 
        handle_input(creator=creator, cable_manager=cable_manager, helper=helper)

    print('Something went wrong :(')


    


