from pydoc import Helper
from cable_manager import CableManager
from constants import CableCodes, JointBoxCodes, SbCodes, Towns
from component_creator import ComponentCreator
from handle_input import handle_input
from remote_connection import RemoteConnection
from helpers import Helpers

WORKING_TOWN = Towns.BURGESS_HILL
WORKING_CLUSTER = 13
keep_open = False
WORKING_TOWN_CODE = 'BUR'

#extention nigga ;)
NUM_EXT = 1
IS_EXT = True

if __name__ == '__main__':

    try:
        helper = Helpers(is_ext=IS_EXT, num_ext=NUM_EXT)
        driver = RemoteConnection.setup_connection()
        creator = ComponentCreator(driver=driver, working_town=WORKING_TOWN,
                                   working_cluster=WORKING_CLUSTER, working_town_code=WORKING_TOWN_CODE, helper=helper)
        cable_manager = CableManager(driver=driver, working_cluster=WORKING_CLUSTER,
                                     working_town_code=WORKING_TOWN_CODE, working_town=WORKING_TOWN, is_ext=IS_EXT, num_ext=NUM_EXT, helper=helper)
        

        keep_open = True

    except:
        print('Error conncting to browser :(')

    print('Start designing')

    while keep_open:
        handle_input(creator=creator,
                     cable_manager=cable_manager, helper=helper)

    print('Something went wrong :(')
