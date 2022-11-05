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

    alumnosGte = request.args.get('alumnos_gte')
    page = request.args.get('page')
    perPage = request.args.get('per_page')

    if (page and not perPage) or (not page and perPage): # Obligatorio que salgan los dos juntos
        return ('BAD REQUEST', 400)

    asignaturasFiltradas = asignaturas

    # filtrar por numero de alumnos
    if alumnosGte:
        alumnosGte = int(alumnosGte)
        asignaturasFiltradas = filter((lambda a: a['numero_alumnos'] >= alumnosGte), asignaturasFiltradas)

    numeroAsigFiltradasGte = len(asignaturasFiltradas)

    # paginar
    if page and perPage:
        page = int(page)
        perPage = int(perPage)

        ini = (page - 1) * perPage
        fin = ini + perPage

        asignaturasFiltradas = asignaturasFiltradas[ini:fin]

    # generar links de las asignaturas
    asigLinks = []
    for a in asignaturasFiltradas:
        aId = a['id']
        asigLinks.append(f'/asignaturas/{aId}')
    
    if len(asignaturasFiltradas) != numeroAsigFiltradasGte:
        return ({'asignaturas':asigLinks}, 206) # partial content

    return ({'asignaturas':asigLinks}, 200) # OK


@app.route('/asignaturas/<int:num>', methods=['DELETE'])
def getAsignatura(num):
    global asignaturas
    aux = [a for a in asignaturas if a['id'] != num]

    if len(aux) == len(asignaturas):  # No encontrado
        return ('NOT FOUND', 404)

    asignaturas = aux
    return ('NO CONTENT', 204)


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

