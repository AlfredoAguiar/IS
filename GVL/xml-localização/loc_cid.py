import xml.etree.ElementTree as ET


def adicionar_coordenadas_a_transacao(transacao, latitude, longitude):
    coordenadas = ET.SubElement(transacao, "Coordinates")
    latitude_element = ET.SubElement(coordenadas, "Latitude")
    latitude_element.text = str(latitude)
    longitude_element = ET.SubElement(coordenadas, "Longitude")
    longitude_element.text = str(longitude)


tree_transacoes = ET.parse("../../../data/Retail_Transactions_Dataset_transformed.GVL")
root_transacoes = tree_transacoes.getroot()

tree_coordenadas = ET.parse("output_with_coordinates.xml")
root_coordenadas = tree_coordenadas.getroot()

coordenadas_cidades = {}
for cidade_element in root_coordenadas.findall(".//City"):
    cidade_nome = cidade_element.text.strip()

    coordenadas_element = cidade_element.find("Coordinates")

    if coordenadas_element is not None:
        latitude_element = coordenadas_element.find("Latitude")
        longitude_element = coordenadas_element.find("Longitude")

        if latitude_element is not None and longitude_element is not None:
            latitude = float(latitude_element.text)
            longitude = float(longitude_element.text)

            coordenadas_cidades[cidade_nome] = (latitude, longitude)

for transacao in root_transacoes.findall(".//Transaction"):
    cidade_element = transacao.find("City")
    cidade = cidade_element.text.strip() if cidade_element is not None else None

    if cidade in coordenadas_cidades:
        latitude, longitude = coordenadas_cidades[cidade]
        adicionar_coordenadas_a_transacao(transacao, latitude, longitude)

tree_transacoes.write("../../../docker/volumes/data/Retail_Transactions_Dataset_loc.GVL")
