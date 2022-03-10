from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class RemoteConnection: 
    
    def setup_connection():
        #setup options
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        #create driver
        driver = webdriver.Chrome(options=chrome_options)

        return driver
