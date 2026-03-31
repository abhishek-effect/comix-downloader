import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_manga_slicing(url, folder_name="manga_download"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': url
    }

    # 1. Selenium to grab the first loaded image
    print("Launching browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        first_img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.fit-w")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        base_src = first_img_element.get_attribute("src")
        print(f"Base tag found: {first_img_element.get_attribute('outerHTML')}")
        
    except Exception as e:
        print(f"Error: {e}")
        return
    finally:
        driver.quit()

    # 2. Get total pages from spans
    progress_div = soup.find('div', class_=lambda x: x and 'progress-line' in x)
    total_pages = len(progress_div.find_all('span')) if progress_div else 0
    
    if total_pages == 0:
        print("Could not determine page count.")
        return

    # 3. The Slicing Logic
    # Instead of rsplit, we find the last '/' and keep everything before it
    full_base_src = urljoin(url, base_src)
    last_slash_index = full_base_src.rfind('/')
    base_url_path = full_base_src[:last_slash_index] # Everything UP TO the last slash

    print(f"Targeting {total_pages} pages using path: {base_url_path}\n")

    # 4. Download Loop
    for i in range(1, total_pages + 1):
        page_num = str(i).zfill(2)
        # Construct URL: Path + / + 01 + .webp
        current_img_url = f"{base_url_path}/{page_num}.webp"
        
        try:
            img_res = requests.get(current_img_url, headers=headers, timeout=15)
            
            if img_res.status_code == 200:
                filename = f"{i}.webp"
                filepath = os.path.join(folder_name, filename)

                with open(filepath, 'wb') as f:
                    f.write(img_res.content)
                
                print(f"[{i}/{total_pages}] Saved: <img class='fit-w' src='{current_img_url}'>")
            else:
                print(f"[{i}/{total_pages}] Failed: HTTP {img_res.status_code}")
                
        except Exception as e:
            print(f"Error on page {i}: {e}")

    print(f"\nTask Finished! Files in: {os.path.abspath(folder_name)}")
    print("Created by abhishek-effect\nVisit github.com/abhishek-effect for more")

# --- RUN ---
print("Welcome to Comix Manga Downloader!\nPlease go to the desired chapter or volume, copy the link such as \'https://comix.to/title/69l57-chainsaw-man/8844787-chapter-232\', and paste it here!")
target_url = None
while target_url != "Q":
    target_url = input("Enter Q to quit.\nPaste URL and press enter: ")
    download_manga_slicing(target_url)
