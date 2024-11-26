import xml.etree.ElementTree as ET
import xml.dom.minidom
import os


def add_location_to_transaction(transaction, city, latitude, longitude):
    """
    Adds location information (city, latitude, longitude) to a transaction.
    """
    loc = ET.SubElement(transaction, "local")
    city_element = ET.SubElement(loc, "City")
    city_element.text = city

    coordinates = ET.SubElement(loc, "Coordinates")
    latitude_element = ET.SubElement(coordinates, "Latitude")
    latitude_element.text = f"{latitude:.7f}"
    longitude_element = ET.SubElement(coordinates, "Longitude")
    longitude_element.text = f"{longitude:.7f}"


def format_and_save_xml(tree, output_file):
    # Convert the tree to a string
    rough_string = ET.tostring(tree.getroot(), encoding="utf-8")
    # Parse the rough string into a DOM object
    reparsed = xml.dom.minidom.parseString(rough_string)
    # Remove extra empty lines caused by minidom
    pretty_xml = reparsed.toprettyxml(indent="  ")
    cleaned_xml = "\n".join(line for line in pretty_xml.splitlines() if line.strip())

    # Save the formatted XML to the file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(cleaned_xml)


# Paths to input and output files
transactions_file = "../../data/Retail_Transactions_Dataset.xml"
coordinates_file = "dt/output_with_coordinates.xml"
output_file = "../../data/Retail_Transactions_Dataset_loc.xml"

# Ensure input files exist
if not os.path.exists(transactions_file) or not os.path.exists(coordinates_file):
    print("Error: One or more input files are missing.")
    exit()

# Load the XML files
try:
    transactions_tree = ET.parse(transactions_file)
    transactions_root = transactions_tree.getroot()

    coordinates_tree = ET.parse(coordinates_file)
    coordinates_root = coordinates_tree.getroot()
except ET.ParseError as e:
    print(f"Error parsing XML files: {e}")
    exit()

# Create a dictionary of city coordinates
city_coordinates = {}
for city_element in coordinates_root.findall(".//City"):
    city_name = city_element.text.strip()
    coordinates_element = city_element.find("Coordinates")
    if coordinates_element is not None:
        try:
            latitude = float(coordinates_element.find("Latitude").text)
            longitude = float(coordinates_element.find("Longitude").text)
            city_coordinates[city_name] = (latitude, longitude)
        except (AttributeError, ValueError):
            print(f"Invalid coordinates for city: {city_name}")

# Modify transactions by adding location data
for transaction in transactions_root.findall(".//Transaction"):
    city_element = transaction.find("City")
    if city_element is not None:
        city_name = city_element.text.strip()
        if city_name in city_coordinates:
            latitude, longitude = city_coordinates[city_name]
            add_location_to_transaction(transaction, city_name, latitude, longitude)
            # Remove the original <City> element
            transaction.remove(city_element)
        else:
            print(f"Coordinates not found for city: {city_name}")

# Save the modified transactions XML
try:
    format_and_save_xml(transactions_tree, output_file)
    print(f"Updated XML saved to {output_file}")
except Exception as e:
    print(f"Error saving the XML file: {e}")