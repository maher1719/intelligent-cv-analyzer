import itertools
import pandas as pd
import numpy as np
from collections import defaultdict

# Initialize a dictionary to store words and connections as sets to prevent duplicates
words = defaultdict(set)

# Define the chunk size for reading the CSV in parts
chunk_size = 10000  # Adjust based on available memory
i=1
# Process CSV in chunks
for chunk in pd.read_csv("csv/skillsFreelancerFinal_equalized.csv", header=None, chunksize=chunk_size,low_memory=False):
    # Iterate over each row in the chunk
    print(i*10000)
    for row in chunk.itertuples(index=False):
        # Generate pairwise combinations and update connections
        for a, b in itertools.combinations(row, 2):
            if a and b:
                words[a].add(b)
                words[b].add(a)
    i=i+1

# Convert keys to a list and determine the size of the final dataset
keys = list(words.keys())
size = len(keys)

# Initialize a numpy array to track connections
track = np.zeros((size, size))

# Populate the track array based on the accumulated connections
for i, k in enumerate(keys):
    track[i, i] = len(words[k])  # Self-connection represents the degree of the node
    for j in words[k]:
        j_index = keys.index(j)
        track[i, j_index] += 1
        track[j_index, i] += 1

# Normalize each row in track by dividing each element by its diagonal entry
track = np.divide(track, np.diagonal(track).reshape(-1, 1), where=np.diagonal(track).reshape(-1, 1) != 0)

# Create a DataFrame from the track array with labels for rows and columns
track_df = pd.DataFrame(track, index=keys, columns=keys)

# Save the DataFrame to a CSV file
track_df.to_csv('correspendentFinalClean.csv')
