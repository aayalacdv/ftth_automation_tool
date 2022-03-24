from pydoc import Helper

from setuptools import Command
from cable_manager import CableManager
from constants import CableCodes, JointBoxCodes, SbCodes, Towns 
from component_creator import ComponentCreator
from remote_connection import RemoteConnection
from helpers import Helpers 
import keyboard 


if __name__ == '__main__': 

    WORKING_TOWN = Towns.CARLTON
    WORKING_CLUSTER = 6

    driver = RemoteConnection.setup_connection()
    creator = ComponentCreator(driver=driver, working_town=WORKING_TOWN, working_cluster=WORKING_CLUSTER)
    cable_manager = CableManager(driver=driver, working_cluster=WORKING_CLUSTER, working_town_code='CHT', working_town=WORKING_TOWN) 

    keep_open = True

    print("Eneter a command\n")
    while keep_open:
        if(keyboard.is_pressed('º+space')): 
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_SMALL)
        if(keyboard.is_pressed('ª+space')): 
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_MEDIAN)
        if(keyboard.is_pressed('q+space') | keyboard.is_pressed('Q+space')): 
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_12_CLIENTS)
        if(keyboard.is_pressed('w+space') | keyboard.is_pressed('W+space')): 
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_MOS)
        if(keyboard.is_pressed('e+space') | keyboard.is_pressed('E+space')): 
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_SAT)
        if(keyboard.is_pressed('1+space')): 
           creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS) 
        if(keyboard.is_pressed('2+space')): 
           creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_MOS) 
        if(keyboard.is_pressed('3+space')): 
           creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_SAT) 
        if keyboard.is_pressed('a+space') | keyboard.is_pressed('A+space'):
            cable_manager.automate_cable_form(cable_template=CableCodes.CABLE_12_FO)
        if keyboard.is_pressed('s+space') | keyboard.is_pressed('S+space'):
            cable_manager.automate_cable_form(cable_template=CableCodes.CABLE_48_FO)
        if keyboard.is_pressed('d+space') | keyboard.is_pressed('D+space'):
            cable_manager.automate_cable_form(cable_template=CableCodes.CABLE_12_FO_ULW)
        if keyboard.is_pressed('f+space') | keyboard.is_pressed('F+space'):
            cable_manager.automate_cable_form(cable_template=CableCodes.CABLE_48_FO_ULW)


