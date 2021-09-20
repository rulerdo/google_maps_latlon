# Google Maps Latitud y Longitud

## Descripcion
Script en Python3 que utiliza el API de Google Maps

Obtiene la latitud y longitud de direcciones provistas por el usuario

El script puede leer un archivo TXT con una lista de direcciones o el usuario puede dar 1 direccion para buscar

Google Maps requiere de un token (API Key), este script usa mi token personal guardada en un MongoDB por temas de privacidad

El usuario debe contar con un user y password valido para autenticarse y obtener el Token

## Instalacion

Para instalar clona el repositorio y utiliza el archivo requirements.txt para instalar los modulos necesarios

    pip install --upgrade -r requirements.txt

## Ejecucion

Usa el archivo main.py para ejecutar el script

    python3 main.py

Puedes editar el archivo address_list.txt para cambiar los parametros de busqueda o si lo eliminas el script te preguntara por una direccion a buscar en la terminal

## MongoDB

Es necesario contar con un usuario y contraseña para obtener el token, se sugiere contactar al autor para obtener un usuario temporal o reemplazar esta funcion con tu token personal

# Contacto

Autor: Raul Gomez

    raul.agobe@gmail.com
