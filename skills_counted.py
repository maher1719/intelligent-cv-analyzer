import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('skills_no_duplicate_sorted.csv')

# Remove duplicate rows
df = df.drop_duplicates()

# Sort each row’s values, convert them to strings, and store as tuples
df_sorted = df.apply(lambda row: tuple(sorted(map(str, row.dropna()))), axis=1)

# Count occurrences of each unique sorted row
row_counts = df_sorted.value_counts()

# Create a new DataFrame with the counts
df_unique_counts = pd.DataFrame(row_counts, columns=['count']).reset_index()
df_unique_counts.columns = [f'Column_{i+1}' for i in range(df_unique_counts.shape[1] - 1)] + ['count']

# Save the resulting DataFrame to a new CSV file
df_unique_counts.to_csv('skills_counted.csv', index=False)
