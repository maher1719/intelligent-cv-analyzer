import csv

# Read all the skills from the input CSV file
all_skills = []
with open("skillsFreelancerFinal.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        all_skills.extend(row)

# Remove any duplicates from the list of skills
unique_skills = list(set(all_skills))

# Write the unique skills to a new CSV file
with open("unique_skills.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(unique_skills)
