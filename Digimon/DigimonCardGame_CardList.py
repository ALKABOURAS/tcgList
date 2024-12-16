import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Send a GET request to the URL
url = 'https://world.digimoncard.com/cardlist/?search=true&category=522024#page-4'
response = requests.get(url)
html_content = response.content

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')


# Step 3: Get Card Details

# 0. Image URL
image_url = soup.select('.cardinfo_top>.card_img')
# print(image_url)

# 1. ID Code
id_code = soup.select('.cardno')
# print(id_code)

# 2. Card Name
card_name = soup.select('.card_detail_inner>.card_name')
# print(card_name)

# 3. Color
color = soup.select('.cardColor')
# print(color)

# 4. Card Info Head
cardinfo_head = soup.select('.cardinfo_head')
# print(cardinfo_head)

# 5. Card Info Top
cardinfo_top = soup.select('.cardinfo_top_body')
# print(cardinfo_top)

# 6. Card Info Bottom
cardinfo_bottom = soup.select('.cardinfo_bottom')
# print(cardinfo_bottom)


# Reformatting Card Details
infobottom = []
for row in cardinfo_bottom:
    cells = row.find_all([])
    row_data = [cell.text.strip() for cell in cells]
    infobottom.append(row_data)

print(infobottom)

# Step 4: Create Final Table



# Step 5: Extract text content from table rows

# rows = []
# for row in table_rows:
#     cells = row.find_all([])
#     row_data = [cell.text.strip() for cell in cells]
#     rows.append(row_data)
#
# # # Step 6: Write the extracted data to a CSV file
# csv_file = 'output1.csv'
# with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     # Write headers
#     # writer.writerow(headers)
#     # Write rows
#     writer.writerows(rows)
#
# print(f'Data has been written to {csv_file}')