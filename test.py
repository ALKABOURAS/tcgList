import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Send a GET request to the URL
url = 'https://digimoncardgame.fandom.com/wiki/EX-07:_Extra_Booster_Digimon_Liberator'
response = requests.get(url)
html_content = response.content

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Select the ul headers and the table rows
ul_headers = soup.select('.wds-tabs__tab-label a')
table_rows = soup.select('.cardlist tbody tr')

# Step 4: Extract text content from ul headers
headers = [header.text.strip() for header in ul_headers]

# Step 5: Extract text content from table rows
rows = []
for row in table_rows:
    cells = row.find_all(['th', 'td'])
    row_data = [cell.text.strip() for cell in cells]
    rows.append(row_data)

# Step 6: Write the extracted data to a CSV file
csv_file = 'output.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow(headers)
    # Write rows
    writer.writerows(rows)

print(f'Data has been written to {csv_file}')