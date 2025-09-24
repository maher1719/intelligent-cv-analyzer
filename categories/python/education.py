a="""Academic Achievement
Academic Advising
Accounting Tutoring
Algebra Tutoring
Calculus Tutoring
Chemistry Tutoring
Chinese Tutoring
Coding Lesson
College Tutoring
Computer Science Tutoring
Education Consulting
English Teaching
English Tutoring
French Tutoring
Geometry
German Tutoring
GMAT Tutoring
GRE Tutoring
Guitar Lesson
Japanese Teaching
Japanese Tutoring
Java Tutoring
Korean Tutoring
Language Tutoring
Latin Tutoring
LSAT Tutoring
Math Tutoring
MCAT Tutoring
Music Lesson
Physics Tutoring
Programming Help
Reading Tutoring
SAT Tutoring
Science Tutoring
Spanish Tutoring
Statistics Tutoring
Video Game Coaching
Writing Tutoring""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("education.csv",header=False,index=False)