a="""2D Animation
2D Animation Explainer Video
2D Drafting
2D Drawing
2D Game Art
2D Layout
360-degree video
3D Animation
3D Architecture
3D CAD
3D Design
3D Drafting
3D Layout
3D Logo
3D Model Maker
3D Modelling
3D Rendering
3D Rigging
3D Scanning
3D Studio Max
3D Visualization
3ds Max
A/V design
A/V editing
A/V Engineering
A/V Systems
A&R
Acting
ActionScript
Adobe Creative Suite
Adobe Dreamweaver
Adobe Fireworks
Adobe Flash
Adobe FrameMaker
Adobe InDesign
Adobe Lightroom
Adobe LiveCycle Designer
Adobe Photoshop
Adobe Robohelp
Advertisement Design
Affinity Designer
Affinity Photo
After Effects
AI Rendering
Album Design
Album Production
Alternative Rock
Alto Flute
Android UI Design
Animated Video Development
Animation
Animoto
App Design
Apple Compressor
Apple Logic Pro
Apple Motion
Architectural Rendering
Architectural Visualization
Architecture
Art Consulting
Artist & Repertoire Administration
Arts & Crafts
Audio Ads
Audio Editing
Audio Engineering
Audio Mastering
Audio Production
Audio Services
Audiobook
Audiobook Narration
AutoCAD Architecture
Autodesk
Autodesk Civil 3D
Autodesk Fusion 360
Autodesk Inventor
Autodesk Revit
Autodesk Sketchbook Pro
Avid
Axure
Banner Design
Beautiful AI
Blog Design
Book Artist
Book Cover Design
Book Design
Bootstrap
BricsCAD
Brochure Design
Building Architecture
Building Information Modeling
Building Regulations
Business Cards
Calligraphy
Canva
Capture NX2
Card Design
Caricature & Cartoons
Catalog Design
Cel Animation
CGI
Character Illustration
Childrens Book Illustration
Cinema 4D
Clip Studio Paint
CMS IntelliCAD
Collage Making
Color Grading
Comics
Commercials
Concept Art
Concept Design
Corel Painter
CorelDRAW
Corporate Identity
Costume Design
Covers & Packaging
Creative Design
CSS
Cutout Animation
CV Design
DaVinci Resolve
Design
Digital Art
Digital Cinema Packages
Digital Painting
Digital Product Design
Doodle
Draftsight
Drawing Artist
eBook Design
eLearning Designer
Evernote
Explainer Videos
Fabric Printing Design
Facade Design
Fashion Consulting
Fashion Design
Fashion Modeling
Film Production
Filmmaking
Final Cut Pro
Final Cut Pro X
Finale / Sibelius
Fire Alarm Design
FL Studio
Flash 3D
Flash Animation
Flex
Floor Plan
Flow Charts
FlowVella
Flyer Design
Format and Layout
Front-end Design
Furniture Design
Game Art
Game Trailer
Game UI
GarageBand
Generative Design
Genially
GIF
GIF Animation
Google Slides
GraffixPro Studio
Graphic Art
Graphic Design
GstarCAD
Haiku Deck
Handy Sketch Pad
Icon Design
Illustration
Illustrator
Image Consultation
Image Processing
iMovie
Industrial Design
Infographics
Infrastructure Architecture
Inkscape
Instructional Design
Interaction Design
Interior Design
Intros & Outros
Invision
Invitation Design
Isometric Animation
JDF
Jingles & Intros
Keynote
Kinetic Typography
Kizoa
Krita
Label Design
Landing Pages
Lettering
Level Design
Lighting Design
Logo Animation
Logo Design
Magazine Design
Make Real
Makerbot
Manga
Matte Painting
Maya
Mentimeter
Menu Design
Microservices
MIDI
Mood Board
Motion Design
Motion Graphics
Music
Music Management
Music Production
Music Transcription
Music Video
NanoCAD
Neo4j
NX CAD
Oil Painting
Package Design
Packaging Design
Pattern Design
Pattern Making
Performing Arts
Photo Editing
Photo Restoration
Photo Retouching
Photography
Photoshop
Photoshop Design
Pixel Art
Podcast Editing
Post-Production
Poster Design
Pre-production
Pre-production Animation
Presentations
Prezi
Print
Print Design
Procreate
Product Cover
Product Photography
ProgeCAD
Prototype Design
PSD to HTML
PSD2CMS
QuarkXPress
Radio Announcement
Research Drone Footages
Resin
Rhino 3D
Rotoscoping
RWD
Seamless Printing
Shopify Templates
Sign Design
SketchUp
Slidebean
SmartDraw
Social Media Post Design
SolidEdge
Sound Design
Sound Effects
Sound Engineering
SoundCloud
Sports Design
Stationery Design
Sticker Design
Storyboard
T-Shirts
Tattoo Design
Technical Drawing / Tech Pack
Tekla Structures
Templates
Textile Design
TikZ
Tldraw
Town Planning
Traditional Animation
Twitter Spaces
Typography
UI / User Interface
Unigraphics NX
Urban Design
UX / User Experience
V-Ray
Vector Design
Vector Tracing
Vectorization
Vectorworks
Vehicle Signage
VFX Art
Video Ads
Video Broadcasting
Video Editing
Video Post-editing
Video Production
Video Services
Video Streaming
Video Tours
Videography
VideoScribe
Vimeo
Virtual Staging
Visme
Visual Arts
Visual Design
Visual Effects
Voice Acting
Voice Artist
Voice Over
Voice Talent
Watercolor Painting
Web Animation
Website Design
Whiteboard
Whiteboard Animation
Wireframes
Word
WordPress Design
Yahoo! Store Design
YouTube Video Editing
Zbrush
Zoho Show""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("design.csv",header=False,index=False)