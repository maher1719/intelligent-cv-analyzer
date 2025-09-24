import itertools
import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv("csv/skills_no_duplicate.csv", header=None)

# Initialize an empty dictionary to store the words and their connections
words = {}

# Iterate over each row in the DataFrame
for row in df.itertuples(index=False):
    parts = row._asdict()
    for a, b in itertools.combinations(parts.values(), 2):
        if a and b:
            if a not in words:
                words[a] = [b]
            else:
                words[a].append(b)
            if b not in words:
                words[b] = [a]
            else:
                words[b].append(a)

# Print the words dictionary
print(words)

# Get the size and keys of the words dictionary
size = len(words)
keys = list(words.keys())

# Initialize a numpy array to track the connections
track = np.zeros((size, size))

# Populate the track array
for i, k in enumerate(keys):
    track[i, i] = len(words[k])
    for j in words[k]:
        track[i, keys.index(j)] += 1
        track[keys.index(j), i] += 1

# Print the keys
print(keys)

# Scale the track array to [0,1]
for row in range(track.shape[0]):
    track[row, :] /= track[row, row]

# Create a DataFrame from the track array
track_df = pd.DataFrame(track, index=keys, columns=keys)

# Save the DataFrame to a CSV file
track_df.to_csv('correspendentFinalClean.csv')
