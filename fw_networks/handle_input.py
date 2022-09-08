import keyboard

from constants import CableCodes, JointBoxCodes, SbCodes
from helpers import Helpers


def handle_input(creator, cable_manager, helper: Helpers):

    if helper.is_apx_active_window:
        if keyboard.is_pressed('º+space'):
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_SMALL)
            print('Enter a command')

        if keyboard.is_pressed('ª+space'):
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_MEDIAN)
            print('Enter a command')

        if keyboard.is_pressed('<+space'):
            creator.create_joint_box(JointBoxCodes.JOINT_BOX_SAM)
            print('Enter a command')


        if keyboard.is_pressed('q+space') | keyboard.is_pressed('Q+space'):
            creator.create_joint_chamber_sb(
                SbCodes.JOINT_CHAMBER_SB_12_CLIENTS)
            print('Enter a command')

        if keyboard.is_pressed('w+space') | keyboard.is_pressed('W+space'):
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_MOS)
            print('Enter a command')

        if keyboard.is_pressed('e+space') | keyboard.is_pressed('E+space'):
            creator.create_joint_chamber_sb(SbCodes.JOINT_CHAMBER_SB_SAT)
            print('Enter a command')

        if keyboard.is_pressed('1+space'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS)
            print('Enter a command')

        if keyboard.is_pressed('2+space'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_MOS)
            print('Enter a command')

        if keyboard.is_pressed('3+space'):
            creator.create_pole_sb(SbCodes.POLE_SB_24_CLIENTS_SAT)
            print('Enter a command')

        if keyboard.is_pressed('a+space') | keyboard.is_pressed('A+space'):
            cable_manager.automate_cable_form(
                cable_template=CableCodes.CABLE_12_FO)
            print('Enter a command')

        if keyboard.is_pressed('s+space') | keyboard.is_pressed('S+space'):
            cable_manager.automate_cable_form(
                cable_template=CableCodes.CABLE_48_FO)
            print('Enter a command')

        if keyboard.is_pressed('d+space') | keyboard.is_pressed('D+space'):
            cable_manager.automate_cable_form(
                cable_template=CableCodes.CABLE_36_FO)
            print('Enter a command')

        if keyboard.is_pressed('h+space') | keyboard.is_pressed('H+space'):
            uprns = helper.scrape_uprns_from_map(cable_manager.driver)
            helper.scrape_uprn_from_cto_list(
                cable_manager.driver, uprn_list=uprns)
            print('Enter a command')

        if keyboard.is_pressed('t+space') | keyboard.is_pressed('T+space'):
            helper.delete_splitter(cable_manager.driver)
            print('Enter a command')


def handle_uprn_response() -> bool:
    handle_response = True

    print('Select clients?')
    while handle_response:
        if keyboard.is_pressed('y') | keyboard.is_pressed('Y'):
            handle_response = False
            print('Select clients?')
            return True
        if keyboard.is_pressed('n') | keyboard.is_pressed('N'):
            handle_response = False
            return False
