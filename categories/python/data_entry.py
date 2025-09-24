a="""ABBYY FineReader
Academic Administration
ANOVA
Answering Telephones
Article Submission
Bookkeeping
BPO
Call Center
Chat Operation
Contact Center Services
Customer Service
Customer Support
Data Analytics
Data Annotating
Data Architecture
Data Cleansing
Data Delivery
Data Entry
Data Extraction
Data Processing
Data Scraping
Database Design
Desktop Support
Email Handling
ePub
Excel
Excel Macros
Excel VB Capabilities
Excel VBA
General Office
Google Spreadsheets
GPT Agent
Helpdesk
Infographic and Powerpoint Slide Designing
Investment Research
LibreOffice
Microsoft Office
Microsoft Outlook
Microsoft Word
Order Processing
Phone Support
PostgreSQL Administration
Procurement
Qlik
Qualitative Research
qwerty
Records Management
Relational Databases
SAP Master Data Governance
Software Documentation
Spreadsheets
Technical Support
Telegram Moderation
Telephone Handling
Time Management
Transcription
Typeform
Typing
Video Upload
Web Search""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("data_entry.csv",header=False,index=False)