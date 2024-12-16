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


def process_image_url(row):
    cells = row.find_all([])
    html_element, imgurl = str(cells).rsplit('src="../', 1)
    imgurl = imgurl.split('"/>')[0]
    return "https://world.digimoncard.com/" + imgurl


def process_id_code(row):
    html_element, idcode = str(row).rsplit('cardno">', 1)
    idcode = idcode.split('</li>')[0]
    return idcode


def process_card_name(row):
    html_element, cardname = str(row).rsplit('card_name">', 1)
    cardname = cardname.split('</div>')[0]
    return cardname


def process_card_color(row):
    cardcolor = str(row).split('">')[2]
    cardcolor = cardcolor.split('</span>')[0]
    return cardcolor


def process_cardinfo_head(row):
    cells = row.find_all(['li'])
    row_data = [cell.text.strip() for cell in cells]
    row_data.pop(0)
    return row_data


def process_cardinfo_top(row):
    cells = row.find_all(['dd'])
    row_data = [cell.text.strip() for cell in cells]
    row_data.pop(0)
    return row_data


def process_cardinfo_bottom(row):
    cells = row.find_all(['dd'])
    row_data = [cell.text.strip() for cell in cells]
    return row_data


def reformat_card_details(image_url, id_code, card_name, color, cardinfo_head, cardinfo_top, cardinfo_bottom):
    final_image_url = list(map(process_image_url, image_url))

    final_card_id = list(map(process_id_code, id_code))

    final_card_name = list(map(process_card_name, card_name))

    final_card_color = list(map(process_card_color, color))

    infohead = list(map(process_cardinfo_head, cardinfo_head))

    infotop = list(map(process_cardinfo_top, cardinfo_top))

    infobottom = list(map(process_cardinfo_bottom, cardinfo_bottom))

    return final_image_url, final_card_id, final_card_name, final_card_color, infohead, infotop, infobottom


def process_final_card_details(i, final_image_url, final_card_id, final_card_name, final_card_color, infohead, infotop,
                               infobottom):
    card_details = [
        final_image_url[i],
        final_card_id[i],
        final_card_name[i],
        final_card_color[i]
    ]
    card_details.extend(infohead[i])
    card_details.extend(infotop[i])
    card_details.extend(infobottom[i])
    return card_details


def create_final_tables(final_image_url, final_card_id, final_card_name, final_card_color, infohead, infotop,
                        infobottom):
    indices = range(len(final_card_id))
    final_card_details = list(
        map(lambda i: process_final_card_details(i, final_image_url, final_card_id, final_card_name, final_card_color,
                                                 infohead, infotop, infobottom), indices))
    return final_card_details


def is_alternative_art(card_detail):
    return "Alternative Art" in str(card_detail)


def separate_alt_art(final_card_details):
    final_card_list_alt_art = list(filter(is_alternative_art, final_card_details))
    final_card_list = list(filter(lambda x: not is_alternative_art(x), final_card_details))
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
