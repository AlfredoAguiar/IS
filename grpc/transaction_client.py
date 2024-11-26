import grpc
import transaction_service_pb2_grpc
import transaction_service_pb2

def run():
    # Connect to the server
    channel = grpc.insecure_channel('localhost:50051')
    stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)

    # Request to convert CSV to XML
    response = stub.ConvertCSVToXML(transaction_service_pb2.Empty())
    print("ConvertCSVToXML:", response.message)

    # Request to get the first two transactions
    response = stub.GetFirstTwoTransactions(transaction_service_pb2.Empty())
    print("GetFirstTwoTransactions:", response.message)

    # Request to validate XML
    response = stub.ValidateXML(transaction_service_pb2.Empty())
    print("ValidateXML:", response.message)

    # Request to query transactions by city
    city = "Chicago"
    response = stub.QueryByCity(transaction_service_pb2.QueryRequest(query=city))
    print(f"QueryByCity for {city}:", response.message)

    # Request to query transactions by ID
    transaction_id = "1000000056"
    response = stub.QueryByTransactionID(transaction_service_pb2.QueryRequest(query=transaction_id))
    print(f"QueryByTransactionID for {transaction_id}:", response.message)

if __name__ == '__main__':
    run()