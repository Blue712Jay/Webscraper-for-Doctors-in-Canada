
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

output_file = "cpsa_doctorstest.csv"

# Read CSV containing a column named 'url'
links_df = pd.read_csv("links_combined.csv")  # CSV must have a column 'url'

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow([
        "url", "Name", "Preferred Name", "Registration Number", "Address", "Postal Code", "Phone Number", "fax", "Languages", "Gender", 
        "Practice Disciplines", "Specialties", "Membership Status", "Conditions on Practice Permit"
            ])
    
    # Start Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    trigger = True

    for index, row in links_df.iterrows():
        url = row['url']
        print(f"Visiting {url}...")
        try:
            driver.get(url)
        except Exception as e:
            print("Retrying...")
            driver.quit()
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            time.sleep(20)
            driver.get(url)

        if trigger:
            driver.get("https://search.cpsa.ca/PhysicianProfile?e=b290d833-c037-4a67-bc41-2731db88e372&i=4002")
            trigger = False
        


        #names
        try:
            # Wait until the <h2> element containing the names is visible (max 60s wait)
            h2_element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "h2"))
            )

            # Extract full name (before the <span>)
            full_name = h2_element.text.split("(Preferred")[0].strip()

            # Extract preferred name (inside <span class="prefName">)
            preferred_name_element = h2_element.find_element(By.CLASS_NAME, "prefName")
            preferred_name = preferred_name_element.text.replace("(Preferred Name:", "").replace(")", "").strip()
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            full_name= ""
            preferred_name = ""

        #reg number
        try:
            number_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.medium-8.columns p"))
            )

            license_number = number_element.text.strip()
        except Exception as e:
            print("No number")
            license_number = "N/A"
            pass

        try:
            # Wait for the third occurrence of div.medium-8.columns
            address_block = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.medium-8.columns"))
            )[2]  # zero-indexed, so [2] = 3rd occurrence

            # Grab all <p> tags inside this block
            address_parts = [p.text.strip() for p in address_block.find_elements(By.TAG_NAME, "p") if p.text.strip()]

            if len(address_parts) >= 4:
                # 3rd last = phone number
                phone_number_raw = address_parts[-3]
                # 4th last = city
                postal_code = address_parts[-4]
                # everything before that = address
                address_only = " ".join(address_parts[:-4])
            else:
                phone_number_raw = " "
                postal_code = ""
                city = ""
                address_only = " "
            if "\n" in phone_number_raw:
                parts = phone_number_raw.split("\n", 1)  # split only once
                phone_number = parts[0].strip()
                fax = parts[1].strip()
            else:
                phone_number = phone_number_raw.strip()
                fax = ""

            # Put them together if you want a full string
            full_address = f"{address_only}, {postal_code}" if postal_code else address_only
        except:
            postal_code = ""
            phone_number = ""
            fax = ""

        
        index = 3
        try:
            # Find the 4th occurrence of "medium-8 columns"
            languages_div = driver.find_elements(By.CLASS_NAME, "medium-8.columns")[index]  # index 3 = 4th
            languages_text = languages_div.find_element(By.TAG_NAME, "p").text.strip()

            # Split into list of languages
            languages = [lang.strip() for lang in languages_text.split(",")]

            # Optional: keep them as a single string if you don’t want a list
            languages_str = ", ".join(languages)
            if languages_str == "Female" or languages_str == "Male":
                languages_str = ""
            else:
                index = index + 1

        except:
            languages_str = ""
            pass


        try:
            # Find the 5th occurrence of "medium-8 columns"
            gender_div = driver.find_elements(By.CLASS_NAME, "medium-8.columns")[index]  # index 4 = 5th
            gender = gender_div.find_element(By.TAG_NAME, "p").text.strip()
        except:
            gender = ""
            pass
        index = index + 1

        try:
            # Find the 6th occurrence of "medium-8 columns"
            discipline_div = driver.find_elements(By.CLASS_NAME, "medium-8.columns")[index]  # index 5 = 6th
            discipline = discipline_div.find_element(By.TAG_NAME, "p").text.strip()
        except:
            discipline = ""
            pass
        index = index + 1

        try:
            # Find the 7th occurrence of "medium-8 columns"
            specialties_div = driver.find_elements(By.CLASS_NAME, "medium-8.columns")[index]  # index 6 = 7th
            specialties = specialties_div.find_element(By.TAG_NAME, "p").text.strip()
        except:
            specialties = ""
            pass
        index = index + 1

        try:
            # Find the 8th occurrence of "medium-8 columns"
            membership_status_div = driver.find_elements(By.CLASS_NAME, "medium-8.columns")[index]  # index 7 = 8th
            membership_status = membership_status_div.find_element(By.TAG_NAME, "p").text.strip()
        except:
            membership_status = ""
            pass
        index = index + 1

        try:
            # Find the 9th occurrence of "medium-8 columns"
            conditions_div = driver.find_elements(By.CLASS_NAME, "medium-8.columns")[index]  # index 8 = 9th
            conditions = conditions_div.find_element(By.TAG_NAME, "p").text.strip()
        except:
            conditions = ""
            pass
        index = index + 1




        
        writer.writerow([
        url, full_name, preferred_name, license_number, address_only, postal_code, phone_number, fax, languages_str, gender, 
       discipline, specialties, membership_status, conditions
            ])
        
        #print("TEST")
        

        



driver.quit()
