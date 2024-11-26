import xmlrpc.client

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


def main():
    with xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}') as proxy:
        while True:
            exibir_menu()
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                response = proxy.executar_main_py()
                print(response)
            elif opcao == '2':
                response = proxy.obter_duas_primeiras_transacoes()
                print(response)
            elif opcao == '3':
                response = proxy.validate()
                print(response)
            elif opcao == '4':
                cidade = input("Digite o nome da cidade: ")
                response = proxy.executar_xquery_por_cidade(cidade)
                print(response)
            elif opcao == '5':
                transacao_id = input("Digite o ID da transação: ")
                response = proxy.executar_xquery_por_id(transacao_id)
                print(response)
            elif opcao == '6':
                print("Saindo...")
                break
            else:
                print("Opção inválida! Por favor, escolha uma opção válida.")


# Executa o cliente
if __name__ == "__main__":
    main()
