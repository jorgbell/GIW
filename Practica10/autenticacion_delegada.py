# -*- coding: utf-8 -*-

# GIW 2022-23
# Práctica 09
# Grupo 02
# Autores: Diego Revenga González, Raul Blas Ruiz, Jorge Bello Martin, Eva Lucas Leiro

from flask import Flask, request, session, render_template
# Resto de importaciones
import requests
import json
from urllib.parse import urlencode


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

DESCUBRIMIENTO_URL = 'https://accounts.google.com/.well-known/openid-configuration'


@app.route('/login_google', methods=['GET'])
def login_google():
    descubimiento_json = json.loads(requests.request('GET', DESCUBRIMIENTO_URL).text)
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

    descubimiento_json = json.loads(requests.request('GET', DESCUBRIMIENTO_URL).text)
    token_url = descubimiento_json['token_endpoint']

    parametros = {
        'code': respuesta['code'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    datos = json.loads(requests.request('POST', token_url, data=parametros).text)

    # VERIFICAR EL JWT
    # SACAR EN UNA PAGINA LA INFO DEL USUARIO

    return datos

        
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
