import csv

# Read the contents of the CSV file
with open('imges.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = [row for row in reader]

# Modify the links
for row in rows:
    row[0] = row[0].replace('shd', 'SHD')

# Write the modified contents back to the CSV file
with open('imges.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print('Links have been updated in imges.csv')