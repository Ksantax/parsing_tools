import bs4
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

__module_path = os.path.dirname(__file__)
__previous_dir_path = __module_path[0: __module_path.rfind("\\")+1]

MODELS_JSON_PATH = __module_path+'\\static\\drom_auto_models.json'
CHROME_DRIVER_PATH = __previous_dir_path+'\\chromedriver\\chromedriver.exe'

op = webdriver.ChromeOptions()
#op.add_argument('headless')

driver = webdriver.Chrome(options=op)
driver.get('https://auto.drom.ru/all/')

el1 = driver.find_element(By.CSS_SELECTOR, 'div.css-75hx9m.e1a8pcii0 input')
el1.click()

