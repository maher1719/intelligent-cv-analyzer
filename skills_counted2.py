import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('skillsFreelancerFinal_equalized.csv',low_memory=False)


# Sort each row’s values, convert them to strings, and store as tuples
df_sorted = df.apply(lambda row: tuple(sorted(map(str, row.dropna()))), axis=1)

# Count occurrences of each unique sorted row
row_counts = df_sorted.value_counts()

# Create a new DataFrame with the counts
df_unique_counts = pd.DataFrame(row_counts, columns=['count']).reset_index()

# Split tuple values into separate columns
df_unique_counts = pd.DataFrame(df_unique_counts['index'].to_list(), columns=[f'Skill_{i+1}' for i in range(df_unique_counts['index'].str.len().max())])

# Add the count column back to the DataFrame
df_unique_counts['count'] = row_counts.values

# Save the resulting DataFrame to a new CSV file
df_unique_counts.to_csv('skills_counted_not_clean.csv', index=False)
