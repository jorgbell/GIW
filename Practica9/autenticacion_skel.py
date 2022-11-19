# -*- coding: utf-8 -*-

# GIW 2022-23
# Práctica 09
# Grupo 02
# Autores: Diego Revenga González, Raul Blas Ruiz, Jorge Bello Martin, Eva Lucas Leiro


from flask import Flask, request, session, render_template
from mongoengine import connect, Document, StringField, EmailField
# Resto de importaciones
import random, string
from argon2 import PasswordHasher, profiles


app = Flask(__name__)
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
    ...
 
           
@app.route('/login', methods=['POST'])
def login():
    nickname = request.form['nickname']
    password = request.form['password']
    
    # Si el usuario no existe:
    if not (user := [u for u in User.objects() if u.user_id == nickname]):
        return render_template('wrongCredentials.html')

    saved_hash = user[0].passwd
    full_name = user[0].full_name

    ph = PasswordHasher().from_parameters(profiles.RFC_9106_LOW_MEMORY)

    try:
        ph.verify(saved_hash, password)
        return render_template('welcomeUser.html', name = full_name)
    except:
        return render_template('wrongCredentials.html')


##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    ...
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    ...
  

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
