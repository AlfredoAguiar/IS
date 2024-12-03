import grpc
import transaction_service_pb2_grpc
import transaction_service_pb2

def convert_csv_to_xml(stub):
    response = stub.ConvertCSVToXML(transaction_service_pb2.Empty())
    print("ConvertCSVToXML:", response.message)

def get_first_two_transactions(stub):
    response = stub.GetFirstTwoTransactions(transaction_service_pb2.Empty())
    print("GetFirstTwoTransactions:", response.message)

def validate_xml(stub):
    response = stub.ValidateXML(transaction_service_pb2.Empty())
    print("ValidateXML:", response.message)

def query_by_city(stub):
    city = input("Enter the city to query transactions: ")
    response = stub.QueryByCity(transaction_service_pb2.QueryRequest(query=city))
    print(f"QueryByCity for {city}:", response.message)

def query_by_transaction_id(stub):
    transaction_id = input("Enter the transaction ID to query: ")
    response = stub.QueryByTransactionID(transaction_service_pb2.QueryRequest(query=transaction_id))
    print(f"QueryByTransactionID for {transaction_id}:", response.message)

def run():
    # Connect to the server
    channel = grpc.insecure_channel('localhost:50051')
    stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)

    while True:
        print("\nMenu:")
        print("1. Convert CSV to XML")
        print("2. Get First Two Transactions")
        print("3. Validate XML")
        print("4. Query Transactions by City")
        print("5. Query Transactions by Transaction ID")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            convert_csv_to_xml(stub)
        elif choice == "2":
            get_first_two_transactions(stub)
        elif choice == "3":
            validate_xml(stub)
        elif choice == "4":
            query_by_city(stub)
        elif choice == "5":
            query_by_transaction_id(stub)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    run()