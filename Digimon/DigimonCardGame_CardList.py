from typing import List, Any

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

# 3.0 Image URL
image_url = soup.select('.cardinfo_top>.card_img')
# print(image_url)

# 1. ID Code
id_code = soup.select('.cardno')
# print(id_code)
# print(id_code[0])
# print(id_code[1])

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

# 6. Card Info Flex
# cardinfo_flex = soup.select('.cardinfo_flex')
# print(cardinfo_flex)

# 6. Card Info Bottom
cardinfo_bottom = soup.select('.cardinfo_bottom')
# print(cardinfo_bottom)


# Step 4: Reformatting Card Details

# 4.0 Image URL
final_image_url = []
for row in image_url:
    cells = row.find_all([])                                                      # Finds HTML Element
    # print(cells)

    html_element, imgurl = str(cells).rsplit('src="../', 1)                # Formats cells list to String
    imgurl = imgurl.split('"/>')[0]                                               # and splits the URL

    final_image_url_text = "https://world.digimoncard.com/" + imgurl              # Generating Full URL
    final_image_url.append(final_image_url_text)                                  # Append to Final List

# print(final_image_url)

# 4.1 Card ID

final_card_id = []
for row in id_code:
    html_element, idcode = str(row).rsplit('cardno">',1)
    idcode = idcode.split('</li>')[0]

    final_card_id.append(idcode)

# print(final_card_id)


# 4.2 Card Name
#
final_card_name = []
for row in card_name:
    html_element, cardname = str(row).rsplit('card_name">',1)
    cardname = cardname.split('</div>')[0]

    final_card_name.append(cardname)
#
# print(final_card_name)

# 4.3 Card Color
#
final_card_color = []
for row in color:
    cardcolor = str(row).split('">')[2]
    cardcolor = cardcolor.split('</span>')[0]

    final_card_color.append(cardcolor)
#
# print(final_card_color)

# 4.4 Card Info Head
#
infohead = []
i=0
for row in cardinfo_head:
    cells = row.find_all(['li'])
    row_data = [cell.text.strip() for cell in cells]
    infohead.append(row_data)

    infohead[i].pop(0)                                             # Removes 1st Value of i List
    i +=1
# #
# print(infohead)


# 4.5 Card Info Top         (Contains Info Flex)
#
infotop = []
i=0
for row in cardinfo_top:
    cells = row.find_all(['dd'])
    row_data = [cell.text.strip() for cell in cells]
    infotop.append(row_data)

    infotop[i].pop(0)
    i +=1
#
# print(infotop)

# 4.6 Card Info Bottom

infobottom = []
for row in cardinfo_bottom:
    cells = row.find_all(['dd'])
    row_data = [cell.text.strip() for cell in cells]
    infobottom.append(row_data)
#
# print(infobottom)

# Step 5: Create Final Tables

final_card_details = []
i = 0
for rows in final_card_id:
    final_card_details.insert (i,[
        final_image_url[i],
        final_card_id[i],
        final_card_name[i],
        final_card_color[i]
    ]
    )

    final_card_details[i].extend(infohead[i])
    final_card_details[i].extend(infotop[i])
    final_card_details[i].extend(infobottom[i])

    i += 1

# print(final_card_details)

final_card_list = []
final_card_list_alt_art = []

c1 = 0
c2 = 0
for i in range(len(final_card_details)):
    if "Alternative Art" in str(final_card_details[i]):
        final_card_list_alt_art.insert(c1, final_card_details[i])
        c1 += 1
    else:
        final_card_list.insert(c2, final_card_details[i])
        c2 += 1

print(final_card_list)
print(final_card_list_alt_art)


# Step 6: Write the extracted data to a CSV file

csv_file = 'card_list.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for j in range(len(final_card_list)):
        writer.writerow(final_card_list[j])
    for k in range(len(final_card_list_alt_art)):
        writer.writerow(final_card_list_alt_art[k])

print(f'Data has been written to {csv_file}')