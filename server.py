from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
from lxml import etree
from GVL.xmlGeneration.csv_to_xml_converter import CSVtoXMLConverter

# Caminho para o arquivo XML
arquivo_xml = "data/Retail_Transactions_Dataset.xml"


# Funções do servidor

def obter_duas_primeiras_transacoes():
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        transacoes = []
        for i, transaction in enumerate(root.findall("Transaction")):
            if i < 2:
                transacao_detalhes = []
                for child in transaction:
                    transacao_detalhes.append(f"{child.tag}: {child.text}")
                transacoes.append("\n".join(transacao_detalhes))
            else:
                break
        return "\n\n".join(transacoes)
    except Exception as e:
        return f"Erro ao ler o arquivo XML: {e}"


def executar_main_py():
    try:
        converter = CSVtoXMLConverter("data/Retail_Transactions_Dataset.csv")
        xml_content = converter.to_xml_str()

        file_path = "data/Retail_Transactions_Dataset.xml"
        with open(file_path, "w") as file:
            file.write(xml_content)

        return f"XML content saved to {file_path}"
    except Exception as e:
        return f"Erro ao converter CSV para XML: {e}"


def validate():
    xml_file_path = "data/Retail_Transactions_Dataset.xml"
    try:
        with open(xml_file_path, "r") as file:
            xml_content = file.read()

        schema_path = "GVL/xmlValidate/schema.xsd"
        xml_doc = etree.fromstring(xml_content)
        xml_schema = etree.XMLSchema(file=schema_path)

        if xml_schema.validate(xml_doc):
            return "XML is valid."
        else:
            return f"XML is not valid.\nErrors: {xml_schema.error_log}"
    except Exception as e:
        return f"Erro ao validar o XML: {e}"


def executar_xquery_por_cidade(cidade):
    try:
        with open(arquivo_xml, "r") as file:
            xml_content = file.read()

        xml_doc = etree.fromstring(xml_content.encode("utf-8"))
        query = f"//Transaction[City = '{cidade}']"
        results = xml_doc.xpath(query)

        result_texts = []
        for result in results:
            if isinstance(result, etree._Element):
                transaction_details = [f"{child.tag}: {child.text}" for child in result]
                result_texts.append("\n".join(transaction_details))

        if result_texts:
            return "\n\n".join(result_texts)
        else:
            return f"Nenhuma transação encontrada para a cidade {cidade}."
    except Exception as e:
        return f"Erro ao executar consulta XPath por cidade: {e}"


def executar_xquery_por_id(id_transacao):
    try:
        with open(arquivo_xml, "r") as file:
            xml_content = file.read()

        xml_doc = etree.fromstring(xml_content.encode("utf-8"))
        query = f"//Transaction[Transaction_ID = '{id_transacao}']"
        results = xml_doc.xpath(query)

        result_texts = []
        if results:
            for result in results:
                transaction_details = [f"{child.tag}: {child.text}" for child in result]
                result_texts.append("\n".join(transaction_details))

            return "\n\n".join(result_texts)
        else:
            return f"Nenhuma transação encontrada para o ID {id_transacao}."
    except Exception as e:
        return f"Erro ao executar consulta XPath por ID de transação: {e}"


# Criação do servidor XML-RPC
with SimpleXMLRPCServer(('127.0.0.1', 65432)) as server:
    server.register_function(obter_duas_primeiras_transacoes, 'obter_duas_primeiras_transacoes')
    server.register_function(executar_main_py, 'executar_main_py')
    server.register_function(validate, 'validate')
    server.register_function(executar_xquery_por_cidade, 'executar_xquery_por_cidade')
    server.register_function(executar_xquery_por_id, 'executar_xquery_por_id')
    print("Servidor XML-RPC iniciado...")
    server.serve_forever()
