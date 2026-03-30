import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def download_js_images(url, folder_name="Downloaded Manga"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 1. Setup Chrome in "headless" mode (runs in background)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        
        # 2. Handle Lazy Loading: Scroll down to trigger image loads
        # This scrolls the page 3 times, waiting for content to load
        for _ in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) 

        # 3. Find the elements
        # Selenium uses find_elements to get a list of objects
        img_elements = driver.find_elements(By.CSS_SELECTOR, "img.fit-w")

        print(f"Found {len(img_elements)} matching images.\n")

        for i, img in enumerate(img_elements, 1):
            # Print the FULL HTML tag as requested
            full_tag = img.get_attribute('outerHTML')
            print(f"Downloading from tag: {full_tag}")

            img_url = img.get_attribute('src')
            if not img_url:
                continue

            # 4. Download the file
            try:
                img_data = requests.get(img_url).content
                filename = f"{i}.jpg"
                filepath = os.path.join(folder_name, filename)

                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"Successfully saved as {filename}\n")
            except Exception as e:
                print(f"Failed to save image {i}: {e}")

    finally:
        driver.quit()

# Usage
print("Welcome to Comix Manga Downloader!\nPlease go to the desired chapter or volume, copy the link such as \'https://comix.to/title/69l57-chainsaw-man/8844787-chapter-232\', and paste it here!")
target_url = input("Paste URL and press enter: ")
download_js_images(target_url)