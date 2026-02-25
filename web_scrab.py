from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# Setup
driver = webdriver.Chrome()
driver.get("https://selenium-python.readthedocs.io/")

# Wait for the table to load
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "tablebg"))
)

# Prepare CSV
with open("sebi_fpi_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["FPI Name", "Registration Number", "Category", "Country", "Date"])

    while True:
        # Parse current page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="tablebg")
        rows = table.find_all("tr")[1:]  # Skip header

        for row in rows:
            cols = row.find_all("td")
            data = [col.text.strip() for col in cols]
            writer.writerow(data)

        # Try to click "Next"
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            time.sleep(2)
        except:
            break

driver.quit()