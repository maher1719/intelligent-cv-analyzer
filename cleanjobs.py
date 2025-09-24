import csv
import re

with open("jobsSkills2.csv") as skills_file:
    reader = csv.reader(skills_file)
    skills = list(reader)

    current_skill_name = skills[1][0]
    past_skill_name = skills[1][0]
    skills_list = []
    skills_words = ""
    f = open("skillsJobsGrouped.csv", 'a', newline='')
    csv_writer = csv.writer(f)
    for skill in range(1, len(skills)):
        current_skill = skills[skill]
        current_skill_name = current_skill[0]

        if (past_skill_name == current_skill_name):
            skills_words += current_skill[1]



        else:

            skills_list.extend(re.split(',', skills_words))
            skills_list_final = list(dict.fromkeys(skills_list))
            skills_string = ','.join(skills_list_final)
            print(skills_string)
            skills_write = [current_skill_name, skills_string]
            print(current_skill_name)
            csv_writer.writerow(skills_write)
            skills_list = []
            print("\n")
            skills_words = ""

            past_skill_name = current_skill_name
