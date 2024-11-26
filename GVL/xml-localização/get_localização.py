import xml.dom.minidom
import requests
import time
import os

def get_coordinates(city):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city,
        'format': 'json',
    }
    headers = {
        'User-Agent': 'YourProjectName/1.0 (your_email@example.com)'
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            print(f"Successfully fetched coordinates for {city}: Latitude {latitude}, Longitude {longitude}")
            return latitude, longitude
        else:
            print(f"No coordinates found for city: {city}")
    except requests.RequestException as e:
        print(f"Error fetching coordinates for {city}: {e}")
    return None, None

def update_xml_with_coordinates(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Input file {input_path} not found.")
        return

    try:
        doc = xml.dom.minidom.parse(input_path)
        cities_elements = doc.getElementsByTagName("City")

        for city_element in cities_elements:
            city_name = city_element.firstChild.nodeValue.strip()
            print(f"Processing city: {city_name}")

            latitude, longitude = get_coordinates(city_name)
            time.sleep(1)  # Respect API rate limits

            coordinates_element = doc.createElement("Coordinates")
            city_element.appendChild(coordinates_element)

            latitude_element = doc.createElement("Latitude")
            latitude_element.appendChild(doc.createTextNode(str(latitude) if latitude else "N/A"))
            coordinates_element.appendChild(latitude_element)

            longitude_element = doc.createElement("Longitude")
            longitude_element.appendChild(doc.createTextNode(str(longitude) if longitude else "N/A"))
            coordinates_element.appendChild(longitude_element)

        with open(output_path, "w", encoding="utf-8") as file:
            doc.writexml(file, indent="\n", addindent="  ", newl="\n")
        print(f"Updated XML saved to {output_path}")

    except Exception as e:
        print(f"Error processing XML: {e}")

# Paths to input and output files
input_xml_path = "dt/unique_cities.xml"
output_xml_path = "dt/output_with_coordinates.xml"

update_xml_with_coordinates(input_xml_path, output_xml_path)