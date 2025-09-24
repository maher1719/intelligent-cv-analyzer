a=""" A/R analysis
A/R Collections
A/R Management
Account Management
Account Payables Management
Account Receivables Management
Accounting
Actimize
Administrative Support
Airline
Alternative Investments
Alumni Relations
Annual Report Design
Anti Money Laundering
Antitrust Economics
Appointment Setting
Asset Management
Attorney
Audit
Autotask
Bank Reconciliation
Billing
Brain Storming
Budgeting and Forecasting
Business Analysis
Business Analytics
Business Coaching
Business Consulting
Business Development
Business Management
Business Plans
Business Requirement Documentation
Business Strategy
Business Valuation
Capital Markets
Care Management
Career Consulting
Certified Public Accountant
Change Management
Chartered Secretary Services
Christmas
Closer
Compensation and Benefits
Compensation Consulting
Compliance
Compliance and Safety Training
Conflict Resolution
Construction Management
Consulting
Contract Management
Contracts
Core Consulting Skills
Core Systems Transformation
Corporate Income Tax
Corporate Law
Corporate Social Responsibility
Corporate Transactions
Credit Analysis
Credit Repair
Criminal Law
Crystal Reports
CTO
Custom Duties Tax
Customer Experience
Customer Retention
Customer Strategy
Customs and Global Trade Services
Data Analysis
Data Protection
Database Management
Development Assessment
Development Consulting
Document Checking
EBS Finance
EBS Procurement
Ecological Consulting
Econometrics
Economics
ECPay
Education & Tutoring
Employee Engagement
Employee Experience
Employee Training
Employment Law
Employment Tax
Energy and Resource Tax
Enterprise Coordination
Entrepreneurship
Environmental Consulting
Equity Research
Equity Transaction Advice
ERP
Event Management
Event Planning
Executive Coaching
Executive Compensation
Executive Reward
Expatriate Tax
External Auditing
Family Law
Finance
Finance Transformation
Financial Accounting
Financial Analysis
Financial Consulting
Financial Crime
Financial Forecasting
Financial Markets
Financial Modeling
Financial Services Tax
Fircosoft
FIX API
Forensic Consulting
Fraud Detection
Fundraising
Game Testing
General Tax Advisory
Global Mobility
Global Tax Compliance
Health Care Management
Health Planning
Health Plans Digitization
Hedge Fund Management
History
Human Resources
IBM Db2
Immigration
Immigration Law
Indirect Tax
Insurance
Intellectual Property Law
Interviewing
Intuit QuickBooks
Inventory Management
Investment Banking
Investment Management
Invoicing
ISO9001
Jewellery
Leadership Development
Legal
Legal Analysis
Legal Assistance
Legal Consultation
Legal Research
Legal Review
Legal Translation
Life Coaching
Life Science Tax Services
LinkedIn Recruiting
Linnworks Order Management
Litigation
Logistics Company
M&A Tax
Management
Management Consulting
Manufacturing Strategy
Market Sizing
Marketplace Service
Media and Entertainment Tax
Medical Billing and Coding
Medical Translation
Mergers and Acquisitions
MYOB
nCino
Nintex Forms
Nintex Workflow
Nutrition
Operations Management
Operations Research
Organization Design
Organizational Change Management
OTRS
Paralegal Services
Patents
PAYE Tax
Payment Consulting
Payment Processing
Payroll
Payroll HR S&E
PeopleSoft
Performance Management
Personal Development
Personal Income Tax
Personal Tax
PitchBook
Planning Consulting
Political science
Portfolio Management
Private Client
Private Equity
Product Consulting
Product Development
Programmatic Advertising
Project Management
Project Management Office
Project Planning
Property Development
Property Insurance
Property Law
Property Management
Property Tax
Public Relations
Public Sector and Taxation
Public Speaking
Real Estate
Real Estate Management
Real Estate Tax
Recruitment
Report Development
Research and Development
Reward
Risk Assessment
Risk Management
Safety Consulting
Salesforce CPQ
Salesforce.com
Sarbanes-Oxley (SOX)
SAS
Secretarial
Share Schemes
Shared Services
Six Sigma
Social Impact
Social Security Tax
Sourcing
Sports
Startup Consulting
Startups
Strategic Planning
Talent Acquisition
Tax
Tax Accounting
Tax Centre of Excellence
Tax Compliance
Tax Compliance and Outsourcing
Tax Law
Tax Management Consulting
Tax Preparation
Tax Reporting
Tax Risk Management
Tax Technology
Technical Recruiter
Technology Law
Total Reward
Trademark
Trademark Registration
Trading
Training
Training Development
Transaction Tax
Transfer Pricing
TS/ISO 16949 Audit
Underwriting
Unit4 Business World
Urban Planning
US Taxation
Valuation & Appraisal
Value Added Tax
Value Based Healthcare
Video Conferencing
Visa / Immigration
Wave Accounting
Wealth Management
Weddings
Workday Compensation
Workday Core HR
Workday Financials
Workday Payroll
Workday Security
Workday Talent & Recruiting
Workday Time & Absence
Workflow Consulting
Workforce Management
Xero""".lower().split("\n")
print(a)
import pandas as pd
df=pd.DataFrame(a).to_csv("b.csv",header=False,index=False)