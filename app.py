#Importando Librerias Necesarias para utilizar Flask
from flask import Flask, render_template, json, request, flash, session
from flask import redirect, jsonify, make_response
#Importando Librerias para utilizar el API de Spotify
import spotipy.util as util
from spotipy import oauth2
import spotipy
#Importando Libreria Pandas
import pandas as pd
#Importando Libreria Pandas-HighCharts
import pandas_highcharts.core

#Creando una instancia de Flask
# __name__ es una variable especial que obtiene como valor la cadena "__main__"
# cuando estás ejecutando el script.
app = Flask(__name__)
#Se declara una clave secreta. Todo lo que requiera cifrado
#(para protegerse contra la manipulación por parte de los atacantes) requiere
#la configuración de la clave secreta.
app.secret_key = 'random string'
#Datos para utilizar el API de Spotify, estos se pueden obtener desde:
#https://beta.developer.spotify.com/dashboard creando una app
username = ''
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8081/callback'
SCOPE = 'user-read-private user-read-email user-read-playback-state user-read-currently-playing user-library-read user-top-read user-read-recently-played'
CACHE = '.spotipyoauthcache'


#Funcion que devuelve la url del cover de la ultima cancion escuchada por
#el usuario
def read_lastsongimg():
    #sp es una instancia de la Spotipy
    #Para mayor informacion acerca de Spotipy visitar
    #http://spotipy.readthedocs.io/en/latest/
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_recently_played(limit=50)
    return results['items'][0]['track']['album']['images'][0]['url']


#Funcion que devuelve el nombre de la ultima cancion escuchada por el usuario
def read_lastsong():
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_recently_played(limit=50)
    return results['items'][0]['track']['name']


#Funcion que devuelve la url del cover de la ultima playlist creada por
#el usuario
def read_lastplaylistimg():
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_playlists(limit=1)
    return results['items'][0]['images'][0]['url']


#Funcion que devuelve el nombre de la ultima playlist creada por el usuario
def read_lastplaylist():
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_playlists(limit=1)
    return results['items'][0]['name']


#Funcion que devuelve la url del cover del artista top escuchado por el usuario
def read_topartistimg():
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_top_artists(limit=1)
    return results['items'][0]['images'][0]['url']


#Funcion que devuelve el nombre del artista top escuchado por el usuario
def read_topartist():
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_top_artists(limit=1)
    return results['items'][0]['name']


#Funcion que devuelve la url del cover de la cancion top escuchada por el usuario
def read_topsongimg():
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_top_tracks(limit=1)
    return results['items'][0]['album']['images'][0]['url']


#Funcion que devuelve el nombre de la cancion top escuchada por el usuario
def read_topsong():
    sp = spotipy.Spotify(auth=session['user'])
    results = sp.current_user_top_tracks(limit=1)
    return results['items'][0]['name']


#Esa función está asignada a la URL de inicio '/'.
#Eso significa que cuando el usuario navega a localhost: 8081,
#la función de inicio se ejecutará y devolverá su resultado en la página web.
@app.route('/')
def main():
    #Verifica si existe un usuario loggeado en la aplicacion, si es asi
    #despliega el dashboard, en caso contrario devuelve la pantalla de login
    if session.get('user'):
        #Se emplea pandas para leer un archivo CSV para utilizar con Highcharts
        df = pd.read_csv('csv/test.csv', index_col='Date', parse_dates=True)
        #Se crea un dataSet con pandas highcharts para ser enviada a la pagina web
        dataSet = pandas_highcharts.core.serialize(
            df, render_to='my-chart', output_type='json', title='Test')
        #se retorna utilizando jinja2 el template dspotify.html con la grafica como parametro JSON
        return render_template('dspotify.html', chart=dataSet)
    else:
        #en caso no exista un usuario loggeado devuelve el template de login
        return render_template('login.html')

#Esa función está asignada a la URL de logout '/logout'
@app.route('/logout')
def logout():
    #Elimina el usuario y lo redirige a la pantalla de inicio
    session.pop('user', None)
    return redirect('/')


#Esa función está asignada a la URL de spotify para obtener un token '/callSpotify'
#empleando el metodo POST
@app.route('/callSpotify', methods=['POST'])
def callSpotify():
    #Redirige el usuario para que se autentique con las credenciales de Spotify
    return redirect("https://accounts.spotify.com/authorize?client_id=23278973c92a4269829378f645f382b2&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8081%2Fcallback&scope=user-library-read+user-read-currently-playing+user-read-email+user-read-playback-state+user-read-private+user-read-recently-played+user-top-read")


#Esa función está asignada a la Redireccion de la URL de Spotify especificada en la api de Spotify
@app.route("/callback")
def callback():
    #El api devuelve un codigo 
    code = request.args['code']
    #Si el codigo no es nulo, empleamos OAUTH2 para llamar al API de Spotify cada vez que realicemos una consulta
    if len(code) > 0:
        if (code != ''):
            #Creamos un objeto para autenticarnos empleando los datos de nuestra app de Spotify
            spAuth = spotipy.oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,
                                                 SPOTIPY_REDIRECT_URI, state=None, scope=SCOPE, cache_path=None, proxies=None)
            #Obtenemos el token para emplear el Api de Spotify
            token = spAuth.get_access_token(code)
            #Empleamos el token de spotify para identificar la sesion de los usuarios
            session['user'] = token['access_token']
            #Ya al estar autenticados se redirigen a los usuarios hacia la pagina de Table
            return redirect('/table')
        else:
            #En caso de no obtener un codigo desde el login de Spotify redireccionamos
            #al usuario a la pagina de inicio y desplegamos un mensaje flotante
            #empleando la funcion flash
            flash('Email o Contraseña Incorrectos')
            return render_template('/')
    else:
        flash('Email o Contraseña Incorrectos')
        return render_template('/')


#Esa función está asignada a la URL de Table '/table', que muestra las ultimas 50
#canciones escuchadas por el usuario
@app.route('/table')
def table():
    #Si hay un usuario registrado nos regresa una pagina mostrando las ultimas 50 canciones del usuario
    if session.get('user'):
        #Creamos un objeto Spotify empleando el token obtenido, para realizar las consultas
        sp = spotipy.Spotify(auth=session['user'])
        results = sp.current_user_recently_played(limit=50)
        items = []
        columns = []
        #Creamos un diccionario con los resultados obtenidos
        for item in results['items']:
            items.append({
                "artist": item['track']['artists'][0]['name'],
                "song": item['track']['name'],
                "uri": """<a href=" """ + item['track']['uri'] + """ ">""" + item['track']['uri'] + """</a>"""
            })
        #En base al diccionario obtenido creamos un DataFrame empleando Pandas
        df = pd.DataFrame(items)
        #Obtenemos los valores de las columnas para agregarles etiquetas para su uso con Bootstrap
        col = df.columns.values
        #Agregamos las etiquetas a las columnas
        for i in range(len(col)):
            part = dict([("field", col[i]), ("title", col[i]), ("sortable", True)])
            columns.append(part)
        #Devolvemos un diccionario para que sea convertido en JSON
        data = df.to_dict('records')
        # return df.to_html()
        #Retornamos el template de Tables con los parametros de data, columnas y titulo
        return render_template("tables.html", data=data, columns=columns, title='Spotify Last Songs')
    else:
        flash('Accesso Denegado')
        return render_template('table.html')


#Esa función está asignada a la URL '/_calldata' que actualiza los datos en el dashboard
@app.route("/_calldata")
def _calldata():
    #Llama a las funciones antes descritas para retornar los valores al Dashboard
    lastsongimg = read_lastsongimg()
    lastsong = read_lastsong()
    lastplaylistimg = read_lastplaylistimg()
    lastplaylist = read_lastplaylist()
    topartistimg = read_topartistimg()
    topartist = read_topartist()
    topsongimg = read_topsongimg()
    topsong = read_topsong()
    #Retornamos los datos en formato JSON
    return jsonify(lastsong=lastsong, lastsongimg=lastsongimg, lastplaylistimg=lastplaylistimg, lastplaylist=lastplaylist, topartistimg=topartistimg, topartist=topartist, topsongimg=topsongimg, topsong=topsong)


#Algo que debes saber es que Python asigna el nombre "__main__" al script cuando se
#ejecuta el script. Si el script se importa desde otro script, el script conserva el
#nombre (por ejemplo, hello.py).
#En este caso que empleamos Flask, estamos ejecutando el script. Por lo tanto,
#__name__ será igual a "__main__". Eso significa que se cumple el condicional IF y
#se ejecutará el método app.run (). Esta técnica permite que el programador tenga control
#sobre el comportamiento del script.
if __name__ == '__main__':
    #Host = 0.0.0.0 indicandole que se puede acceder desde cualquier direccion IP
    #el puerto que se emplea es el 8081, este puede ser cambiado por uno que se
    #encuentre en el rango de 5000 - 9999
    app.run(host='0.0.0.0', port=8081)
