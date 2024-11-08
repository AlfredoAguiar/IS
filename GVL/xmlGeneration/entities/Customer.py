import xml.etree.ElementTree as ET


class Customer:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def to_xml(self, element_name):
        customer_el = ET.Element(element_name)
        ET.SubElement(customer_el, "Customer_Name").text = str(self.name)
        ET.SubElement(customer_el, "Customer_Category").text = str(self.category)
        return customer_el
