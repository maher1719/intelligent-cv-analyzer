a="""ASHSP
Coffee Delivery
Delivery
Esports
Food Delivery
Freelance
Healthcare Education
Inspections
Investigation
Joint Commission International
Local Job
Motivational Speaking
Odd Jobs
Parcel Delivery
Photo Anywhere
Pickup
Policymaking
Psychological Assessment
QOPI
Quanum
Shopping
Surveillance
Travel Ready
Virtual Assistant""".split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("other.csv",header=False,index=False)