from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions


# https://www.google.com/maps/dir/43.203014,23.547599/42.6975,23.3241/
# maps_time_address = maps_const + f"{current_location}/{str_stadium_coordinates}"
PATH = "C:\Program Files (x86)\chromedriver.exe"
op = webdriver.ChromeOptions()
op.add_argument('headless')

driver = webdriver.Chrome(PATH, options=op)

maps_time_address = "https://www.bing.com/maps/"

driver.get(maps_time_address)

# ACCEPTING COOKIES
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#bnp_btn_accept"))).click()

directions = driver.find_element_by_class_name("directionsIcon")
directions.click()
time.sleep(2)

start = driver.find_element_by_css_selector(".start+ input")
end = driver.find_element_by_css_selector(".end+ input")

start.send_keys('43.203014,23.547599')
end.send_keys('42.6975,23.3241')

go_btn = driver.find_element_by_class_name("dirBtnGo.commonButton")
go_btn.click()

time_minutes = None
time_hours = None
while time_hours is None:
    try:
        time_hours = driver.find_element_by_class_name('drHours')
        time_minutes = driver.find_element_by_class_name('drMins')
    except selenium.common.exceptions.NoSuchElementException:
        pass

travel_time = f"{time_hours.text} h: {time_minutes.text} min"
print(travel_time)

# Cookies --> bnp_btn_reject
