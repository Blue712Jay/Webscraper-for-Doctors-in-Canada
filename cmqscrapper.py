"Link: https://www.cmq.org/en/directory/physicians?number=10000&lastname=&firstname=&specialty=0&city=&unlisted=false"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import requests
import bs4 as BeautifulSoup
import math


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

def random_delay():
    delay = random.uniform(2, 5)
    r = random.randint(1, 100)  
    if r == 1:
        time.sleep(7)
    else:
        time.sleep(delay)

def extract_sections(data):
    # Ordered list of all possible keywords
    keywords = [
        'Permit number:', 'Sex:', 'Permit type:', 'Status:', 'Disciplinary file(s):', 
        'Insurance:', 'Specialty(ies):',
        'Activity(ies):', 'Authorization(s):', 'Address:', 'Phone:', 'Fax:',
        'First registration on the roll of the Collège:', 'Date of issuance of the permit:',
        "Issue date of the specialist's certificate(s):", 'History of the right to practice:',
        'Print'
    ]

    # For faster lookup
    keyword_set = set(keywords)

    # Initialize dictionary with all keywords as keys
    result = {key: "" for key in keywords if key != 'Print'}

    current_key = None

    for item in data:
        if item in keyword_set:
            if item == 'Print':
                current_key = None
            else:
                current_key = item
        else:
            if current_key:
                if result[current_key]:
                    result[current_key] += " " + item
                else:
                    result[current_key] = item

    return result

#CSVfile to save data
output_file = "cmq_doctors03.csv"

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Name',
        'Permit number:', 'Sex:', 'Permit type:', 'Status:', 'Disciplinary file(s):',
        'Insurance:', 'Specialty(ies):',
        'Activity(ies):', 'Authorization(s):', 'Address:', 'Phone:', 'Fax:',
        'First registration on the roll of the Collège:', 'Date of issuance of the permit:',
        "Issue date of the specialist's certificate(s):", 'History of the right to practice:'
    ])
        
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    for cmqnum in range(4873, 10000, 1):
        cmqnum = f"{cmqnum:05n}"

        
        # Open the page
        url = f"https://www.cmq.org/en/directory/physicians?number={cmqnum}&lastname=&firstname=&specialty=0&city=&unlisted=false"
        driver.get(url)
        print("reading: " + str(cmqnum))
        
        time.sleep(3)


        
        print("clicking:")
        try:
            driver.find_elements(By.CSS_SELECTOR, "td.u-text-right")[0].click()
        except Exception as e:
            print("Doesn't exist")
            continue
        random_delay()
            

        WebDriverWait(driver, 600).until(
            lambda d: any(
                e.text.strip() and e.text.strip() != "Member's history"
                for e in d.find_elements(By.XPATH, '//h5[@data-v-84ff2fd3]')
            )
        )

        #name
        try:
            # Find all <h5> elements with the data-v attribute
            h5_elements = driver.find_elements(By.XPATH, '//h5[@data-v-84ff2fd3]')
            
            name_text = "N/A"  # Default if not found
            for elem in h5_elements:
                text = elem.text.strip()
                if text and text != "Member's history":
                    name_text = text
                    break  # Stop after finding the first valid name
            if name_text == "N/A":
                print("oh no")
                exit()
            print("Name:", name_text)
        except Exception as e:
            print("Could not scrape the name:", e)
            name_text = "N/A"
            continue

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//span[@data-v-84ff2fd3]'))
        )



        spans = driver.find_elements(By.XPATH, '//span[@data-v-84ff2fd3]')

        # Extract text content, skipping any empty strings
        texts = [s.text.strip() for s in spans if s.text.strip()]

        print("Scraped texts:", texts)

        dictionaryofinfo = extract_sections(texts)

        

        #finally adding data to CSV
        writer.writerow([
        name_text,
        dictionaryofinfo['Permit number:'], dictionaryofinfo['Sex:'], dictionaryofinfo['Permit type:'], dictionaryofinfo['Status:'], dictionaryofinfo['Disciplinary file(s):'],
        dictionaryofinfo['Insurance:'], dictionaryofinfo['Specialty(ies):'],
        dictionaryofinfo['Activity(ies):'], dictionaryofinfo['Authorization(s):'], (dictionaryofinfo['Address:']).replace("\n", " "), dictionaryofinfo['Phone:'], dictionaryofinfo['Fax:'],
        dictionaryofinfo['First registration on the roll of the Collège:'], dictionaryofinfo['Date of issuance of the permit:'],
        dictionaryofinfo["Issue date of the specialist's certificate(s):"], dictionaryofinfo['History of the right to practice:']
        ])
        # 

        
        
    time.sleep(1000)
    driver.quit()
