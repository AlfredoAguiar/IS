import xml.etree.ElementTree as ET


class Product:
    def __init__(self, names, total_items, total_costs):
        self.names = names
        self.total_items = total_items
        self.total_costs = total_costs

    def to_xml(self):
        product_element = ET.Element("Product")

        for name in self.names:
            name_element = ET.SubElement(product_element, "Name")
            name_element.text = str(name)

        total_items_element = ET.SubElement(product_element, "Total_Items")
        total_items_element.text = str(self.total_items)

        total_costs_element = ET.SubElement(product_element, "Total_Cost")
        total_costs_element.text = str(self.total_costs)

        return product_element
