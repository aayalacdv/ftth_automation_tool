from cable_manager import CableManager
from constants import  Towns 
from component_creator import ComponentCreator
from handle_input import handle_input
from remote_connection import RemoteConnection

WORKING_TOWN = Towns.LUTTERWORTH
WORKING_CLUSTER = 2 
keep_open = False 
WORKING_TOWN_CODE = 'LUT'

if __name__ == '__main__': 

    try: 
        driver = RemoteConnection.setup_connection()
        creator = ComponentCreator(driver=driver, working_town=WORKING_TOWN, working_cluster=WORKING_CLUSTER)
        cable_manager = CableManager(driver=driver, working_cluster=WORKING_CLUSTER, working_town_code=WORKING_TOWN_CODE, working_town=WORKING_TOWN) 

        keep_open = True 
    except: 
        print('Error conncting to browser :(')
    print('Start designing')
    
    while keep_open: 
        handle_input(creator=creator, cable_manager=cable_manager)

    print('Something went wrong :(')


    


