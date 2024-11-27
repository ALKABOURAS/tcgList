# Step 1: Install Selenium and the appropriate WebDriver for your browser
# pip install selenium
# Download the WebDriver for your browser (e.g., ChromeDriver for Chrome)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Step 2: Use Selenium to open the webpage
url = 'https://starwarsunlimited.com/cards'
options = Options()
options.headless = True  # Run in headless mode
service = Service('C:\\Users\\brike\\Desktop\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')  # Update with the path to your WebDriver
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

# Step 2.5 pRESS BUTTON TO CHANGE VIEW TO TABLE

button = driver.find_element(
    By.XPATH, '//*[@id="__next"]/div[2]/main/div[5]/div/div[1]/div/button[2]'
).click()
# Step 3: Scroll down the page until all listings are loaded
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)  # Wait for the page to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Step 4: Extract the page source and parse it with BeautifulSoup
html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')

# Select the table headers
header_cells = soup.select('thead th')
headers = [header.get_text(strip=True) for header in header_cells]

# Select the table rows
table_rows = soup.select('tr.cards-table--row')

# Extract text content from table rows
rows = []
for row in table_rows:
    cells = row.find_all('td')
    row_data = []
    for cell in cells:
        if cell.find('img'):
            cell_text = ' '.join(img['alt'] for img in cell.find_all('img'))
        elif cell.find('span'):
            cell_text = ' '.join(span.text for span in cell.find_all('span'))
        else:
            cell_text = cell.text.strip()
        row_data.append(cell_text)
    rows.append(row_data)

# Write the extracted data to a CSV file
csv_file = 'starwars.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow(headers)
    # Write rows
    writer.writerows(rows)

print(f'Data has been written to {csv_file}')