import csv

# Path to the input text file
input_file = 'input.txt'

# Path to the output CSV file
output_csv_file = 'output.csv'

# Specify the delimiter used in the text file (two spaces in this case)
delimiter = '  '  # Two spaces as delimiter

# Open the input text file for reading
with open(input_file, 'r') as text_file:
    # Read the lines from the text file
    lines = text_file.readlines()

# Create a CSV file and write the data into it
with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Loop through each line and split using the delimiter, then write to the CSV file
    for line in lines:
        # Remove leading and trailing whitespace and split using the delimiter
        data = line.strip().split(delimiter)
        
        # Write the data to the CSV file
        csv_writer.writerow(data)

print(f"Conversion from '{input_file}' to '{output_csv_file}' complete.")
