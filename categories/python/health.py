a="""Health & Medicine
Post a ProjectSign up for work
Counseling Psychology
Diet
Epidemiology
Fitness
Food Safety
Hypnotherapy
Managed Care
Medical Scribe
Psychometric Testing
Public Health""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("health.csv",header=False,index=False)