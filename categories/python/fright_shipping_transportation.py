a="""Bicycle Courier
Boat
Boat with Trailer
Bulk Product (e.g grain)
Car
Car Courier
Car Driving
Caravan or Motorhome
Cargo Freight
Container Transport
Container Truck
Containerization
Courier
Dangerous Goods
DOP Management
Dropshipping
Dry Van Trucking
Flatbed Trucking
Flower Delivery
Freight
Furniture
Furniture Removal
General Freight
General Part Load
Grain Tipper
Haulier
Hay
Heavy Haulage
Heavy Haulage Trucking
Hiab Crane Trucking
Hotshot
Import/Export
International Shipping
Last Mile Optimization
Line Haulage
Livestock
Logistics
Machinery
Machinery (Stationary)
Machinery 50T and over
Motorbike
Motorcycle Courier
Moving
Package
Packing & Shipping
Pallets
Pallets (Less Than a Load)
Pilot
Pilot Work
Pipe
Portable Building
Rail Freight
Reefer Trucking
Refrigerated Goods
Removal Services
Shipping
Shipping Container
Trailer
Trailers to be carried
Truck Courier
Truck or Prime Mover
Trucking
Van Courier""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("firght_shipping_transportation.csv",header=False,index=False)