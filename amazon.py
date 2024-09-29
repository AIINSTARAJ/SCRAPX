from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


service = Service()
options = Options()
options.add_argument("user-data-dir = C:\\Users\\USER\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")

def scrap():
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.amazon.com/s?k=computers&ref=nb_sb_noss")
    time.sleep(50)    
    browser.close()

scrap()