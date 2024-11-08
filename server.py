import socket
import xml.etree.ElementTree as ET
from lxml import etree
from GVL.xmlGeneration.csv_to_xml_converter import CSVtoXMLConverter

# Configuração do servidor
HOST = '127.0.0.1'
PORT = 65432

# Caminho para o arquivo XML
arquivo_xml = "data/Retail_Transactions_Dataset.xml"

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
        # Abrir e carregar o conteúdo do XML (cada vez que a função é chamada)
        with open(arquivo_xml, "r") as file:
            xml_content = file.read()

        xml_doc = etree.fromstring(xml_content.encode("utf-8"))

        # Executar a consulta XPath para cidade
        query = f"//Transaction[City = '{cidade}']"
        results = xml_doc.xpath(query)

        # Formatar os resultados para retornar como string
        result_texts = []
        for result in results:
            if isinstance(result, etree._Element):
                # Se o resultado for um elemento, inclui sua tag e texto
                transaction_details = [f"{child.tag}: {child.text}" for child in result]
                result_texts.append("\n".join(transaction_details))

        # Caso não haja resultados, retorna uma mensagem de "nenhum resultado encontrado"
        if result_texts:
            return "\n\n".join(result_texts)
        else:
            return f"Nenhuma transação encontrada para a cidade {cidade}."
    except Exception as e:
        return f"Erro ao executar consulta XPath por cidade: {e}"

def executar_xquery_por_id(id_transacao):
    try:
        # Abrir e carregar o conteúdo do XML (cada vez que a função é chamada)
        with open(arquivo_xml, "r") as file:
            xml_content = file.read()

        # Parse do conteúdo XML
        xml_doc = etree.fromstring(xml_content.encode("utf-8"))

        # Executar a consulta XPath para encontrar a transação pelo ID
        query = f"//Transaction[Transaction_ID = '{id_transacao}']"
        results = xml_doc.xpath(query)

        # Formatar os resultados para retornar como string
        result_texts = []
        if results:
            for result in results:
                # Se o resultado for um elemento, inclui sua tag e texto
                transaction_details = [f"{child.tag}: {child.text}" for child in result]
                result_texts.append("\n".join(transaction_details))

            # Retornar todos os detalhes das transações encontradas
            return "\n\n".join(result_texts)
        else:
            # Se não encontrar nenhuma transação, retornar mensagem apropriada
            return f"Nenhuma transação encontrada para o ID {id_transacao}."
    except Exception as e:
        return f"Erro ao executar consulta XPath por ID de transação: {e}"

def tratar_requisicao(opcao, dados=None):
    if opcao == '1':
        return executar_main_py()
    elif opcao == '2':
        return obter_duas_primeiras_transacoes()
    elif opcao == '3':
        return validate()
    elif opcao == '4':  # XQuery por cidade
        return executar_xquery_por_cidade(dados)
    elif opcao == '5':  # XQuery por ID de transação
        return executar_xquery_por_id(dados)
    elif opcao == '6':
        return "Servidor: A Encerrar conexão..."
    else:
        return "Servidor: Opção inválida!"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Servidor em execução. A aguardar conexão de cliente...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Conectado ao cliente em {addr}")
            while True:
                opcao = conn.recv(1024).decode()
                if not opcao:
                    break

                if opcao in ['4', '5']:
                    # Recebe dados adicionais (cidade ou ID de transação) para consultas
                    dados = conn.recv(1024).decode()

                    # Agora a consulta é processada de forma isolada para cada pesquisa
                    resposta = tratar_requisicao(opcao, dados)
                else:
                    resposta = tratar_requisicao(opcao)

                print(f"Opção recebida do cliente: {opcao}")

                conn.sendall(resposta.encode())

                # Após responder, aguarda a próxima opção
                if opcao == '6':
                    print("A encerrar a conexão com o cliente.")
                    break

        print("Servidor encerrado.")

if __name__ == "__main__":
    main()
