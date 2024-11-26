import time
from concurrent import futures

import grpc
import xml.etree.ElementTree as ET
from lxml import etree
from grpc import RpcError
import transaction_service_pb2
import transaction_service_pb2_grpc

# Logic to convert CSV to XML (placeholder for actual logic)
def convert_csv_to_xml():
    try:
        # CSV to XML conversion logic goes here
        return "CSV to XML conversion successful."
    except Exception as e:
        raise RpcError(f"Error during CSV to XML conversion: {str(e)}")

# Logic to get the first two transactions from the XML
def get_first_two_transactions():
    try:
        tree = ET.parse("..//data/Retail_Transactions_Dataset.xml")
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
        raise RpcError(f"Error reading XML: {str(e)}")

# Logic to validate the XML file
def validate_xml():
    try:
        with open("..//data/Retail_Transactions_Dataset.xml", "r") as file:
            xml_content = file.read()
        schema_path = "..//GVL/xmlValidate/schema.xsd"
        xml_doc = etree.fromstring(xml_content)
        xml_schema = etree.XMLSchema(file=schema_path)

        if xml_schema.validate(xml_doc):
            return "XML is valid."
        else:
            return f"XML is not valid.\nErrors: {xml_schema.error_log}"
    except Exception as e:
        raise RpcError(f"Error validating XML: {str(e)}")

# Logic to query by city
def query_by_city(city):
    try:
        with open("..//data/Retail_Transactions_Dataset.xml", "r") as file:
            xml_content = file.read()

        xml_doc = etree.fromstring(xml_content.encode("utf-8"))
        query = f"//Transaction[City = '{city}']"
        results = xml_doc.xpath(query)

        result_texts = []
        for result in results:
            if isinstance(result, etree._Element):
                transaction_details = [f"{child.tag}: {child.text}" for child in result]
                result_texts.append("\n".join(transaction_details))

        if result_texts:
            return "\n\n".join(result_texts)
        else:
            return f"No transactions found for city {city}."
    except Exception as e:
        raise RpcError(f"Error querying by city: {str(e)}")

# Logic to query by transaction ID
def query_by_transaction_id(transaction_id):
    try:
        with open("..//data/Retail_Transactions_Dataset.xml", "r") as file:
            xml_content = file.read()

        xml_doc = etree.fromstring(xml_content.encode("utf-8"))
        query = f"//Transaction[Transaction_ID = '{transaction_id}']"
        results = xml_doc.xpath(query)

        result_texts = []
        if results:
            for result in results:
                transaction_details = [f"{child.tag}: {child.text}" for child in result]
                result_texts.append("\n".join(transaction_details))

            return "\n\n".join(result_texts)
        else:
            return f"No transactions found for ID {transaction_id}."
    except Exception as e:
        raise RpcError(f"Error querying by transaction ID: {str(e)}")

# gRPC service class implementation
class TransactionService(transaction_service_pb2_grpc.TransactionServiceServicer):

    def ConvertCSVToXML(self, request, context):
        result = convert_csv_to_xml()
        return transaction_service_pb2.StringResponse(message=result)

    def GetFirstTwoTransactions(self, request, context):
        result = get_first_two_transactions()
        return transaction_service_pb2.StringResponse(message=result)

    def ValidateXML(self, request, context):
        result = validate_xml()
        return transaction_service_pb2.StringResponse(message=result)

    def QueryByCity(self, request, context):
        result = query_by_city(request.query)
        return transaction_service_pb2.StringResponse(message=result)

    def QueryByTransactionID(self, request, context):
        result = query_by_transaction_id(request.query)
        return transaction_service_pb2.StringResponse(message=result)

# Start the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_service_pb2_grpc.add_TransactionServiceServicer_to_server(TransactionService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started, listening on port 50051...")
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)  # Keep server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()