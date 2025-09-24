import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('skillsFreelancerFinal_equalized.csv',low_memory=False)


# Count the occurrences of each unique value in the DataFrame
value_counts = df.stack().value_counts()

# Convert the Series to a DataFrame
value_counts_df = value_counts.reset_index()

# Rename the columns of the DataFrame
value_counts_df.columns = ['value', 'count']

# Save the DataFrame to a new CSV file
value_counts_df.to_csv('value_counts_clean_not_clean.csv', index=False)
