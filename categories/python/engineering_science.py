a="""802.11
A&P
A1 Assessor
AAUS Scientific Diver
ABC Analysis
AC Drives
Accelerator Physics
Acoustical Engineering
Aeronautical Engineering
Aerospace Engineering
Agronomy
AI (Artificial Intelligence) HW/SW
AI Consulting
Aircraft Performance
Aircraft Propulsion
Aircraft Structures
Aircraft Systems
Airfield Lighting
Airframe
Airspace Management
Alarm Management
Alarm Systems
Alchemist
Algorithm
Analog
Analog / Mixed Signal / Digital
Anodizing
Anomaly Detection
Anritsu Certified
Antenna Design
Anthropology
Apple Homekit
Apple MFI
Arduino
ARM
ASIC
Astrophysics
Audio Processing
AutoCAD
Automotive
Automotive Engineering
Aviation
Bare Metal
Battery Charging and Batteries
BeagleBone Black
BERT
Bill of Materials (BOM) Analysis
Bill of Materials (BOM) Evaluation
Bill of Materials (BOM) Optimization
Biology
Biomedical Engineering
Biotechnology
Bluetooth
Bluetooth Module
Board Support Package (BSP)
Broadcast Engineering
Building Engineering
CAD/CAM
Calculus
CATIA
Cellular Design
Cellular Modules
Cellular Service
Chatbot Prompt Writing
Chemical Engineering
Circuit Board Layout
Circuit Design
Civil Engineering
Clean Technology
Climate Sciences
Cloud Service
Combinatorial Optimization
Combinatorial Problem Solving
Compliance Engineering
Component Engineering
Computational Analysis
Computational Fluid Dynamics
Computational Linguistics
Construction Engineering
Construction Monitoring
Consumer Products
Continuous Integration
Control Engineering
Control System Design
Controller Area Network (CAN)
Cryptography
Data Engineer
Data Mining
Data Science
DDR3 (PCIe, board design/fpga)
Deep Learning
DesignBuilder
DevOps
DFM (Design for Manufacturing)
Digital ASIC Coding
Digital Design
Digital Electronics
Digital Forensics
Digital Networking
DO-178 Certification
DO-254 Certification
Drilling Engineering
Drones
DSL/MODEMs
Edge Computing
Electrical Engineering
Electronic Design
Electronics
Embedded Systems
Encryption
Energy
Energy Modelling
Engineering
Engineering Drawing
Engineering Mathematics
Environmental Engineering
Estimation
Finite Element Analysis
Flex Circuit Design
FPGA
FPGA Coding
Genealogy
Generative AI
Genetic Algorithms
Genetic Engineering
Geology
Geospatial
Geotechnical Engineering
GPS
Graphical User Interface (GUI)
HALT/HASS Testing
Health
Heat Load Calculation
Home Design
Human Sciences
HVAC
HyperLynx
I2C
Imaging
IMX6
Industrial Engineering
Instrumentation
Intercom
Internet of Things (IoT)
Intrinsic Safety Applications
IP Cores
ISM Radio Module
ISO/IEC 17025 Calibration
Isometry
Large Language Model
Linear Programming
LLaMA
Local Interconnect Network (LIN)
LoRa
Machine Learning (ML)
Machine Vision / Video Analytics
Manufacturing Design
Manufacturing Engineering
Marine Engineering
Materials Engineering
Materials Science
Mathematics
MATLAB
Matlab and Mathematica
Mechanical Design
Mechanical Engineering
Mechatronics
Medical
Medical Engineering
Medical Products
MEMs
Microbiology
Microcontroller
Microstation
Midjourney
Midjourney Logo Prompt Writing
Mining Engineering
Mixing Engineering
Motor Control
MPSoC Design
Nanotechnology
Natural Language
Natural Language Processing
Near Field Communication (NFC)
Neural Networks
Optical Engineering
PCB Design and Layout
PCB Layout
PCI Express
Petroleum Engineering
Photogrammetry
Physics
PLC & SCADA
Power Amplifier RF
Power Converters
Power Generation
Power Redesign
Power Supply
Precast Designer
Process Engineering
Product End of Life (EOL)
Product Management
Project Scheduling
Prompt Engineering
Prompt Writing
Qi
Quality and Reliability Testing
Quantum
Quantum Computing
RADAR/LIDAR
Radio Frequency
Radio Frequency Engineering
Rapid Prototyping
Rasch Analysis
Remote Sensing
Renewable Energy Design
Renewables
Rezence
RFID (Radio-frequency identification)
Robotic Process Automation
Robotics
Robotics and Cognitive Automation
RTOS
RUST Programming
Schematic Review
Schematics
Scientific Computing
Scientific Research
Security
Semiconductor
Serial Peripheral Interface (SPI)
Siemens NX
Signal Processing
Sigrity
Simulation
Site Reliability Engineering
SMART City
Smart Lighting
Smart Phone/Tablet Apps
SoC Design
Solar
Solidworks
Statistical Analysis
Statistical Modeling
Statistics
STM32
Structural Engineering
Superconductors
Surfboard Design
Systems Engineering
Technology
Telecom
Telecommunications Engineering
Telecoms Engineering
Textile Engineering
Thermal & Environmental Testing
Thermal Analysis
Vector Calculus
Verilog / VHDL
Very-large-scale integration (VLSI)
Video Hardware
Video Processing
Virtual Assistant Solutions (Alexa, Google, Siri, Home Kit, Cortana)
Voice Assistance Devices
Waterproof Design (IP68)
WiFi
Wireless
Wireless Certification (CSA, FCC, IEC, FAA, IEEE, CE, Atex)
Wireless Charging
Wireless Radio Frequency Engineering
Wireless Sensors
Wireless Sensors and Gateways
Wolfram
Yocto
Zemax
Zigbee
Zwave""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("engineering_science.csv",header=False,index=False)
