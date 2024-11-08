import xml.dom.minidom
import requests

def get_coordinates(city):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city,
        'format': 'json',
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
    else:
        print(f"Erro na solicitação: {response.status_code}")

    return None, None

xml_path = "unique_cities.xml"

doc = xml.dom.minidom.parse(xml_path)

cities_elements = doc.getElementsByTagName("City")

for city_element in cities_elements:
    city_name = city_element.firstChild.nodeValue.strip()

    latitude, longitude = get_coordinates(city_name)

    coordinates_element = doc.createElement("Coordinates")
    city_element.appendChild(coordinates_element)

    latitude_element = doc.createElement("Latitude")
    latitude_element.appendChild(doc.createTextNode(str(latitude)))
    coordinates_element.appendChild(latitude_element)

    longitude_element = doc.createElement("Longitude")
    longitude_element.appendChild(doc.createTextNode(str(longitude)))
    coordinates_element.appendChild(longitude_element)

with open("output_with_coordinates.xml", "w") as file:
    doc.writexml(file, indent="\n")