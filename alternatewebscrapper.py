from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import bs4 as BeautifulSoup
import math

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

#CSVfile to save data
output_file = "cpso_doctors5.csv"

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        "CPSO number", "Name", "Active?", "Active as of", "Medschool", "Gender", 
        "languages", "Primary location", "Alternatelocation 1", "Alternatelocation 2",
        "Alternatelocation 3", "Alternatelocation 4", "Phone Number", "Fax Number", "Specialty"
        ])
        
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    for cpsonum in range(170000, 200000, 1):
        
        # Open the page
        url = f"https://register.cpso.on.ca/physician-info/?cpsonum={cpsonum}"
        driver.get(url)
        print("reading: " + str(cpsonum))

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Wait for JavaScript to load the content
        #time.sleep(1)

        # Use XPath to extract the doctor name
        try:
            doctor_name = driver.find_element(By.XPATH, '//*[@id="banner-content"]/div[1]/h1').text
            print("Doctor Name:", doctor_name)
        except Exception as e:
            doctor_name = "N/A"
            print("Doctor name not found.")
            #print("Error:", str(e))

        if doctor_name == "N/A":
            #driver.quit()
            continue

        # Use XPath to extract the doctors activity
        try:
            active = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[2]/div[1]/div[2]').text
            print("Active:", active)
        except Exception as e:
            active = "N/A"
            print("not found.")
            #print("Error:", str(e))

        # Use XPath to extract the doctors activity "as of"
        try:
            activeasof = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[2]/div[2]/div/span/span').text
            print("Active:", activeasof)
        except Exception as e:
            activeasof = "N/A"
            print("not found.")
            #print("Error:", str(e))


        #Alternate version of the code that is faulty.
        # Use XPath to extract the doctors medical school
        # time.sleep(3)
        # try:
        #     medschool = driver.find_element(By.XPATH, '//*[@id="general-information"]/div/div[1]/div[2]/span[2]').text
        #     print("Medschool:", medschool)
        # except Exception as e:
        #     medschool = "N/A"
        #     print("not found.")
        #     #print("Error:", str(e))
        # try:
        #     # Wait for the element to be visible
        #     medschool_elem = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/span[2]'))
        #     )
        #     medschool = medschool_elem.text.strip()
        #     print("Medschool:", medschool)
        # except Exception as e:
        #     print("Medschool not found.")
        #     # print("Error:", str(e))
        
        # try:
        #     element = WebDriverWait(driver, 10).until(
        #         EC.visibility_of_element_located((By.CLASS_NAME, 'scrp-education-value'))
        #     )
        #     print("Element found")
        #     print("Text:", element.text.strip())
        # except Exception as e:
        #     print("Element not found:", e)

        # response = requests.get(url, headers=headers)
        # soup = BeautifulSoup(response.content, "html.parser")
        # # Find the element
        # education = soup.find("span", class_="scrp-education-value")

        # # Print result
        # if education:
        #     print(education.get_text(strip=True))
        # else:
        #     print("Element not found")



        #education
        education_text = driver.execute_script(
            "return document.querySelector('.scrp-education-value')?.textContent.trim();"
        )

        print("Medschool:", education_text)

        # # Use XPath to extract the doctors gender
        # try:
        #     gender = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/nav/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/span[2]').text
        #     print("Active:", gender)
        # except Exception as e:
        #     gender = "N/A"
        #     print("not found.")
        #     #print("Error:", str(e))

        #gender
        gender_text = driver.execute_script(
            "return document.querySelector('.scrp-gender-value')?.textContent.trim();"
        )
        print("gender:", gender_text)

        #language
        language_text = driver.execute_script(
            "return document.querySelector('.scrp-laguage-value')?.textContent.trim();"
        )
        print("languages:", language_text)

        #location
        location_text = driver.execute_script(
            "return document.querySelector('.scrp-practiceaddress-value')?.textContent.trim();"
        )
        print("location:", location_text)

        location_list = driver.execute_script("""
            return Array.from(document.querySelectorAll('.scrp-practiceaddress-value'))
                        .map(el => el.textContent.trim())
                        .filter(text => text.length > 0);
        """)


        numberoflocations = math.floor(len(location_list) / 4)
        truelistoflocations = []

        for n in range(0, int(numberoflocations), 1):
            truelistoflocations.append(location_list[n])
        
        for n in range(6):
            truelistoflocations.append("N/A")

        # Print all location entries
        for i, location in enumerate(location_list, 1):
            print(f"Location {i}: {location}")
        
        #note: repeats the list of locations 4 times.

        #phone
        phone_text = driver.execute_script(
            "return document.querySelector('.scrp-phone-value')?.textContent.trim();"
        )
        print("phone:", phone_text)     

        #fax
        fax_text = driver.execute_script(
            "return document.querySelector('.scrp-fax-value')?.textContent.trim();"
        )
        print("fax:", fax_text)   

        #specialty
        specialty_text = driver.execute_script(
            "return document.querySelector('.scrp-specialtyname-value')?.textContent.trim();"
        )
        print("specialty:", specialty_text)   

        #finally adding data to CSV
        writer.writerow([
        cpsonum, doctor_name, active, activeasof, education_text, gender_text, 
        language_text, truelistoflocations[0], truelistoflocations[1], truelistoflocations[2],
        truelistoflocations[4], truelistoflocations[5], phone_text, fax_text, specialty_text
        ])
        # 
        # Close the browser
    driver.quit()
