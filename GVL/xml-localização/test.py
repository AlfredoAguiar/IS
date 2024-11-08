import requests


def get_coordinates(city):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city,
        'format': 'json',
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            # Obtém as coordenadas da primeira correspondência (assumindo a correspondência mais relevante)
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
    else:
        print(f"Erro na solicitação: {response.status_code}")

    return None, None


# Exemplo de uso para a cidade de Nova York
city_name = "New York"
latitude, longitude = get_coordinates(city_name)

if latitude is not None and longitude is not None:
    print(f"Coordenadas para {city_name}: Latitude {latitude}, Longitude {longitude}")
else:
    print(f"Não foi possível obter as coordenadas para {city_name}")