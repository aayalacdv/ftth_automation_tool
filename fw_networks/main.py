from pydoc import Helper
from cable_manager import CableManager
from constants import CableCodes, JointBoxCodes, SbCodes, Towns 
from component_creator import ComponentCreator
from remote_connection import RemoteConnection
from helpers import Helpers 


if __name__ == '__main__': 

    WORKING_TOWN = Towns.DORKING
    WORKING_CLUSTER = 2 

    driver = RemoteConnection.setup_connection()
    creator = ComponentCreator(driver=driver, working_town=WORKING_TOWN, working_cluster=WORKING_CLUSTER)
    cable_manager = CableManager(driver=driver, working_cluster=WORKING_CLUSTER, working_town_code='DOR', working_town=WORKING_TOWN) 

    keep_open = True
    

    while keep_open:
        command = input("ENTER A COMMAND \n") 
        if(command == 'o'): 
            keep_open = False
        elif( command == 'º'): 
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_SMALL)
        elif( command == 'ª'): 
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_MEDIAN)
        elif( command == 'ºº'): 
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_SAM)
        elif( command == 'q'): 
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_12_CLIENTS)
        elif command == 'w':
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_MOS)
        elif(command == 'e'):
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_SAT)
        elif(command == '1'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS)
        elif(command == '2'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_MOS)
        elif(command == '3'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_SAT)
        elif(command == 'a'):
            cable_manager.automate_cable_form(cable_template=CableCodes.CABLE_12_FO)
        elif(command == 's'):
            cable_manager.automate_cable_form(cable_template=CableCodes.CABLE_48_FO)
        elif(command == 'd'):
            cable_manager.automate_cable_form(cable_template=CableCodes.CABLE_36_FO)
        # elif(command == '0'): 
        #     Helpers.scrape_uprns_from_map(driver)
            
