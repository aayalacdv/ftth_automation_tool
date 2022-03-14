from pydoc import Helper
from cable_manager import CableManager
from constants import JointBoxCodes, SbCodes, Towns 
from component_creator import ComponentCreator
from remote_connection import RemoteConnection
from helpers import Helpers 


if __name__ == '__main__': 

    WORKING_TOWN = Towns.CARLTON
    WORKING_CLUSTER = 11

    driver = RemoteConnection.setup_connection()
    creator = ComponentCreator(driver=driver, working_town=WORKING_TOWN, working_cluster=WORKING_CLUSTER)

    keep_open = True
    


    while keep_open:
        command = input("ENTER A COMMAND \n") 
        if(command == 'o'): 
            keep_open = False
        elif( command == 'º'): 
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_SMALL)
        elif( command == 'ª'): 
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_MEDIAN)
        elif( command == 'q'): 
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_12_CLIENTS)
        elif(command == 'w'):
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_MOS)
        elif(command == 'e'):
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_SAT)
        elif(command == '1'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS)
        elif(command == '2'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_MOS)
        elif(command == '3'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_SAT)
        elif(command == '0'): 
            cable_manager = CableManager(driver=driver, working_cluster=WORKING_CLUSTER, working_town_code='CHT', working_town=WORKING_TOWN) 
            id = cable_manager.get_cable_id('J13081','SB39786')
            print(id)

            cable_manager.automate_cable_form(cable_template='12 f.o.')


