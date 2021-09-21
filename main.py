#!/usr/bin/env python3
'''
Script en Python3 que utiliza el API de Google Maps
Obtiene la latitud y longitud de direcciones provistas por el usuario
El script puede leer un archivo TXT con una lista de direcciones o el usuario puede dar 1 direccion para buscar
Google Maps requiere de un token (API Key) 
El usuario debe contar con un user y password valido para autenticarse y obtener el Token
Autor: Raul Gomez - raul.agobe@gmail.com
'''

from getpass import getpass
import requests
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from tabulate import tabulate


def get_latlon(address, API_KEY):

    """Usa el API de Google Maps para obtener la latitud, longitud y direccion completa de una direccion provista por el usuario

    Args:
        address (str): Direccion dada por el usuario
        API_KEY (str): Token obtenido por la funcion get_token_mongodb

    Raises:
        SystemExit: Finaliza el programa si el API de google maps no esta disponible

    Returns:
        f_response (dict): Dictionario con los 3 parametros lat, lon y f_add
    """

    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

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


def get_address_list_txt(file_name):

    """Lee un archivo de texto y obtiene las direcciones a buscar

    Args:
        file_name (str): nombre del archivo con las direcciones

    Returns:
        address_list (lst): lista con las direcciones a buscar
    """

    with open(file_name) as file:
        read_file = file.readlines()
        address_list = [item.replace('\n', '') for item in read_file]

    return address_list


def get_token_mongodb():

    """Funcion para obtener el token de google maps de una base de datos en la nube Atlas MongoDB

    Returns:
        gm_token (str): Token de google maps
    """

    auth = False
    host = 'mongodb+srv://{}:{}@cluster0.pk2u7.mongodb.net/'
    arguments = '?tls=true&tlsAllowInvalidCertificates=true'
    uri_string = host + arguments

    while not auth:
        user = input('MongoDB user: ')
        pwd = getpass('MongoDB password:')
        try:
            mongodb_uri = uri_string.format(user, pwd)
            client = MongoClient(mongodb_uri)
            db = client['python_projects']
            col = db['api_tokens']
            gm_token = col.find_one({'name': 'google_maps_token'})['value']
            print('TOKEN obtenido!')
            auth = True
        except OperationFailure:
            print('user o password incorrecto, por favor intenta de nuevo')
            auth = False

    return gm_token


if __name__ == '__main__':

    """Corre las funciones si el archivo es ejecutado como script
    Utiliza tabulate para imprimir los resultados en formato de tabla
    """

    API_KEY = get_token_mongodb()

    try:
        address_list = get_address_list_txt('address_list.txt')
    except OSError:
        print('Archivo "address_list.txt" no encontrado')
        address_list = [input('Escribe la direccion a buscar: ')]

    results_list = list()
    results_list.append(('Valor buscado','Latitud','Longitud','Direccion'))
    for items in address_list:
        a = get_latlon(items, API_KEY)
        new_line = (items,a['lat'], a['lon'], a['f_add'])
        results_list.append(new_line)

    print('\n',tabulate(results_list,headers="firstrow",tablefmt="grid"),'\n')
