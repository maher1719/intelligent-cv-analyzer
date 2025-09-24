import pandas as pd

# Step 1: Read the CSV file
input_file = 'correspendentFinalCleanSorted.csv'
output_file = 'correspendantFinalCleanTranspose.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Step 2: Transpose the DataFrame
df_transposed = df.transpose()

# Step 3: Save the transposed DataFrame to a new CSV file
df_transposed.to_csv(output_file, header=False)

print(f"Transposed CSV saved to {output_file}")
