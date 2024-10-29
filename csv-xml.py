import csv
import xml.etree.ElementTree as ET

# Nome do arquivo CSV de entrada
input_file = 'books.csv'  # Substitua pelo caminho do seu arquivo CSV

# Criar a raiz do documento XML
library = ET.Element('library')

# Ler o arquivo CSV
with open(input_file, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Percorrer cada linha do CSV e adicionar ao XML
    for row in csv_reader:
        book = ET.SubElement(library, 'book')

        title = ET.SubElement(book, 'title')
        title.text = row['title']

        author = ET.SubElement(book, 'author')
        author.text = row['author']

        publication_date = ET.SubElement(book, 'publication_date')
        publication_date.text = row['publication_date']

        genre = ET.SubElement(book, 'genre')
        genre.text = row['genre']

        isbn = ET.SubElement(book, 'isbn')
        isbn.text = row['isbn']

# Criar o elemento árvore e escrever em um arquivo XML
tree = ET.ElementTree(library)
output_file = 'books.xml'  # Nome do arquivo XML de saída
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f'Dados escritos com sucesso em {output_file}')