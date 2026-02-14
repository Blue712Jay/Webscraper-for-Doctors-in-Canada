from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up browser
driver = webdriver.Chrome()
driver.get("https://register.cpso.on.ca/physician-info/?cpsonum=101000")

education_text = driver.execute_script(
    "return document.querySelector('.scrp-education-value')?.textContent.trim();"
)

print("Education:", education_text)
driver.quit()