import flickrapi
import requests
import io
import time
from PIL import Image
import pandas as pd
import datetime
import os 
import re
import geopandas as gpd
import matplotlib.pyplot as plt

loc = r".\Attribution Data\attribution_data.csv"

data = pd.read_csv(loc)
# [VERY IMPORTANT] Remove this later!!
flickr = flickrapi.FlickrAPI("58445d0d307e80e14c9c8e678706ba2d", "ecff13ac8d1aba55", format='parsed-json')

location_data = {"id":[], "image_name":[],"latitude":[], "longitude":[]}

count = 0
for i in range(0,len(data.original)):
    print(i)
    url = data.iloc[i].original
    photo_id = re.search(r'/(\d+)_', url).group(1)

    photo_name = data.iloc[i].image_name

    try:
        location = flickr.photos.geo.getLocation(photo_id=photo_id)
        
        location_data["id"].append(photo_id)
        location_data["image_name"].append(photo_name)
        
        location_data['latitude'].append(location["photo"]["location"]["latitude"])
        location_data['longitude'].append(location["photo"]["location"]["longitude"])

    except:
        print("Could find loc")
        count += 1

location_data = pd.DataFrame.from_dict(location_data)

# Plot the world map
gdf = gpd.GeoDataFrame(
    location_data,
    geometry=gpd.points_from_xy(location_data["longitude"], location_data["latitude"]),
    crs="EPSG:4326"
)

world = gpd.read_file("https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip")
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
world.plot(ax=ax,color="#E6E6E6",edgecolor="#FFFFFF",linewidth=0.5)
gdf.plot(ax=ax,color="#E63946",markersize=30,alpha=0.4,edgecolor="black",linewidth=0.3)
# Remove axis
ax.set_axis_off()

plt.tight_layout()
plt.savefig(r".\Visualizations\map.svg")
plt.show()