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
options.add_argument

def scrap():
    browser = webdriver.Chrome(options=options)
    browser.get('https://tg-app.memefi.club/#tgWebAppData=query_id%3DAAEzwH4pAwAAADPAfinCxPQi%26user%3D%257B%2522id%2522%253A7138623539%252C%2522first_name%2522%253A%2522A.I%2522%252C%2522last_name%2522%253A%2522INSTARAJ%2522%252C%2522username%2522%253A%2522Instaraj25%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1725886260%26hash%3D60f4b8170b209dd8d41f2ab00527147e326e0350af73656fedc04e924da4e1a2&tgWebAppVersion=7.8&tgWebAppPlatform=android&tgWebAppThemeParams=%7B"bg_color"%3A"%23212d3b"%2C"section_bg_color"%3A"%231d2733"%2C"secondary_bg_color"%3A"%23151e27"%2C"text_color"%3A"%23ffffff"%2C"hint_color"%3A"%237d8b99"%2C"link_color"%3A"%235eabe1"%2C"button_color"%3A"%2350a8eb"%2C"button_text_color"%3A"%23ffffff"%2C"header_bg_color"%3A"%23242d39"%2C"accent_text_color"%3A"%2364b5ef"%2C"section_header_text_color"%3A"%2379c4fc"%2C"subtitle_text_color"%3A"%237b8790"%2C"destructive_text_color"%3A"%23ee686f"%2C"section_separator_color"%3A"%230d1218"%7D')
    try:
        time.sleep(25)
        earn = browser.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[3]/div/div/canvas')
        if earn:
            print("Earn")
        while True:
            earn.click()
    except Exception as E:
        print("Error")

    time.sleep(50)    
    browser.close()

scrap()