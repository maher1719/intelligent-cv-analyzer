a="""A&E
Abatement
ABO Certified
Air Conditioning
Alzheimers Care
Antenna Measurements
Antenna Services
Antique Restoration
Antiques
Appliance Installation
Appliance Repair
Art Installation
Asbestos Removal
Asphalt Contractor
Attic Access Ladders Making
Awnings
Baking
Balustrading
Bamboo Flooring
Bartending
Bathroom
Biometrics
Bracket Installation
Bricklaying
Building
Building Certification
Building Consulting
Building Design
Building Surveying
Car Washing
Carpentry
Carpet Cleaning
Carpet Repair & Laying
Carports
Carwashing
Casting
Catering Services
CCTV
CCTV Repair
Ceiling Installation
Cement Bonding Agents
Child Counselling
Clothesline Installation
Column Installation
Commercial Cleaning
Computer Repair
Computer Support
Concreting
Construction
Cooking / Baking
Cooking & Recipes
Counselling and Psychotherapy
Courses
Damp Proofing
Decking
Decoration
Demolition
Disposals
Domestic Cleaning
Drafting
Drone Photography
Electric Repair
Electronics repair
Embroidery
Epic Systems
Equipment Rental
Event Staffing
Excavation
Extensions & Additions
Fencing
Feng Shui
Field Technical Support
Financial Planning
Fire Fighting
Flashmob
Floor Coatings
Flooring
Flyscreen Installation
Frames & Trusses
Furniture Assembly
Gardening
Gas Fitting
General Labor
Glass / Mirror & Glazing
Gutter Installation
Hair Styles
Handyman
Harmonized System Cassification
Haute Cuisine
Heating Systems
Home Automation
Home Organization
Horticulture
Hot Water Installation
House Cleaning
Housework
IKEA Installation
Installation
Interiors
Kitchen
Landscape Design
Landscaping
Laundry and Ironing
Lawn Mowing
Lifestyle Coach
Lighting
Locksmith
Lost-wax Casting
Machinery Equipment Hire
Make Up
Marriage Counselling
Masonry
Material Coating
Millwork
Mobile Repair
Mobile Welding
Mortgage Brokering
Mural Painting
Notary Public
Painting
Pavement
Pest Control
Pet Sitting
Physical Fitness Training
Piping
Plumbing
Printer Repair
Psychology
Roofing
Sculpture
Sculpturing
Security Camera
Security Systems
Sewing
Solar Panel Installation
Teaching/Lecturing
Tiling
Upholstery Cleaning
Visa Ready Resources
Water Treatment
Welding
Workshops
Yard Work & Removal
Yoga""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("trades_services.csv",header=False,index=False)