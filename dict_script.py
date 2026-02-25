from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpiFilter=yes")  # replace with actual URL

# Wait a bit if necessary
driver.implicitly_wait(5)

records = []

# Find all record containers
record_containers = driver.find_elements(By.CSS_SELECTOR, "div.card-table-left")

for container in record_containers:
    record_dict = {}
    
    # Each field
    fields = container.find_elements(By.CSS_SELECTOR, "div.card-view")
    
    for field in fields:
        # Extract key and value
        key = field.find_element(By.CSS_SELECTOR, "div.title span").text.strip()
        value = field.find_element(By.CSS_SELECTOR, "div.value span").text.strip()
        record_dict[key] = value
    
    records.append(record_dict)

driver.quit()

import pandas as pd
import numpy as np

# Example list of dictionaries

# Convert list of dicts to DataFrame
df = pd.DataFrame(records)

# Replace missing values with NaN (optional, pandas already does this by default)
df = df.fillna(np.nan)

# Save to CSV
df.to_csv("output.csv", index=False)

print(df)

