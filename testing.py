import requests
from bs4 import BeautifulSoup
import time

url = "https://s3.amazonaws.com/capitalbikeshare-data/index.html"

# Fetch the rendered HTML (static here, no JS needed)
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all anchor tags with href
links = [a["href"] for a in soup.find_all("a", href=True)]

# Keep only .zip files
zip_links = [link for link in links if link.endswith(".zip")]

for link in zip_links:
    print(link)
