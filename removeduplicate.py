import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('skills_no_duplicate.csv')

# Remove duplicate rows
df = df.drop_duplicates()

# Sort the DataFrame based on the first column
df = df.sort_values(by=df.columns[0])

# Save the DataFrame back to a CSV file
df.to_csv('skills_no_duplicate_sorted.csv', index=False)