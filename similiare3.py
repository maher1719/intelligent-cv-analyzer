# generate_matrix.py
import pandas as pd
import numpy as np
import itertools
from collections import defaultdict

# --- Configuration ---
# This is the file where each row represents a set of co-occurring skills for a project/job.
INPUT_SKILLS_FILE = "csv/skillsFreelancerFinal.csv"

# This will be the final, correctly formatted co-occurrence matrix.
OUTPUT_MATRIX_FILE = "skill_co_occurrence_matrix2.csv"

# --- Main Script ---

print(f"Step 1: Reading skills from '{INPUT_SKILLS_FILE}' and building co-occurrence map.")

# Use defaultdict(set) for efficient and duplicate-free storage of skill connections.
skill_connections = defaultdict(set)
all_skills = set()

# We read the CSV line by line to handle varying numbers of skills per row.
with open(INPUT_SKILLS_FILE, 'r', encoding='utf-8') as f:
    # Skip the header row if it exists.
    # If you are SURE there's no header, you can comment out the next line.
    next(f, None) 
    
    for line in f:
        # Split by comma and strip whitespace/quotes from each skill
        skills_in_row = [skill.strip().strip('"') for skill in line.strip().split(',')]
        
        # Filter out any empty strings that might result from trailing commas
        cleaned_skills = [skill for skill in skills_in_row if skill]
        
        # Add all unique skills to our master set
        all_skills.update(cleaned_skills)
        
        # Generate all unique pairs of skills in this row
        for skill1, skill2 in itertools.combinations(cleaned_skills, 2):
            skill_connections[skill1].add(skill2)
            skill_connections[skill2].add(skill1)

print(f"Step 2: Found {len(all_skills)} unique skills. Creating the co-occurrence matrix.")

# Create a sorted list of keys for consistent matrix ordering
keys = sorted(list(all_skills))
size = len(keys)

# Create a mapping of skill_name -> index for much faster lookups
key_to_index = {key: i for i, key in enumerate(keys)}

# Initialize a numpy array to store the counts
co_occurrence_counts = np.zeros((size, size), dtype=int)

# Populate the matrix with co-occurrence counts
for skill, connections in skill_connections.items():
    i = key_to_index[skill]
    # The diagonal will store the total number of connections (degree) for each skill
    co_occurrence_counts[i, i] = len(connections)
    for connected_skill in connections:
        if connected_skill in key_to_index:
            j = key_to_index[connected_skill]
            # We simply count 1 for each co-occurrence
            co_occurrence_counts[i, j] = 1

print("Step 3: Normalizing the matrix to create correlation scores.")

# Create a copy of the matrix for normalization
# We will divide each cell (i, j) by the total occurrences of skill i.
# This gives P(j|i) - the probability of seeing skill j given that you see skill i.
normalized_matrix = np.zeros((size, size), dtype=float)
for i in range(size):
    total_occurrences = co_occurrence_counts[i, i]
    if total_occurrences > 0:
        normalized_matrix[i, :] = co_occurrence_counts[i, :] / total_occurrences
        normalized_matrix[i, i] = 1.0 # The probability of a skill co-occurring with itself is 1

print("Step 4: Saving the final matrix to CSV.")

# Create a pandas DataFrame to save the result with proper headers and index
final_df = pd.DataFrame(normalized_matrix, index=keys, columns=keys)

# Save to CSV. Pandas will automatically handle quoting for skill names with commas.
final_df.to_csv(OUTPUT_MATRIX_FILE)

print(f"\nSuccess! Your skill intelligence matrix has been saved to '{OUTPUT_MATRIX_FILE}'.")
print("This file is the 'brain' of your application.")
print("\nYou can now use this file as input for the 'generate_centrality.py' script and then the final 'cv_analyzer_app.py'.")
