from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# create a Chrome browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# open a website
driver.get("https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpiFilter=yes")

elements = driver.find_elements(By.CLASS_NAME, "fixed-table-body")




driver.quit()
