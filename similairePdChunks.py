import itertools
import pandas as pd
import numpy as np

# Initialize an empty dictionary to store the words and their connections
words = {}

# Function to update the words dictionary and track array with a chunk of data
def update_words_and_track(chunk, track, keys_dict):
    for row in chunk.itertuples(index=False):
        parts = row._asdict()
        for a, b in itertools.combinations(parts.values(), 2):
            if a and b:
                if a not in keys_dict:
                    keys_dict[a] = len(keys_dict)
                    words[a] = [b]
                else:
                    words[a].append(b)

                if b not in keys_dict:
                    keys_dict[b] = len(keys_dict)
                    words[b] = [a]
                else:
                    words[b].append(a)

                a_index = keys_dict[a]
                b_index = keys_dict[b]

                # Resize the track array if necessary
                size = len(keys_dict)
                if track.shape[0] < size:
                    new_track = np.zeros((size, size))
                    new_track[:track.shape[0], :track.shape[1]] = track
                    track = new_track

                track[a_index, a_index] += 1
                track[b_index, b_index] += 1
                track[a_index, b_index] += 1
                track[b_index, a_index] += 1

    return track

# Read the CSV file in chunks of 10,000 rows
chunksize = 10000
keys_dict = {}
track = np.zeros((1, 1))  # Initialize with a small size, will be resized later
i=1
for chunk in pd.read_csv("csv/skillsFreelancerFinal_equalized.csv", header=None, chunksize=chunksize):
    print(i*10000)
    track = update_words_and_track(chunk, track, keys_dict)
    i=i+1

# Get the keys from the keys_dict
keys = list(keys_dict.keys())

# Print the keys
print(keys)

# Scale the track array to [0,1]
for row in range(track.shape[0]):
    track[row, :] /= track[row, row]

# Create a DataFrame from the track array
track_df = pd.DataFrame(track, index=keys, columns=keys)

# Save the DataFrame to a CSV file
track_df.to_csv('correspendentFinalClean.csv')
