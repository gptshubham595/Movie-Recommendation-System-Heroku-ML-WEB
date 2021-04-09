#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH="chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.google.com/search?q=avatar&tbm=isch")

time.sleep(3)


# try:
span=driver.find_element_by_class_name("rg_i")	
print(span.get_attribute("src"))
	
# except :
	# driver.quit()




 #closes tab







