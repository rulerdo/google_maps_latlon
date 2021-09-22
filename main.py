#!/usr/bin/env python3
'''
Script en Python3 que utiliza el API de Google Maps
Obtiene la latitud y longitud de direcciones provistas por el usuario
Reemplaza el valor de API_KEY con tu propio token de google maps
Autor: Raul Gomez - raul.agobe@gmail.com
'''

import requests
from tabulate import tabulate
import os


def get_latlon(address):

    """Usa el API de Google Maps para obtener la latitud, longitud y direccion completa de una direccion provista por el usuario

    Args:
        address (str): Direccion dada por el usuario

    Raises:
        SystemExit: Finaliza el programa si el API de google maps no esta disponible

    Returns:
        response (dict): Dictionario con los 3 parametros lat, lon y f_add
    """

    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    API_KEY = os.environ.get('GOOGLEMAPSTOKEN')
    parameters = {'address': address, 'sensor': 'false', 'key': API_KEY}

    try:
        req = requests.get(GOOGLE_MAPS_API_URL, params=parameters)
        response = req.json()
        result = response['results'][0]
        latitude = result['geometry']['location']['lat']
        longitude = result['geometry']['location']['lng']
        f_address = result['formatted_address']

        response = {'lat': latitude, 'lon': longitude, 'f_add': f_address}

        return response

    except requests.exceptions.RequestException as e:
        print('API de Google Maps no disponible, por favor intenta de nuevo en unos segundos')
        raise SystemExit(e)


if __name__ == '__main__':

    user_input = input('Ingresa las direcciones a buscar separadas por comas: ')
    address_list = user_input.split(',')
    results_list = list()
    results_list.append(('Valor buscado','Latitud','Longitud','Direccion'))

    for items in address_list:
        a = get_latlon(items)
        new_line = (items,a['lat'], a['lon'], a['f_add'])
        results_list.append(new_line)

    print('\n',tabulate(results_list,headers="firstrow",tablefmt="grid"),'\n')
