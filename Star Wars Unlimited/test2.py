import csv

# Step 1: Read the existing CSV file
input_file = 'output.csv'
output_file = 'reformatted_output.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Step 2: Write the new header
    new_header = ['ID Code', 'Color', 'Card Name', 'Stage Level/Type', 'Rarity']
    writer.writerow(new_header)

    # Step 3: Process each row
    for row in reader:
        if len(row) == 5:  # Ensure the row has the expected number of columns
            card, level, color, type_, rarity = row
            # Extract ID Code and Card Name from the Card field
            if '(' in card:
                card_name, id_code = card.rsplit('(', 1)
                id_code = id_code.rstrip(')')
            else:
                card_name = card
                id_code = ''
            # Skip rows with 'Alternative Art' in the Rarity field
            if 'Alternative Art' in rarity:
                continue
            # Step 4: Write the reformatted row
            new_row = [id_code, color, card_name.strip(), level, type_, rarity]
            writer.writerow(new_row)

print(f'Data has been reformatted and written to {output_file}')