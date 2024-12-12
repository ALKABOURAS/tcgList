# Make url number increment by 1 in loop
import csv

url = 'https://www.swudb.com/cards/shd/280.png'
csv_file = 'image_urls_show.csv'
url_list = []
for i in range(263, 523):
    url = url.replace(str(i-1), str(i))
    url_list.append(url)
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Image URL'])
    for url in url_list:
        writer.writerow([url])
print(f'Image URLs have been written to {csv_file}')

