from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import csv

SCRAPERAPI_KEY = "YOUR_API_KEY_HERE"  # Replace with your ScraperAPI key
output_file = "cpsbc_Specialists.csv"

def create_driver_with_scraperapi():
    proxy = f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001"
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    #chrome_options.add_argument('--headless')  # Optional: remove this if you want to see the browser
    return webdriver.Chrome(service=Service(), options=chrome_options)

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # writer.writerow([
    #     "Title", "Description", "Price", "Location", "Pets Allowed?"
    #     ])
    writer.writerow([
    "Name", "Gender", "Languages", "registration_status", "registration_class", "practice_type", "certification", "degree info", "address", "phone", "fax"
    ])
        
    driver = webdriver.Chrome()
    driver.get("https://www.cpsbc.ca/public/registrant-directory")



    # Let the page load
    time.sleep(2)

    # Locate the input field and search for a name, e.g., "Smith"
    search_box = driver.find_element(By.ID, "edit-ps-last-name")
    search_box.send_keys("")
    search_box.send_keys(Keys.RETURN)
    time.sleep(20)

    counter = 0
    while counter < 1000:
        # Wait for search results to load
        time.sleep(5)

        # Scrape search results
        links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/public/registrant-directory/search-result/']")
        for link in links:
            print(link.get_attribute("href"))
        ############################+
        i = 0
        while True:
            result_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/public/registrant-directory/search-result/']")
            if i >= len(result_links):
                break  # Done with this page

            print(f"Clicking result {i+1}/{len(result_links)}")
            result_links[i].click()
            time.sleep(2)

            # Scrape info !!!!!!!!!!!!!!!
            name = driver.find_element(By.CSS_SELECTOR, "h1").text
            print("Name:", name)

            ##
            gender = "N/A"
            language = "N/A"

            try:
                # === Scrape Gender ===
                gender_span = driver.find_element(
                    By.XPATH,
                    '//div[contains(@class, "directory-profile--summary-info")]//label[strong[contains(text(), "Gender")]]/following-sibling::span'
                )
                gender_text = gender_span.text.strip()
                if gender_text in ["Male", "Female"]:
                    gender = gender_text
                print("Gender:", gender)
            except Exception:
                print("Gender not found")
                gender = "N/A"

            try:
                # === Scrape ALL Languages Spoken ===
                language_spans = driver.find_elements(
                    By.XPATH,
                    '//div[contains(@class, "directory-profile--summary-info")]//strong[contains(text(), "Languages spoken")]/following-sibling::span'
                )
                languages_list = [span.text.strip().strip(',') for span in language_spans if span.text.strip()]
                if languages_list:
                    languages = ", ".join(languages_list)
                print("Languages:", languages)
            except Exception:
                print("Languages not found")
                languages = "N/A"

            registration_status = "N/A"
            registration_class = "N/A"
            practice_type = "N/A"
            certification = "N/A"

            try:
                # === Registration Status ===
                status_elem = driver.find_element(By.XPATH, '//strong[contains(text(), "Registration status")]/following-sibling::span')
                registration_status = status_elem.text.strip()
            except Exception:
                print("Registration status not found")
                registration_status = "N/A"

            try:
                # === Registration Class ===
                class_elem = driver.find_element(By.XPATH, '//strong[contains(text(), "Registration class")]/following-sibling::span')
                registration_class = class_elem.text.strip()
            except Exception:
                print("Registration class not found")
                registration_class = "N/A"

            try:
                # === Practice Type ===
                practice_elem = driver.find_element(By.XPATH, '//strong[contains(text(), "Practice type")]/following-sibling::span')
                practice_type = practice_elem.text.strip()
            except Exception:
                print("Practice type not found")
                practice_type = "N/A"

            try:
                # === Certification ===
                cert_elem = driver.find_element(By.XPATH, '//strong[contains(text(), "Certification")]/parent::label/following-sibling::span')
                cert_lines = cert_elem.find_elements(By.XPATH, './/span')
                cert_texts = [line.text.strip() for line in cert_lines if line.text.strip()]
                if cert_texts:
                    certification = " ".join(cert_texts)
            except Exception:
                print("Certification not found")
                certification = "N/A"

            # Output all data
            print("Registration status:", registration_status)
            print("Registration class:", registration_class)
            print("Practice type:", practice_type)
            print("Certification:", certification)

            #Degree
            degree_info = "N/A"
            try:
                degree_div = driver.find_element(By.CLASS_NAME, "directory-profile__degree")
                spans = degree_div.find_elements(By.TAG_NAME, "span")
                # Get non-empty trimmed text and join with spaces
                parts = [span.text.strip() for span in spans if span.text.strip()]
                degree_info = " ".join(parts)
            except Exception:
                print("Degree info not found")
                degree_info = "N/A"

            print("Degree:", degree_info)

            #address
            try:
                # Find all elements with class "ml-1"
                ml1_elements = driver.find_elements(By.CLASS_NAME, "ml-1")
                
                # Loop through each one and filter out text that starts with "Certification"
                for el in ml1_elements:
                    text = el.text.strip()
                    if text and not text.startswith("Certification"):
                        # Clean up and format nested address spans (if applicable)
                        spans = el.find_elements(By.TAG_NAME, "span")
                        address_parts = [span.text.strip() for span in spans if span.text.strip()]
                        address = ", ".join(address_parts) if address_parts else text
                        break
                else:
                    address = "N/A"

            except Exception:
                address = "N/A"

            print("Address:", address)

            #phone and fax
            phone = "N/A"
            fax = "N/A"

            try:
                mb2_elements = driver.find_elements(By.CLASS_NAME, "mb-2")

                for el in mb2_elements:
                    text = el.text.strip()
                    if "Languages spoken" in text:
                        continue  # Skip language-related blocks

                    if "Phone:" in text:
                        try:
                            phone = el.find_element(By.TAG_NAME, "span").text.strip()
                        except:
                            pass

                    elif "Fax:" in text:
                        try:
                            fax = el.find_element(By.TAG_NAME, "span").text.strip()
                        except:
                            pass

            except Exception:
                pass

            print("Phone:", phone)
            print("Fax:", fax)

            ##
            writer.writerow([
            name, gender, languages, registration_status, registration_class, practice_type, certification, degree_info, address, phone, fax
            ])

            # Go back to results page
            driver.back()
            time.sleep(2)

            # Increase index
            i += 1

        ################################

        # Find and click the next-page button
        next_button = driver.find_element(By.CSS_SELECTOR, "a[aria-label='page-next']")
        next_button.click()


        counter = counter + 1



    driver.quit()
    time.sleep(1000)
    



    #REDDIT POST

#     The particular site I want to scrape is https://www.cpsbc.ca, because my employer requested me to. 
# However, this site does everything in its power to make it a pain to scrape; URL links of page numbers cannot be typed directly in the URL, and must be accessed by clicking like a normal person. 
# Even if I make my chromedriver click on the next page every time, my IP gets flagged and my code stops running. Even if I use a VPN, they find the FAKE IP and ban that too. 
# I considered using ScraperAPI, but that doesnt work either because of the combination of the two things I mentioned earlier. In the site, you cannot jump to a particular page, you have to painstakingly press the "next" button over and over until you get the page you want. Its for this reason that if I want the code to change IPs, I have to make a new chromedriver, and also make it catch up to what page the previous chromedriver was at. 
# Anyone got any advice to tackling this? Or would you say its downright impossible to scrape?