from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import time

# Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpiFilter=yes")

records = []

def scrape_current_page():
    """Scrape all records on the current page."""
    record_containers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card-table-left"))
    )

    for container in record_containers:
        record_dict = {}
        fields = container.find_elements(By.CSS_SELECTOR, "div.card-view")

        for field in fields:
            try:
                key = field.find_element(By.CSS_SELECTOR, "div.title span").text.strip()
            except:
                key = None
            try:
                value = field.find_element(By.CSS_SELECTOR, "div.value span").text.strip()
            except:
                value = np.nan

            if key:
                record_dict[key] = value

        records.append(record_dict)

# Loop through all pages using "Next" button
while True:
    scrape_current_page()

    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Next']"))
        )
        next_button.click()
        time.sleep(2)  # wait for page to load
    except:
        print("Reached last page.")
        break

# Close browser
driver.quit()

# Convert to DataFrame and save to CSV
df = pd.DataFrame(records)
df = df.fillna(np.nan)  # ensure missing fields are NaN
df.to_csv("sebi_records.csv", index=False)
print("Data saved to sebi_records.csv")
