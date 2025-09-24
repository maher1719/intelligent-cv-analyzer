a="""Abnormal Psychology
Abstract
Academic Medicine
Academic Publishing
Academic Research
Academic Writing
Annuals
Apple iBooks Author
Article Rewriting
Article Writing
Beta Reading
Biography Writing
Blog
Blog Writing
Blogging
Book Review
Book Writing
Braille
Business Plan Writing
Business Writing
Cartography & Maps
Case Study Writing
Catch Phrases
Comedy Writing
Communications
Compliance and Safety Procedures Writer
Content Audit
Content Creation
Content Development
Content Strategy
Content Writing
Copy Editing
Copy Typing
Copywriting
Cover Letter
Creative Writing
Domain Research
eBooks
Editing
Editorial Writing
Educational Research
English Translation
Environmental Science
Essay Writing
Fact Checking
Fashion Writing
Fiction
Financial Research
Forum Posting
Ghostwriting
Grant Writing
Headlines
Investigative Journalism
Journalism
LaTeX
Legal Writing
LinkedIn Profile
Manuscripts
Medical Research
Medical Writing
Memoir Writing
Newsletters
Non-Fiction Writing
Online Writing
PDF
Pitch Deck Writing
Podcast Writing
Poetry
Powerpoint
Press Releases
Product Descriptions
Proofreading
Proposal Writing
Publishing
Report Writing
Research
Research Writing
Resumes
Reviews
RFP Writing
Romance Writing
Scientific Writing
Screenwriting
Script Writing
SEO Writing
Short Stories
Slogans
Social Media Copy
Speech Writing
Survey Research
Taglines
Technical Documentation
Technical Writing
Test Plan Writing
Test Strategy Writing
Translation
Travel Writing
Web Page Writer
White Paper
WIKI
Wikipedia
Word Processing
Writing""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("writing.csv",header=False,index=False)