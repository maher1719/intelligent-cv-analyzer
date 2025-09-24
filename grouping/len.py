import pandas as pd
from collections import defaultdict

import csv

# Read the data to determine maximum column count
"""with open("skillsFreelancerFinal.csv", mode="r") as file:
    reader = list(csv.reader(file))
    max_columns = max(len(row) for row in reader)

# Write data to a new CSV file with padded columns
with open("skillsFreelancerFinal_equalized.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    for row in reader:
        # Pad each row with empty strings until it matches max_columns
        row.extend([""] * (max_columns - len(row)))
        writer.writerow(row)

print(f"All rows have been padded to {max_columns} columns and saved to 'skillsFreelancerFinal_equalized.csv'.")"""


# Read CSV file, treating each row as a list of skills
import pandas as pd
from collections import defaultdict
chunk_size = 1000
num_chunk=0
# Read CSV in chunks and calculate co-occurrences
for chunk in pd.read_csv("skillsFreelancerFinal_equalized.csv", header=None, chunksize=chunk_size):
    # Calculate total rows for progress tracking
    num_chunk+=1
print(num_chunk*1000)