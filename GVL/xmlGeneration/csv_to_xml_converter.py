import ast
from lxml import etree  # Para a função transform_boolean_strings
import xml.etree.ElementTree as ET  # Manipulação de XML
import xml.dom.minidom as md  # Para formatar a saída em XML
from .csv_reader import CSVReader
from .entities.Transaction import Transaction
from .entities.Customer import Customer
from .entities.Product import Product


class CSVtoXMLConverter:

    def __init__(self, path):
        # Inicializa o leitor de CSV com o caminho fornecido
        self._reader = CSVReader(path)

    def to_xml(self):
        # Lê e converte os dados do CSV em transações, usando um "builder" (construtor) para cada linha do CSV
        transactions = self._reader.read_entities(
            attr="Transaction_ID",
            builder=lambda row: Transaction(
                id=row["Transaction_ID"],
                date=row["Date"],
                customer=Customer(name=row["Customer_Name"], category=row["Customer_Category"]),
                products=self._parse_products(row),
                payment_method=row["Payment_Method"],
                city=row["City"],
                store_type=row["Store_Type"],
                discount_applied=row["Discount_Applied"],
                season=row["Season"],
                promotion=row["Promotion"]
            )
        )

        # Cria o elemento raiz XML chamado "Transactions"
        root_el = ET.Element("Transactions")

        # Adiciona cada transação convertida como um elemento filho no XML
        for transaction in transactions.values():
            root_el.append(transaction.to_xml())

        return root_el

    def to_xml_str(self):
        # Converte o elemento XML para uma string usando `ElementTree`
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()

        # Aplica formatação (identação) usando `minidom` para melhorar a legibilidade
        dom = md.parseString(xml_str)
        pretty_xml = dom.toprettyxml()

        # Aplica a transformação para strings booleanas usando `transform_boolean_strings`
        transformed_xml = self.transform_boolean_strings(pretty_xml)

        return transformed_xml

    def _parse_products(self, row):
        # Extrai e converte os dados de produtos da linha do CSV
        product_names = ast.literal_eval(row["Product"])  # Converte string para lista de nomes de produtos
        total_items = int(row["Total_Items"])  # Converte o total de itens para um inteiro
        total_costs = float(row["Total_Cost"])  # Converte o custo total para um float

        # Cria uma lista com um único objeto Product (pode ser ajustado se necessário)
        products = [Product(product_names, total_items, total_costs)]
        return products

    def transform_boolean_strings(self, xml_content):
        # Converte o conteúdo XML para um documento usando `lxml.etree`
        xml_doc = etree.fromstring(xml_content.encode('utf-8'))

        # Localiza todos os nós de texto que têm valores "True" ou "False"
        boolean_text_elements = xml_doc.xpath('//text()[(.="True" or .="False")]')

        # Substitui "True" ou "False" pelos valores equivalentes em minúsculas
        for text_element in boolean_text_elements:
            parent_element = text_element.getparent()  # Obtém o elemento pai do texto
            parent_element.text = parent_element.text.lower()  # Converte o texto para minúsculas

        # Converte a árvore XML modificada de volta para uma string
        transformed_xml = etree.tostring(xml_doc, pretty_print=True, encoding="utf-8").decode("utf-8")

        return transformed_xml