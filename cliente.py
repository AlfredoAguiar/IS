import socket

# Configuração do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432  # Porta de comunicação com o servidor


def exibir_menu():
    print("===== MENU =====")
    print("1. Converter CSV para XML")
    print("2. Exibir 2 linhas do XML gerado")
    print("3. Validar xml")
    print("4. XQuery - Consultar por cidade")
    print("5. XQuery - Consultar por ID de transação")
    print("6. Sair")
    print("================")


def enviar_opcao(client_socket, opcao, cidade=None):
    # Envia a opção selecionada para o servidor
    client_socket.sendall(opcao.encode())

    # Se a opção for 4 ou 5, podemos enviar mais informações (como a cidade ou ID)
    if opcao == '4':
        # Exibe lista de cidades para o cliente escolher
        print("""
        Escolha uma cidade:
        1. New York
        2. Houston
        3. Miami
        4. Seattle
        5. Atlanta
        6. Boston
        7. Dallas
        8. Chicago
        9. San Francisco
        10. Los Angeles
        """)
        cidade = input("Nome da cidade: ")
        client_socket.sendall(cidade.encode())

    elif opcao == '5':  # ID de transação
        transacao_id = input("ID da transação: ")
        client_socket.sendall(transacao_id.encode())

    # Recebe a resposta do servidor
    resposta = client_socket.recv(1024).decode()
    print("Resposta do servidor:", resposta)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Conecta ao servidor
        client_socket.connect((HOST, PORT))
        print("Conectado ao servidor.")

        while True:
            exibir_menu()
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                enviar_opcao(client_socket, opcao)
            elif opcao == '2':
                enviar_opcao(client_socket, opcao)
            elif opcao == '3':
                enviar_opcao(client_socket, opcao)
            elif opcao == '4':
                enviar_opcao(client_socket, opcao)  # Selecionar cidade
            elif opcao == '5':
                enviar_opcao(client_socket, opcao)  # Consultar por ID de transação
            elif opcao == '6':
                print("Encerrando conexão e saindo...")
                enviar_opcao(client_socket, opcao)  # Envia a opção de sair
                break  # Sai do loop e fecha a conexão
            else:
                print("Opção inválida! Por favor, escolha uma opção válida.")

    print("Conexão encerrada.")


# Executa o cliente
if __name__ == "__main__":
    main()