import socket
from xml.dom.minidom import parseString


# Função para analisar e construir uma resposta detalhada com a estrutura completa do XML
def parse_and_build_detailed_response(xml_data):
    dom_tree = parseString(xml_data)
    response = "XML Recebido:\n"

    def build_dom_tree(element, indent=""):
        nonlocal response
        response += f"{indent}Elemento: <{element.tagName}>\n"

        if element.hasAttributes():
            attrs = element.attributes.items()
            for attr_name, attr_value in attrs:
                response += f"{indent}  Atributo: {attr_name}='{attr_value}'\n"

        for child in element.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                build_dom_tree(child, indent + "  ")
            elif child.nodeType == child.TEXT_NODE and child.nodeValue.strip():
                response += f"{indent}  Texto: {child.nodeValue.strip()}\n"

    build_dom_tree(dom_tree.documentElement)
    return response


# Função para extrair informações detalhadas de cada livro
def extract_books_info(xml_data):
    dom_tree = parseString(xml_data)
    response = "Books\n"
    books = dom_tree.getElementsByTagName("book")
    for book in books:
        title = book.getElementsByTagName("title")[0].firstChild.nodeValue
        author = book.getElementsByTagName("author")[0].firstChild.nodeValue
        pub_date = book.getElementsByTagName("publication_date")[0].firstChild.nodeValue
        genre = book.getElementsByTagName("genre")[0].firstChild.nodeValue
        isbn = book.getElementsByTagName("isbn")[0].firstChild.nodeValue

        response += (
            f"Título: {title}, Autor: {author}, Data de Publicação: {pub_date}, "
            f"Gênero: {genre}, ISBN: {isbn}\n"
        )

    return response


# Configuração do servidor
HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Servidor a escutar no endereço", HOST, "e porta", PORT)

    conn, addr = server_socket.accept()
    with conn:
        print("Conexão estabelecida com", addr)

        while True:
            data = conn.recv(1024)
            if not data:
                break  # Encerra se não há dados

            xml_data = data.decode('utf-8').strip()
            if xml_data.lower() == "sair":
                print("Comando 'sair' recebido. Encerrando conexão.")
                break

            print("Dados XML recebidos do cliente:")
            print(xml_data)

            detailed_response = parse_and_build_detailed_response(xml_data)
            print("\nEstrutura detalhada do XML:")
            print(detailed_response)

            client_response = extract_books_info(xml_data)
            conn.sendall(client_response.encode('utf-8'))
            print("\nResposta enviada ao cliente:")
            print(client_response)

        print("Conexão fechada com", addr)