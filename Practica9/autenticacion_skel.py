# -*- coding: utf-8 -*-

# GIW 2022-23
# Práctica 09
# Grupo 02
# Autores: Diego Revenga González, Raul Blas Ruiz, Jorge Bello Martin, Eva Lucas Leiro

# Diego Revenga González, Raul Blas Ruiz, Jorge Bello Martin y Eva Lucas Leiro 
# declaramos que esta solución es fruto exclusivamente
# de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
# obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
# con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
# actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


from flask import Flask, request, session, render_template
from mongoengine import connect, Document, StringField, EmailField
# Resto de importaciones
import random, string
from argon2 import PasswordHasher, profiles
import pyotp
from pyotp import utils
from flask_qrcode import QRcode


app = Flask(__name__)
QRcode(app)
connect('giw_auth')


# Clase para almacenar usuarios usando mongoengine
class User(Document):
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)


##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#

# Las contraseñas se guardan en la base de datos encriptandolas con argon2. 
# Este algoritmo ya añade sal, asi que las contraseñas cortas son igual de seguras.
# Además usa memoria y tarda tiempo en hacer el hash, por lo que dificulta hacer ataques de fuerza bruta.


@app.route('/signup', methods=['POST'])
def signup():
    nickname = request.form['nickname']
    full_name = request.form['full_name']
    country = request.form['country']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    # Si las contraseñas no coinciden:
    if password != password2:
        return render_template('passwordsDontMatch.html')

    # Si ya existe el nickname:
    if [u for u in User.objects() if u.user_id == nickname]:
        return render_template('alreadyExistingNickname.html')

    # Encriptar password
    ph = PasswordHasher().from_parameters(profiles.RFC_9106_LOW_MEMORY)
    passEncrypted = ph.hash(password)

    # Guardar usuario en la base de datos
    new_user = User(user_id=nickname, full_name=full_name, country=country, email=email, passwd=passEncrypted)
    new_user.save()

    return render_template('welcomeUser.html', name = full_name)


@app.route('/change_password', methods=['POST'])
def change_password():
    nickname = request.form['nickname']
    old_password = request.form['old_password']
    new_password = request.form['new_password']

    # Si no existe el nickname:
    if not (user := [u for u in User.objects() if u.user_id == nickname]):
        return render_template('wrongCredentials.html')

    user = user[0]

    ph = PasswordHasher().from_parameters(profiles.RFC_9106_LOW_MEMORY)
    try:
        ph.verify(user.passwd, old_password)
        user.passwd = ph.hash(new_password)
        user.save()
        return render_template('passwordChanged.html', nickname = user.full_name)
    except:
        return render_template('wrongCredentials.html')
 
           
@app.route('/login', methods=['POST'])
def login():
    nickname = request.form['nickname']
    password = request.form['password']
    
    # Si el usuario no existe:
    if not (user := [u for u in User.objects() if u.user_id == nickname]):
        return render_template('wrongCredentials.html')

    user = user[0]

    ph = PasswordHasher().from_parameters(profiles.RFC_9106_LOW_MEMORY)
    try:
        ph.verify(user.passwd, password)
    except:
        return render_template('wrongCredentials.html')

    return render_template('welcomeUser.html', name = user.full_name)

##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#

# La semilla aleatoria (el secreto) se genera con la librería pyotp. Esto se hace por cada usuario registrado.
# La url de registro se genera con la librería pyotp.utils, indicandole el secreto y el nombre de la app, que luego aparecera en google authenticator.
# El codigo qr se genera usando la libreria flask_QRcode, a partir de la url.


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    nickname = request.form['nickname']
    full_name = request.form['full_name']
    country = request.form['country']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    # Si las contraseñas no coinciden:
    if password != password2:
        return render_template('passwordsDontMatch.html')

    # Si ya existe el nickname:
    if [u for u in User.objects() if u.user_id == nickname]:
        return render_template('alreadyExistingNickname.html')

    # Encriptar password
    ph = PasswordHasher().from_parameters(profiles.RFC_9106_LOW_MEMORY)
    passEncrypted = ph.hash(password)

    # Generar secreto TOTP
    secret = pyotp.random_base32()

    # Guardar usuario en la base de datos
    new_user = User(user_id=nickname, full_name=full_name, country=country, email=email, passwd=passEncrypted, totp_secret=secret)
    new_user.save()

    secret_url = utils.build_uri(secret=secret, name='Practica9 GIW')

    return render_template('totpConfigurator.html', nickname=nickname, secret=secret, secret_url=secret_url)
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    nickname = request.form['nickname']
    password = request.form['password']
    totp = request.form['totp']
    
    # Si el usuario no existe:
    if not (user := [u for u in User.objects() if u.user_id == nickname]):
        return render_template('wrongCredentials.html')

    user = user[0]

    ph = PasswordHasher().from_parameters(profiles.RFC_9106_LOW_MEMORY)
    try:
        # Comprobar contraseña
        ph.verify(user.passwd, password)
    except:
        return render_template('wrongCredentials.html')
    
    # Comprobar totp
    intern_totp = pyotp.TOTP(user.totp_secret)
    if not intern_totp.verify(totp):
        return render_template('wrongCredentials.html')
  
    return render_template('welcomeUser.html', name = user.full_name)


class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = 'la_asignatura_de_giw'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    # User.drop_collection()

    app.config.from_object(FlaskConfig())
    app.run()
