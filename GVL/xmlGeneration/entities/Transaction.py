import xml.etree.ElementTree as ET


class Transaction:
    def __init__(self, id, date, customer, products, payment_method, city, store_type, discount_applied, season,
                 promotion):
        self.id = id
        self.date = date
        self.customer = customer
        self.products = products
        self.payment_method = payment_method
        self.city = city
        self.store_type = store_type
        self.discount_applied = discount_applied
        self.season = season
        self.promotion = promotion

    def to_xml(self):
        transaction_el = ET.Element("Transaction")

        transaction_el.append(self.customer.to_xml("Customer"))

        products_el = ET.Element("Products")
        for product in self.products:
            products_el.append(product.to_xml())
        transaction_el.append(products_el)

        ET.SubElement(transaction_el, "Transaction_ID").text = str(self.id)
        ET.SubElement(transaction_el, "Date").text = str(self.date)
        ET.SubElement(transaction_el, "Payment_Method").text = str(self.payment_method)
        ET.SubElement(transaction_el, "City").text = str(self.city)
        ET.SubElement(transaction_el, "Store_Type").text = str(self.store_type)
        ET.SubElement(transaction_el, "Discount_Applied").text = str(self.discount_applied)
        ET.SubElement(transaction_el, "Season").text = str(self.season)
        ET.SubElement(transaction_el, "Promotion").text = str(self.promotion)

        return transaction_el
