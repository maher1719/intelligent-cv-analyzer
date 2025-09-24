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

# Initialize co-occurrence dictionary
co_occurrence = defaultdict(lambda: defaultdict(int))

# Set chunk size (e.g., 1000 rows per chunk)
chunk_size = 1000
num_chunk=0
# Read CSV in chunks and calculate co-occurrences
for chunk in pd.read_csv("skillsFreelancerFinal_equalized.csv", header=None, chunksize=chunk_size):
    # Calculate total rows for progress tracking
    total = len(chunk)
    num_chunk+=1
    for idx, row in chunk.iterrows():
        print(f"Processing chunk {num_chunk} - Row {idx + 1}/{total} of size {total}")
        
        # Clean and normalize skills, removing any empty strings
        skills = [str(skill).strip().lower() for skill in row if str(skill).strip()]
        
        # Populate co-occurrence matrix
        for i, skill1 in enumerate(skills):
            for j, skill2 in enumerate(skills):
                if i != j:  # Only consider pairs (skill1, skill2) where skill1 != skill2
                    co_occurrence[skill1][skill2] += 1

# Convert co-occurrence dictionary to DataFrame
co_occurrence_df = pd.DataFrame(co_occurrence).fillna(0).astype(int)

# Export to CSV
co_occurrence_df.to_csv("grouped4.csv")
print(co_occurrence_df)

