a="""ABR Accredited Buyer Representative
ABR Designation
Ad Planning & Buying
Advertising
Affiliate Marketing
Agency Relationship Management
Airbnb
Aircraft Sales
Amazon Ads
Analytics Sales
ATS Sales
B2B Marketing
Basecamp
Bing Ads
Book Marketing
Brand Management
Brand Marketing
Branding
Bulk Marketing
Channel Account Management
Channel Sales
Classifieds Posting
ClickBank
ClickFunnels
Cloud Sales
Competitor Analysis
Content Marketing
Conversion Rate Optimization
CRM
Crowdfunding
Customer Retention Marketing
Datacenter Sales
Digital Agency Sales
Digital Strategy
Direct Mail
Drip
eBay
Email Campaign
Email Marketing
Emerging Accounts
Enterprise Sales
Enterprise Sales Management
Etsy
Eventbrite
Facebook Ads
Facebook Marketing
Facebook Shops
Facebook Verification
Field Sales
Field Sales Management
Financial Sales
Google Ads
Google Adsense
Google Adwords
Google Shopping
Healthcare Sales
HootSuite
HR Sales
Hubspot Marketing
IDM Sales
Inbound Marketing
Indiegogo
Influencer Marketing
Inside Sales
Instagram Ads
Instagram Marketing
Instagram Verification
Interactive Advertising
Internet Marketing
Internet Research
ISV Sales
Kartra
Keap
Keyword Research
Kickstarter
Klaviyo
Lead Generation
Leads
Life Science Sales
Mailchimp
Mailwizz
Market Analysis
Market Research
Marketing
Marketing Strategy
Marketo
Media Relations
Media Sales
Medical Devices Sales
MLM
Mobile Sales
Multi Level Marketing
Network Sales
OEM Account Management
OEM Sales
Pardot Marketing
Payroll Sales
Periscope
Podcast Marketing
Podcasting
PPC Marketing
Product Marketing
Recruiting Sales
Reseller
Retail Sales
SaaS Sales
Sales
Sales Account Management
Sales Management
Sales Promotion
Search Engine Marketing
Security Sales
SEMrush
SendGrid
SEOMoz
Social Media Marketing
Social Sales
Social Video Marketing
Software Sales
Soundcloud Promotion
Spotify Ads
Sprout
Technology Sales
Telecom Sales
Telemarketing
TikTok
Tiktok Ads
Twitter Marketing
Unboxing Videos
Viral Marketing
Visual Merchandising
WooCommerce
YouTube Ads""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("sales_marketing.csv",header=False,index=False)