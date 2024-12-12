from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Step 1: Use Selenium to open the webpage
url = 'https://starwarsunlimited.com/cards'
options = Options()
options.headless = True  # Run in headless mode
service = Service('C:\\Users\\brike\\Desktop\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')  # Update with the path to your WebDriver
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

# Step 3: Scroll down the page until all listings are loaded
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(30)  # Wait for the page to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Step 4: Extract the page source and parse it with BeautifulSoup
html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')

# Step 5: Select all image elements and extract their src attributes
image_elements = soup.find_all('img')
image_urls = [img['src'] for img in image_elements if 'src' in img.attrs]

# Step 6: Write the image URLs to a CSV file
csv_file = 'image_urls.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Image URL'])
    for url in image_urls:
        writer.writerow([url])

print(f'Image URLs have been written to {csv_file}')