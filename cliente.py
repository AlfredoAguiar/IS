import socket

# Configuração do cliente
HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Conectado ao servidor em", HOST, "porta", PORT)

    while True:
        file_path = input("Nome do ficheiro XML(books.xml) ou 'sair' para fechar: ")

        if file_path.lower() == "sair":
            client_socket.sendall(file_path.encode('utf-8'))
            print("Comando 'sair' enviado. Encerrando conexão.")
            break

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_data = file.read()
        except FileNotFoundError:
            print(f"Erro: O ficheiro '{file_path}' não foi encontrado.")
            continue

        # Conteúdo do XML do servidor
        client_socket.sendall(xml_data.encode('utf-8'))
        print(f"Conteúdo do ficheiro '{file_path}' enviado ao servidor.")

        # Resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')
        print("Resposta do servidor:")
        print(response)

    print("Conexão encerrada.")