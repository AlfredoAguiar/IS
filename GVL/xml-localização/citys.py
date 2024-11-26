import xml.etree.ElementTree as ET

xml_path = "../../data/Retail_Transactions_Dataset.xml"

tree = ET.parse(xml_path)
root = tree.getroot()

unique_cities = set()

output_root = ET.Element("UniqueCities")

for transaction in root.findall('.//Transaction'):
    city = transaction.find('City').text

    if city not in unique_cities:
        unique_cities.add(city)

        city_element = ET.SubElement(output_root, "City")
        city_element.text = city

output_tree = ET.ElementTree(output_root)

output_tree.write("dt/unique_cities.xml")
