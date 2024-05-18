


# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

import os
import csv
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------
# Configure logging
# ---------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------------------------
# Function to clear the terminal
# ---------------------------------
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------------------------------
# Function to fetch and parse table using Selenium
# ---------------------------------
def fetch_table_data_selenium(url, xpath):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Path to the chromedriver executable
    chrome_driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')

    # Initialize the WebDriver
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    logging.info(f"Opening URL: {url}")
    driver.get(url)
    
    headers, data = [], []
    try:
        # Wait for the table to be present
        logging.info(f"Waiting for the table to be present with XPath: {xpath}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        table = driver.find_element(By.XPATH, xpath)
        
        logging.info("Extracting headers")
        headers = [header.text for header in table.find_elements(By.XPATH, ".//tr/th")]
        headers.append('Link')  # Add an extra header for the link
        logging.debug(f"Headers found: {headers}")
        
        logging.info("Extracting rows")
        rows = table.find_elements(By.XPATH, ".//tr")[1:]  # Skip header row
        for row in rows:
            row_data = []
            cells = row.find_elements(By.XPATH, ".//td")
            for idx, cell in enumerate(cells):
                if idx == 2:  # Third column (Município)
                    link_element = cell.find_element(By.XPATH, "./a")
                    link = link_element.get_attribute("href") if link_element else ""
                    municipio_name = link_element.text if link_element else cell.text.strip()
                    row_data.append(municipio_name)
                    row_data.append(link)  # Append the link after the text
                else:
                    cell_data = cell.text.strip()
                    row_data.append(cell_data)
            data.append(row_data)
        logging.debug(f"Data rows extracted: {len(data)}")
    except Exception as e:
        logging.error(f"Error: {e}")
        logging.error("Page source for debugging:")
        logging.error(driver.page_source)  # Log the page source for debugging
    finally:
        driver.quit()
    
    return headers, data

# ---------------------------------
# Function to save data to CSV
# ---------------------------------
def save_to_csv(headers, data, file_path):
    logging.info(f"Saving data to CSV file: {file_path}")
    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        writer.writerows(data)
    logging.info("Data saved successfully")

# ---------------------------------
# Main function to execute scraper
# ---------------------------------
def main():
    clear_terminal()
    url = 'https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Portugal_por_popula%C3%A7%C3%A3o'
    xpath = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/center/table'
    headers, data = fetch_table_data_selenium(url, xpath)
    if headers and data:
        save_to_csv(headers, data, 'municipalities_population.csv')
    else:
        logging.error("Failed to fetch data from the webpage.")

if __name__ == "__main__":
    main()





