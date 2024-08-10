import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def download_image(url, folder_path, image_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_path, image_name), 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download image from {url}")
    except Exception as e:
        print(f"Exception occurred while downloading image from {url}: {e}")

def login_facebook(driver, email, password):
    driver.get("https://www.facebook.com")
    time.sleep(3)

    try:
        email_element = driver.find_element(By.ID, "email")
        email_element.send_keys(email)
        
        password_element = driver.find_element(By.ID, "pass")
        password_element.send_keys(password)
        
        password_element.send_keys(Keys.RETURN)
        time.sleep(5)

        if "login" in driver.current_url:
            print("Failed to log in. Please check your credentials.")
            driver.quit()
            exit()
    except Exception as e:
        print(f"Exception occurred during login: {e}")
        driver.quit()
        exit()

def get_profile_photos(driver, profile_url, folder_path):
    driver.get(profile_url)
    time.sleep(5)

    os.makedirs(folder_path, exist_ok=True)

    # Scroll down to load more photos
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find all image elements and their links
    photo_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'photo.php')]")

    photo_urls = [link.get_attribute("href") for link in photo_links]

    for index, photo_url in enumerate(photo_urls):
        try:
            driver.get(photo_url)
            time.sleep(5)
            image_element = driver.find_element(By.XPATH, "//img[contains(@src, 'scontent')]")
            image_url = image_element.get_attribute("src")
            download_image(image_url, folder_path, f"photo_{index}.jpg")
            time.sleep(2)  # Add a delay between downloads
        except Exception as e:
            print(f"Failed to download photo from {photo_url}: {e}")

if __name__ == "__main__":
    email = "email login facebook"
    password = "senha"
    profile_url = "link do perfil de fotos"
    folder_path = "caminho das fotos para salvar no computador"

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")  # Maximize the browser window on start
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    try:
        login_facebook(driver, email, password)
        get_profile_photos(driver, profile_url, folder_path)
    finally:
        driver.quit()
