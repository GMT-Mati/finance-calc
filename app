import requests

from bs4 import BeautifulSoup

import matplotlib.pyplot as plt

# Specify the location and zoom level

location = "51.109/17.033"

zoom = "6"

# Build the URL for the Windy website

url = f"https://www.windy.com/{location}?{location},{zoom}"

# Send a request to the website and get the HTML response

response = requests.get(url)

html = response.content

# Parse the HTML using BeautifulSoup and extract the wind speed and direction data

soup = BeautifulSoup(html, "html.parser")

wind_data = soup.find_all("div", class_="leaflet-interactive leaflet-marker-icon")

speeds = []

directions = []

for data in wind_data:

    speed = data.get("data-wind-speed")

    direction = data.get("data-wind-dir")

    if speed is not None and direction is not None:

        speeds.append(float(speed))

        directions.append(float(direction))

# Visualize the wind speed and direction data using a scatter plot

plt.scatter(directions, speeds)

plt.xlabel("Wind Direction (degrees)")

plt.ylabel("Wind Speed (m/s)")

plt.title("Wind Data for Location: " + location)

plt.show()
