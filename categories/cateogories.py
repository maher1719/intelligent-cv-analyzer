import pandas as pd
import os

# Directory where the CSV files are located
directory = '/home/maher/Downloads/scrap/categories/'






"""df = pd.read_csv("b.csv", header=None)

        # Transpose the dataframe
df = df.transpose()

        # Set the first column as the index
df.columns = df.iloc[0]
df = df[1:]

        # Write the transposed dataframe back to the original file
df.to_csv("bu.csv", index=False, header=False)"""
"""for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Read the CSV file
        df = pd.read_csv(os.path.join(directory, filename), header=None)


        # Set the first column as the index
        df.columns = df.iloc[0]
        df = df[1:]

        # Write the transposed dataframe back to the original file
        df.to_csv(os.path.join(directory, filename), index=False)
# List to hold all dataframes"""
dataframes = []

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Read the CSV file
        df = pd.read_csv(os.path.join(directory, filename), header=None)

        # Append the dataframe to the list
        dataframes.append(df)

# Concatenate all dataframes into one
final_df = pd.concat(dataframes)

# Write the final dataframe to a new CSV file
final_df.to_csv('categories.csv', index=False,header=False)
