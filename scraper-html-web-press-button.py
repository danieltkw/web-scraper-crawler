



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# -----
# Initialize the web driver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://anmp.pt/municipios/municipios/contactos-camaras-municipais/")
    return driver

# -----
# Close potential overlays (e.g., cookie notices)
def close_overlays(driver):
    try:
        # Close cookie notice if it appears
        cookie_notice = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cn-close-notice"))
        )
        cookie_notice.click()
        time.sleep(1)
    except Exception as e:
        print("No cookie notice found or error closing it:", e)

# -----
# Click the "Ver mais" button until no more buttons are found
def click_ver_mais(driver):
    wait = WebDriverWait(driver, 10)
    while True:
        try:
            ver_mais_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-original='Ver mais']"))
            )
            ver_mais_button.click()
            time.sleep(2)  # Adding delay to ensure content loads
        except Exception as e:
            print("No more 'Ver mais' buttons to click or error encountered:", e)
            break

# -----
# Extract city information from the page source
def extract_city_info(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cities = soup.find_all("div", class_="contact-001-content")
    city_info = []
    for city in cities:
        try:
            name = city.find_previous_sibling("div").text.strip()
            address = city.find("div", class_="content").text.strip()
            map_link = city.find("a", class_="buttonMap")["href"]
            president = city.find("div", class_="item general-content").text.strip().split(":")[1].strip()
            phone = city.find("a", href=lambda href: href and "tel:" in href).text.strip()
            fax = city.find_all("a", href=lambda href: href and "tel:" in href)[1].text.strip()
            email = city.find("a", href=lambda href: href and "mailto:" in href).text.strip()
            website = city.find("a", text="consultar website")["href"]

            # <a href="http://www.cm-abrantes.pt" target="_blank">consultar website</a>
            # <a href="http://www.google.com/maps/place/39.463010, -8.197883" target="_blank" class="buttonMap">[ver no mapa]</a>


            # Print the captured information to the terminal
            print(f"Captured: {name}, {address}, {map_link}, {president}, {phone}, {fax}, {email}, {website}")

            city_info.append({
                "name": name,
                "address": address,
                "map_link": map_link,
                "president": president,
                "phone": phone,
                "fax": fax,
                "email": email,
                "website": website
            })
        except Exception as e:
            print(f"Error extracting city info: {e}")

    return city_info

# -----
# Save city information to a CSV file
def save_to_csv(city_info):
    with open("city_info.csv", "w", newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ["name", "address", "map_link", "president", "phone", "fax", "email", "website"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for info in city_info:
            writer.writerow(info)

# -----
# Main function to run the script
def main():
    driver = init_driver()
    try:
        # Wait until the page is fully loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "accordion")))
        close_overlays(driver)  # Close potential overlays
        click_ver_mais(driver)
        city_info = extract_city_info(driver)
        save_to_csv(city_info)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()







# ---------------------------------