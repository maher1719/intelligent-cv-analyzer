import csv
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Read CSV and parse skills grouped by categories
category_skills = defaultdict(list)
with open("/home/maher/Downloads/scrap/categories/categories.csv", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        category = row[0]  # Assume category is in the first column
        skills = row[1:]   # Remaining columns contain skills
        category_skills[category].extend([skill.strip().lower() for skill in skills])

# Build a co-occurrence matrix for each category
co_occurrence = {category: defaultdict(lambda: defaultdict(int)) for category in category_skills}
for category, skills in category_skills.items():
    unique_skills = set(skills)
    for skill1 in unique_skills:
        for skill2 in unique_skills:
            if skill1 != skill2:
                co_occurrence[category][skill1][skill2] += 1

# Visualize Top Skills in a Word Cloud for Each Category
for category, skills in category_skills.items():
    skill_counts = pd.Series(skills).value_counts()
    wordcloud = WordCloud(width=1200, height=800).generate_from_frequencies(skill_counts)
    
    plt.figure(figsize=(10, 5))
    plt.title(f"Top Skills in {category}")
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
