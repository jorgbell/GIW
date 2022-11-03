"""
GIW 2022-23
Práctica NN
Grupo XX
Autores: XX, YY, ZZ,

(Nombres completos de los autores) declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
"""
from flask import Flask, request, session, render_template
import json
app = Flask(__name__)


asignaturas = []
id = 0


@app.route('/asignaturas', methods=['DELETE'])
def deleteAsignaturas():
    global asignaturas, id

    asignaturas = []
    id = 0

    return ('Borradas todas las asignaturas',204)


@app.route('/asignaturas', methods=['POST'])
def postAsignatura():
    asig = request.get_json()

    if 'nombre' not in asig or type(asig['nombre']) != str:
        return ('Error', 400)

    if 'numero_alumnos' not in asig or type(asig['numero_alumnos']) != int:
        return ('Error', 400)

    if 'horario' not in asig or type(asig['horario']) != list:
        return ('Error', 400)

    global id, asignaturas
    asig['id'] = id
    id+=1

    asignaturas.append(asig)

    return ("Todo bien", 201)


@app.route('/asignaturas', methods=['GET'])
def getAsignaturas():
    global asignaturas

    L = []
    for a in asignaturas:
        aId = a['id']
        L.append(f'/asignaturas/{aId}')
    
    return ({'asignaturas':L}, 200)


class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = "giw_clave_secreta"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()

