import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('skillsFreelancerFinal.csv')

# Group by skill and count
skill_demand = df.groupby('skill').size().sort_values(ascending=False)

# Create trend visualization
plt.figure(figsize=(12,6))
plt.bar(skill_demand.index[:20], skill_demand.values[:20])
plt.xticks(rotation=45)
plt.title('Top 20 Most In-Demand Skills')
