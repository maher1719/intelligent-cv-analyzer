
a="""Product Sourcing & Manufacturing
Post a ProjectSign up for work
3D Printing
Alerting
AliExpress
Amazon
Analog Electronics
Andon
Buyer Sourcing
CNC Accessories
CNC Machine Retrofitting
CNC Programming
Computer Aided Manufacturing
Computer Numerical Control
Computerized Embroidery
Coordinate-Measuring Machine
Freedom to Operate Search
Manufacturing
Patent Design Search
Patent Infringement Research
Patent Invalidity Search
Patent Landscape
Patent Validity Search
Process Automation
Process Validation
Product Design
Product Research
Product Sourcing
Supplier Sourcing
Supply Chain""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("product.csv",header=False,index=False)
