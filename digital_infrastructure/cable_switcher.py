from cProfile import label
from encodings import search_function
from pydoc import Helper
from unittest.loader import VALID_MODULE_NAME
from cable_manager import CableManager
from constants import CableCodes, JointBoxCodes, SbCodes, Towns
from component_creator import ComponentCreator
from remote_connection import RemoteConnection
from helpers import Helpers
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


if __name__ == '__main__':

    WORKING_TOWN = Towns.CARLTON
    WORKING_CLUSTER = 8

    ORIGIN_ID_XPATH = '//*[@id="frmcable"]/form/article/div[2]/app-location/apx-field1[2]/div/div/div[1]/app-find-closest-element/select'
    DEST_ID_XPATH = '//*[@id="frmcable"]/form/article/div[2]/app-location/apx-field1[2]/div/div/div[2]/app-find-closest-element/select'

    driver = RemoteConnection.setup_connection()

    cable_list = [
        'CHT-CL005-J13452-SB40631',
        'CHT-CL005-J13455-SB40637',
        'CHT-CL005-J13455-SB40639',
        'CHT-CL005-J13456-SB40645',
        'CHT-CL005-J13457-SB40647',
        'CHT-CL005-J13457-SB40648',
        'CHT-CL005-J13457-SB40650',
        'CHT-CL005-J13462-SB40649',
        'CHT-CL005-J13464-SB40660',
        'CHT-CL005-J13464-SB40703',
        'CHT-CL005-J13473-SB40699',
        'CHT-CL005-SB40621-SB40624',
        'CHT-CL005-SB40627-SB40628',
        'CHT-CL005-SB40628-SB40629',
        'CHT-CL005-SB40632-SB40633',
        'CHT-CL005-SB40637-SB40638',
        'CHT-CL005-SB40645-SB40643',
        'CHT-CL005-SB40650-SB40651',
        'CHT-CL005-SB40660-SB40661',
        'CHT-CL005-SB40670-SB40671',
        'CHT-CL005-SB40672-SB40666',
        'CHT-CL005-SB40674-SB40675',
        'CHT-CL005-SB40676-SB40677',
        'CHT-CL005-SB40678-SB40679',
        'CHT-CL005-SB40680-SB40678',
        'CHT-CL005-SB40687-SB40686',
        'CHT-CL005-SB40687-SB40688',
        'CHT-CL005-SB40689-SB40690',
        'CHT-CL005-SB40689-SB40691',
        'CHT-CL005-SB40701-SB40702',
        'CHT-CL005-SB40701-SB40704',
        'CHT-CL005-SB40711-SB40676',
        'CHT-CL005-SB40712-SB40674',
        'CHT-CL005-SB40715-SB40714']

    def get_cable_id(origin, destination):

        return f'CHT-CL006-{origin}-{destination}'

    def change_cable_label():

        id_field = driver.find_element(
            by=By.CSS_SELECTOR, value="apx-field1[label='Id'] input")
        old_id = id_field.get_attribute('value')
        id_field.clear()

        select_origin = Select(driver.find_element(
            by=By.XPATH, value=ORIGIN_ID_XPATH))
        select_dest = Select(driver.find_element(
            by=By.XPATH, value=DEST_ID_XPATH))

        origin = ''
        destination = ''

        for i in range(1, len(select_origin.options)):
            selection = select_origin.options[i].text.split(':')
            if len(selection) == 1:
                select_origin.select_by_index(i)
                origin = select_origin.options[i].text.split(' ')[0]
                break

        for i in range(1, len(select_dest.options)):
            selection = select_dest.options[i].text.split(':')
            if len(selection) == 1:
                select_dest.select_by_index(i)
                destination = select_dest.options[i].text.split(' ')[0]
                break

        # input cable id
        id_container = driver.find_element(
            by=By.XPATH, value='//*[@id="frmcable"]/form/article/div[2]/apx-field1[1]/div/div/input')
        id = get_cable_id(origin=origin, destination=destination)
        id_container.clear()
        id_container.send_keys(id)

        save_btn = driver.find_element(
            by=By.XPATH, value='//*[@id="frmcable"]/form/footer/button[1]').click()
        WebDriverWait(driver, 600).until_not(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="frmcable"]/form/article/div[2]/apx-field1[1]/div/div/input')))

    for label in cable_list:

        buscador = driver.find_element(by=By.NAME, value='txtbuscador')
        buscador.clear()
        buscador.send_keys(label)

        btn_wait = WebDriverWait(driver, 600).until(
            EC.element_to_be_clickable((By.ID, 'btBuscar')))
        search_btn = driver.find_element(by=By.ID, value='btBuscar').click()
        search_wait = WebDriverWait(driver, 600).until_not(
            EC.visibility_of_element_located((By.ID, 'lSearching')))
        cable = WebDriverWait(driver, 600).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="buscadorResult"]/div[1]/ul/li[2]')))
        cable = driver.find_element(
            by=By.XPATH, value='//*[@id="buscadorResult"]/div[1]/ul/li[2]')
        cable.click()

        popup = WebDriverWait(driver, 600).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="map"]/div[1]/div[6]/div/div[1]/div/div[1]/div/div/div[2]/div/a')))
        popup = driver.find_element(
            by=By.XPATH, value='//*[@id="map"]/div[1]/div[6]/div/div[1]/div/div[1]/div/div/div[2]/div/a').click()

        id_wait = WebDriverWait(driver, 600).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "apx-field1[label='Id']")))

        change_cable_label()
