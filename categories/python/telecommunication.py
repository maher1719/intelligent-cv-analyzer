a="""Access Point Identification
Active Site Survey
Aerial Technical Site Survey
Base Station Equipment Management
Blueprint Calibration
Discord
Floorplan Blueprinting
HetNet Access Point Installation
Hidden Wireless Network Detection
Live Survey
Passive Site Survey
Physical Site Survey
PnP BTS configuration
Pre-inspection visits
Predictive Site Survey
Radio Access Network Commissioning
RAN Call Testing
RAN NMS Integration
Remote Quality Audit
RF Manual Site Survey
RF Site Survey
Rogue Access Point Detection
Signal Propagation Assessment
Small Cell Deployment
TeamViewer
Technical Site Audit
Technical Site Survey
Walking Path Analysis
Wireless Access Point Installation
Wireless Capacity Analysis
Wireless Coverage Assessment
Wireless Network Risk Analysis & Reduction
Wireless Network Security Analysis
Wireless Security Audit
Wireless Site Survey""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("telecommunication.csv",header=False,index=False)