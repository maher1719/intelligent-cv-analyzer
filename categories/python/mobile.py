a="""Mobile Phones & Computing
Post a ProjectSign up for work
Amazon Fire
Amazon Kindle
Android
App Store Optimization
App Usability Analysis
Appcelerator Titanium
Apple Watch
Blackberry
Geolocation
iPad
iPhone
J2ME
Kotlin
Metro
Mobile App Development
Nokia
Palm
Salesforce Lightning
Samsung
Symbian
Virtualization
WebOS
Windows CE
Windows Mobile
Windows Phone""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("mobile.csv",header=False,index=False)