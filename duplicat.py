import pandas as pd
import csv

# col_list_jobs=["name","description"]
# jobs=pd.read_csv("jobs.csv",usecols=col_list_jobs)
# skills=pd.read_csv("header2.csv")
# for index, row in jobs.iterrows():
#     row_description = row["description"]
#     for index2,row_skills in skills.iterrows():
#         print(row_description)
#         index=row_description.find(row_skills)
#         print(index)

with open('jobs - Copy (2).csv', newline='') as f:
    reader = csv.reader(f)
    jobs = list(reader)

with open('header2.csv', newline='') as f:
    reader = csv.reader(f)
    skills = list(reader)

file = open("jobsSkills2.csv", "w",newline='')
csv_writer=csv.writer(file)
for job in jobs:
    splited = job[1].split()
    list_skill = []
    list_skill.append(job[0])
    skills_gatherd = ""

    for word in splited:
        for skill in skills[0]:
            if skill.lower() == word.lower():
                skills_gatherd += "," + skill
    list_skill.append(skills_gatherd[1:])
    csv_writer.writerow(list(dict.fromkeys(list_skill)))
