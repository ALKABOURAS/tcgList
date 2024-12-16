import time

import requests
from bs4 import BeautifulSoup
import csv


def fetch_html(url):
    response = requests.get(url)
    return response.content


def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')


def extract_card_details(soup):
    image_url = soup.select('.cardinfo_top>.card_img')
    id_code = soup.select('.cardno')
    card_name = soup.select('.card_detail_inner>.card_name')
    color = soup.select('.cardColor')
    cardinfo_head = soup.select('.cardinfo_head')
    cardinfo_top = soup.select('.cardinfo_top_body')
    cardinfo_bottom = soup.select('.cardinfo_bottom')
    return image_url, id_code, card_name, color, cardinfo_head, cardinfo_top, cardinfo_bottom


def reformat_card_details(image_url, id_code, card_name, color, cardinfo_head, cardinfo_top, cardinfo_bottom):
    final_image_url = []
    for row in image_url:
        cells = row.find_all([])
        html_element, imgurl = str(cells).rsplit('src="../', 1)
        imgurl = imgurl.split('"/>')[0]
        final_image_url_text = "https://world.digimoncard.com/" + imgurl
        final_image_url.append(final_image_url_text)

    final_card_id = []
    for row in id_code:
        html_element, idcode = str(row).rsplit('cardno">', 1)
        idcode = idcode.split('</li>')[0]
        final_card_id.append(idcode)

    final_card_name = []
    for row in card_name:
        html_element, cardname = str(row).rsplit('card_name">', 1)
        cardname = cardname.split('</div>')[0]
        final_card_name.append(cardname)

    final_card_color = []
    for row in color:
        cardcolor = str(row).split('">')[2]
        cardcolor = cardcolor.split('</span>')[0]
        final_card_color.append(cardcolor)

    infohead = []
    i = 0
    for row in cardinfo_head:
        cells = row.find_all(['li'])
        row_data = [cell.text.strip() for cell in cells]
        infohead.append(row_data)
        infohead[i].pop(0)
        i += 1

    infotop = []
    i = 0
    for row in cardinfo_top:
        cells = row.find_all(['dd'])
        row_data = [cell.text.strip() for cell in cells]
        infotop.append(row_data)
        infotop[i].pop(0)
        i += 1

    infobottom = []
    for row in cardinfo_bottom:
        cells = row.find_all(['dd'])
        row_data = [cell.text.strip() for cell in cells]
        infobottom.append(row_data)

    return final_image_url, final_card_id, final_card_name, final_card_color, infohead, infotop, infobottom


def create_final_tables(final_image_url, final_card_id, final_card_name, final_card_color, infohead, infotop,
                        infobottom):
    final_card_details = []
    i = 0
    for rows in final_card_id:
        final_card_details.insert(i, [
            final_image_url[i],
            final_card_id[i],
            final_card_name[i],
            final_card_color[i]
        ])
        final_card_details[i].extend(infohead[i])
        final_card_details[i].extend(infotop[i])
        final_card_details[i].extend(infobottom[i])
        i += 1
    return final_card_details


def separate_alt_art(final_card_details):
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
    return final_card_list, final_card_list_alt_art


def write_to_csv(final_card_list, final_card_list_alt_art, csv_file='card_list.csv'):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for j in range(len(final_card_list)):
            writer.writerow(final_card_list[j])
        for k in range(len(final_card_list_alt_art)):
            writer.writerow(final_card_list_alt_art[k])
    print(f'Data has been written to {csv_file}')


def main(url):
    html_content = fetch_html(url)
    soup = parse_html(html_content)
    image_url, id_code, card_name, color, cardinfo_head, cardinfo_top, cardinfo_bottom = extract_card_details(soup)
    final_image_url, final_card_id, final_card_name, final_card_color, infohead, infotop, infobottom = reformat_card_details(
        image_url, id_code, card_name, color, cardinfo_head, cardinfo_top, cardinfo_bottom)
    final_card_details = create_final_tables(final_image_url, final_card_id, final_card_name, final_card_color,
                                             infohead, infotop, infobottom)
    final_card_list, final_card_list_alt_art = separate_alt_art(final_card_details)
    write_to_csv(final_card_list, final_card_list_alt_art)


if __name__ == "__main__":
    url = 'https://world.digimoncard.com/cardlist/?search=true&category=522014'
    main(url)
