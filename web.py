from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def find(browser, user,pwd):
    username = browser.find_element(By.ID, "username")
    username.clear()
    username.send_keys(user)
    password = browser.find_element(By.ID, "password")
    password.clear()
    password.send_keys(pwd)
    submit = browser.find_element(By.TAG_NAME,"button")
    submit.click()


username = ['Terminax', "Ruby", "Goodx45", "Instant24", "Goody"]
password = ['Terminax', "Ruby", "Goodx45", "Instant24", "Goody"]

def scrap():
    browser = webdriver.Chrome()
    browser.get("http://127.25.115.0:8080/signup")
    loop(browser)
    #time.sleep(20)
    browser.close()

def loop(browser):
    for i in range(len(username)):
        find(browser=browser,user=username[i], pwd=password[i])
        next = WDW(browser,10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        if 'Login' in next.text:
            print(next.text)
            find(browser=browser,user=username[i], pwd=password[i])
            browser.get("http://127.25.115.0:8080/signup")
            vn = WDW(browser,10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
            

if __name__ == "__main__":
    start = time.time()
    scrap()
    stop = time.time()
    time = float((stop - start))
    print("TIME FOR SCRAPING: ", time)
