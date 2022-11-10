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
from schema import *

app = Flask(__name__)


DIA_SCHEMA = Schema(
    {
        "dia": str,
        "hora_inicio": int,
        "hora_final": int
    }
)

def checkHorario(h):
    for d in h:
        if not DIA_SCHEMA.is_valid(d):
            return False

    return True

ASIG_SCHEMA = Schema({
    "nombre": str,
    "numero_alumnos": int,
    "horario": checkHorario
})

CAMPO_SCHEMA = Schema({
    Optional("nombre"): str,
    Optional("numero_alumnos"): int,
    Optional("horario"): checkHorario
})


asignaturas = []
id = 0


def esAsignaturaValida(asig):
    return ASIG_SCHEMA.is_valid(asig)


def esCampoValido(campoJson):
    return len(campoJson) == 1 and CAMPO_SCHEMA.is_valid(campoJson)


@app.route('/asignaturas', methods=['DELETE'])
def deleteAsignaturas():
    global asignaturas, id

    asignaturas = []
    id = 0

    return ('Borradas todas las asignaturas',204)


@app.route('/asignaturas', methods=['POST'])
def postAsignatura():
    asig = request.get_json()

    if not esAsignaturaValida(asig):
        return ('Asignatura no valida', 400)

    global id, asignaturas
    asig['id'] = id
    id+=1

    asignaturas.append(asig)

    return ("Asignatura creada con exito", 201)


@app.route('/asignaturas', methods=['GET'])
def getAsignaturas():
    global asignaturas

    alumnosGte = request.args.get('alumnos_gte')
    page = request.args.get('page')
    perPage = request.args.get('per_page')

    if (page and not perPage) or (not page and perPage): # Obligatorio que salgan los dos juntos
        return ('Los parametros page y per_page tienen que aparecer juntos', 400)

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
def deleteAsignatura(num):
    global asignaturas
    aux = [a for a in asignaturas if a['id'] != num]

    if len(aux) == len(asignaturas):  # No encontrado
        return ('Asignatura no encontrada', 404)

    asignaturas = aux
    return ('Asignatura borrada con exito', 204)


@app.route('/asignaturas/<int:num>', methods=['GET'])
def getAsignatura(num):
    global asignaturas
    
    # buscar la asignatura con id num
    for a in asignaturas:
        if a['id'] == num:
            return (a, 200)

    return ('Asignatura no encontrada', 404)


@app.route('/asignaturas/<int:num>', methods=['PUT'])
def replaceAsignatura(num):
    newAsig = request.get_json()

    if not esAsignaturaValida(newAsig):
        return ('Asignatura no valida', 400)

    global asignaturas

    # buscar la asignatura con id num
    oldAsig = None
    for a in asignaturas:
        if a['id'] == num:
            oldAsig = a

    if not oldAsig:
        return ('Asignatura no encontrada', 404)

    # copiar id
    newAsig['id'] = oldAsig['id']

    # actualizar la asig en la lista
    for i, a in enumerate(asignaturas):
        if a['id'] == num:
            asignaturas[i] = newAsig

    return ('Asignatura modificada con exito', 200)


@app.route('/asignaturas/<int:num>', methods=['PATCH'])
def replaceField(num):
    campoJson = request.get_json()

    if not esCampoValido(campoJson):
        return ('El json del campo no es valido', 400)

    # buscar la asignatura con id num
    asig = None
    global asignaturas
    for a in asignaturas:
        if a['id'] == num:
            asig = a

    if not asig:
        return ('Asignatura no encontrada', 404)

    # modificar el campo
    for i in campoJson:
        asig[i] = campoJson[i]

    return ('Campo actualizado con exito', 200)


@app.route('/asignaturas/<int:num>/horario', methods=['GET'])
def getHorario(num):
    global asignaturas
    
    # buscar la asignatura con id num
    for a in asignaturas:
        if a['id'] == num:
            return ({'horario': a['horario']}, 200)

    return ('Asignatura no encontrada', 404)


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

