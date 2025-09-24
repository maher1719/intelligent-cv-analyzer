import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("csv/skills_no_duplicate_sorted.csv", header=None)

# Print the number of lines in the CSV file
print(f"Number of lines in the CSV file: {df.shape[0]}")
