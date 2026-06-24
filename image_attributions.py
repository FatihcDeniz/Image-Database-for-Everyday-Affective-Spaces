import pandas as pd

# Licenses used by Flickr 
licenses = {'licenses': {'license': [{'id': 0,
    'name': 'All Rights Reserved',
    'url': 'https://www.flickrhelp.com/hc/en-us/articles/10710266545556-Using-Flickr-images-shared-by-other-members'},
   {'id': 4,
    'name': 'CC BY 2.0',
    'url': 'https://creativecommons.org/licenses/by/2.0/'},
   {'id': 6,
    'name': 'CC BY-ND 2.0',
    'url': 'https://creativecommons.org/licenses/by-nd/2.0/'},
   {'id': 3,
    'name': 'CC BY-NC-ND 2.0',
    'url': 'https://creativecommons.org/licenses/by-nc-nd/2.0/'},
   {'id': 2,
    'name': 'CC BY-NC 2.0',
    'url': 'https://creativecommons.org/licenses/by-nc/2.0/'},
   {'id': 1,
    'name': 'CC BY-NC-SA 2.0',
    'url': 'https://creativecommons.org/licenses/by-nc-sa/2.0/'},
   {'id': 5,
    'name': 'CC BY-SA 2.0',
    'url': 'https://creativecommons.org/licenses/by-sa/2.0/'},
   {'id': 7,
    'name': 'No known copyright restrictions',
    'url': 'https://www.flickr.com/commons/usage/'},
   {'id': 8,
    'name': 'United States Government Work',
    'url': 'https://www.usa.gov/government-copyright'},
   {'id': 9,
    'name': 'Public Domain Dedication (CC0)',
    'url': 'https://creativecommons.org/publicdomain/zero/1.0/'},
   {'id': 10,
    'name': 'Public Domain Mark',
    'url': 'https://creativecommons.org/publicdomain/mark/1.0/'},
   {'id': 11,
    'name': 'CC BY 4.0',
    'url': 'https://creativecommons.org/licenses/by/4.0/'},
   {'id': 12,
    'name': 'CC BY-SA 4.0',
    'url': 'https://creativecommons.org/licenses/by-sa/4.0/'},
   {'id': 13,
    'name': 'CC BY-ND 4.0',
    'url': 'https://creativecommons.org/licenses/by-nd/4.0/'},
   {'id': 14,
    'name': 'CC BY-NC 4.0',
    'url': 'https://creativecommons.org/licenses/by-nc/4.0/'},
   {'id': 15,
    'name': 'CC BY-NC-SA 4.0',
    'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/'},
   {'id': 16,
    'name': 'CC BY-NC-ND 4.0',
    'url': 'https://creativecommons.org/licenses/by-nc-nd/4.0/'}]},
 'stat': 'ok'}

# Load CSV
image_data = pd.read_csv(r".\Attribution Data\attribution_data.csv")

# List of images you used
images_used = ["bedroom__0.png", "bedroom__1.png", "office__0.png",
 "living room__123.png","kitchen__275.png", "restaurant__157.png"]

# Output file
output_file = r".\Attribution Data\image_attributions.txt"

# Store formatted lines
attributions = []

for idx, image_name in enumerate(images_used, start=1):
    # Filter row
    row = image_data[image_data['image_name'] == image_name]
    
    if not row.empty:
        title = row.iloc[0]['title']
        author = row.iloc[0]['owner']
        source = row.iloc[0]['original']
        license_ = licenses["licenses"]["license"][row.iloc[0]['license']]["name"]
        
        # Format string
        line = f'{idx}) Title: "{title}", Author: "{author}", Source: {source}, License: "{license_}"'
        attributions.append(line)
    else:
        attributions.append(f'{idx}) No data found for {image_name}')

# Save to text file
with open(output_file, 'w', encoding='utf-8') as f:
    for line in attributions:
        f.write(line + '\n')

print(f"Attributions saved to: {output_file}")