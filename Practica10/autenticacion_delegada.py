# -*- coding: utf-8 -*-

# GIW 2022-23
# Práctica 10
# Grupo 02
# Autores: Diego Revenga González, Raul Blas Ruiz, Jorge Bello Martin, Eva Lucas Leiro

# Diego Revenga González, Raul Blas Ruiz, Jorge Bello Martin y Eva Lucas Leiro 
# declaramos que esta solución es fruto exclusivamente
# de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
# obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
# con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
# actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from flask import Flask, request, session, render_template
# Resto de importaciones
import requests
import json
from urllib.parse import urlencode
from datetime import datetime


app = Flask(__name__)


# Credenciales. 
# https://developers.google.com/identity/openid-connect/openid-connect#appsetup
# Copiar los valores adecuados.
CLIENT_ID = '581456804150-kp3t1e3suqoon6rr1fhrrih2ccbtah6s.apps.googleusercontent.com'
CLIENT_SECRET = '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'

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
# https://developers.google.com/identity/openid-connect/openid-connect#authenticatingtheuser
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'

# token_info endpoint para extraer información de los tokens en depuracion, sin
# descifrar en local
# https://developers.google.com/identity/openid-connect/openid-connect#validatinganidtoken
TOKENINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'


@app.route('/login_google', methods=['GET'])
def login_google():
    descubimiento_json = json.loads(requests.request('GET', DISCOVERY_DOC).text)
    auth_base_url = descubimiento_json['authorization_endpoint']

    parametros = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': 'openid email',
        'redirect_uri': REDIRECT_URI,
        'nonce': '12345678901234567890'
    }

    auth_url = f'{auth_base_url}?{urlencode(parametros)}'

    return render_template('login.html', auth_url=auth_url)


@app.route('/token', methods=['GET'])
def token():
    respuesta = request.args

    descubimiento_json = json.loads(requests.request('GET', DISCOVERY_DOC).text)
    token_url = descubimiento_json['token_endpoint']

    parametros = {
        'code': respuesta['code'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    datos = json.loads(requests.request('POST', token_url, data=parametros).text)

    # Verificar JWT
    datos_verificados = json.loads(requests.request('GET', f'{TOKENINFO_ENDPOINT}?id_token={datos.get("id_token")}').text)
    
    if datos_verificados.get('iss') != 'https://accounts.google.com' and datos_verificados['iss'] != 'accounts.google.com':
        return ('Error al verificar el JWT', 500)
        
    if datos_verificados.get('aud') != CLIENT_ID:
        return ('Error al verificar el JWT', 500)

    if datetime.now() >= datetime.fromtimestamp(int(datos_verificados.get('exp'))):
        return ('Error al verificar el JWT', 500)

    # Extraer el email para usarlo en la pag de bienvenida
    email = datos_verificados.get('email')

    return render_template('welcome.html', email=email)

        
class FlaskConfig:
    '''Configuración de Flask'''
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = 'la_asignatura_de_giw'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()
