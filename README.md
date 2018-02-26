# Python MeetUp 24 de Febrero de 2018 - Flask && Pandas
A continuacion se presentan los archivos utilizados en la presentación de Python MeetUp

### Contenido
1. [Acerca De](#acerca-de)
2. [Requerimientos](#requerimientos)
3. [Instalacion de Librerias Necesarias](#instalacion-de-librerias-necesarias)
4. [Configuración](#configuraci%C3%B3n)
5. [Uso](#uso)
6. [Licencia](#license)

## Acerca De
El dashboard que se presenta consta de tres vistas, las cuales son: Login, Ultimas 50 Canciones Escuchadas y el Dashboard como tal. El dashboard utiliza el login utilizando el API de Spotify, del cual se obtiene un token para realizar las consultas.
En la vista de Ultimas 50 Canciones Escuchadas, se muestran las ultimas 50 canciones escuchadas por el usuario en una tabla empleando el framework de Bootstrap para su visualización, se muestra el nombre de la canción, el artista y el uri de la canción.
En la vista de Dashboard se presenta la ultima cancion escuchada por el usuario, la ultima playlist creada por el usuario, el artista top del usuario y la cancion top del usuario con sus respectivos covers.

## Requerimientos
- CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE para utilizar la [API de Spotify](http://developer.spotify.com)
- Python 3 (compatible con Python 2.7)
- [Spotipy](http://spotipy.readthedocs.io/en/latest/)
- [Flask](http://flask.pocoo.org/)
- [Pandas](http://pandas.pydata.org/)
- [Pandas HighCharts](https://pypi.python.org/pypi/pandas-highcharts/)

## Instalacion de Librerias Necesarias
1. Install the requirements:
    - `pip install spotipy`
    - `pip install flask`
    - `pip install pandas`
    - `pip install pandas-highcharts`
2. [Descargar el codigo][source] y descomprimirlo (o clonarlo)
3. Crar una aplicación en [developer.spotify.com](developer.spotify.com)
4. Agregar los valores de CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE en el archivo `app.py`. Consultar la [Sección de Configuración](#configuraci%C3%B3n)

[source]: https://github.com/aleva90/Python-MeetUp-Flask-Febrero-2018/archive/master.zip

## Configuración
En el archivo `app.py`modificar las siguientes lineas:
- Ingresar los datos obtenidos de la App de Spotify de CLIENT_ID en: `SPOTIPY_CLIENT_ID = ''`
- Ingresar los datos obtenidos de la App de Spotify de CLIENT_SECRET en: `SPOTIPY_CLIENT_SECRET = ''`

## Uso
Ejecutar el script utilizando `python app.py`. Despues, desde el navegador, dirigirse a [http://localhost:8081](http://localhost:8081). Ingresar con las credenciales de tu cuenta de spotify y visualizar los datos.

## License
Spotify Dashboard is Copyright © 2018 by Alejandro López and licensed under the MIT license. You may do what you like with the software, but must include the [license and copyright notice](https://github.com/aleva90/Python-MeetUp-Flask-Febrero-2018/blob/master/LICENSE).
