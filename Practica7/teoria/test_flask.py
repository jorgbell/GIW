"""
Ejemplo completo de Flask
"""
from flask import Flask, request, session, render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    """/ es una ruta válida"""
    return 'Soy la página principal'


@app.route('/partidos', methods=['GET'])
def partidos():
    """Ruta fija"""
    return 'Datos de todos los partidos'


@app.route('/partidos/<int:numero>', methods=['GET'])
def partido_concreto(numero):
    """Ruta con una variable numérica"""
    return f'Datos del partido número {numero}'


@app.route('/partidos/<int:numero>/goles', methods=['GET'])
def partido_goles(numero):
    """Ruta con variable numérica en la mitad"""
    return f'Goles del partido número {numero}'


@app.route('/partidos/<int:num_partido>/goles/<int:num_gol>', methods=['GET'])
def partido_gol_concreto(num_partido, num_gol):
    """Ruta con varias variables numéricas"""
    return f'Información del gol {num_gol} del partido número {num_partido}'


@app.route('/post', methods=['POST'])
def post():
    """Ruta para peticiones POST"""
    return 'Recibida peticion POST'


@app.route('/methods', methods=['GET', 'POST'])
def methods():
    """request.method indica el método HTTP utilizado"""
    if request.method == 'GET':
        return 'Recibida una petición GET'
    return 'Recibida una petición POST'


@app.route('/methods', methods=['DELETE'])
def methods_delete():
    """Se pueden definir varias rutas para el mismo recurso.
    Si una petición encaja en varias rutas, se elegirá la
    primera que encaje"""
    return 'Recibida una petición DELETE'


@app.route('/parametros', methods=['GET'])
def parametros():
    """request.args es un diccionario con los
    parámetros de la petición"""
    return f"Parámetros enviados: ini={request.args.get('ini')} fin={request.args.get('fin')}"


@app.route('/cabeceras', methods=['GET'])
def cabeceras():
    """request.headers es un diccionario con las
    cabeceras de la petición"""
    return f'Cabeceras de la petición: Accept={request.headers["Accept"]}'


@app.route('/login', methods=['POST'])
def login():
    """request.form es un diccionario con los datos
    enviados por formulario"""
    username = request.form['username']
    password = request.form['password']
    return f'Recibido user={username} pass={password}'


@app.route('/respuesta_html', methods=['GET'])
def respuesta_html():
    """Si la funcion devuelve una cadena, se genera
    una contestación que contiene contenido HTML
    con código de estado 200"""
    return "<html><h1>Bienvenido!!</h1></html>"


@app.route('/respuesta_json', methods=['GET'])
def respuesta_json():
    """Si se devuelve un diccionario, se generará
    una respuesta JSON de manera automática con
    código de estado 200"""
    dicc = {'nombre': 'pepe', 'edad': 55}
    return dicc


@app.route('/respuesta_status', methods=['GET'])
def respuesta_status():
    """si se devuelven 2 valores, el segundo será
    el código de estado"""
    return {'titulo': 'ninguno'}, 206


@app.route('/respuesta_cabeceras', methods=['GET'])
def respuesta_cabeceras():
    """Si se devuelve 3 valores, el tercer valor
    es un diccionario que representa las cabeceras
    que se añadirán en la contestación"""
    return (
        "<user><nombre>Pepe</nombre><edad>44</edad></user>",
        200, {'Content-Type': 'application/xml'})


@app.route('/ver_sesion', methods=['GET'])
def ver_sesion():
    """session es un diccionario que almacena el
    estado de la sesión y que se puede modificar.
    Para usar sesiones es imprescindible establecer
    SECRET_KEY en la configuración de Flask"""
    valor_actual = session.get('valor', 0)
    session['valor'] = valor_actual + 1
    return f'Valor en la sesión: {session["valor"]}'


@app.route('/plantilla_simple', methods=['GET'])
def plantilla_simple():
    """Renderizado de plantilla simple"""
    return render_template('saludo.html', name='José')


@app.route('/plantilla_condicional', methods=['GET'])
def plantilla_condicional():
    """Renderizado de plantilla condicional"""
    return render_template('saludo_admin.html',
                           admin=False, name='José')


@app.route('/plantilla_bucle', methods=['GET'])
def plantilla_bucle():
    """Renderizado de plantilla que recorre una lista.
    Más información sobre la sintaxis de plantillas en
    https://jinja.palletsprojects.com/en/2.11.x/templates/"""
    return render_template('saludo_lista.html',
                           productos=['pera', 'platano'])

@app.route('/logging', methods=['GET'])
def usar_log():
    """ Ejemplos de uso de log de Flask """
    app.logger.debug('Mensaje de depuración')
    app.logger.info('Mensaje informacion')
    app.logger.warning('Aviso de algo potencialmente malo')
    app.logger.error('Algo malo ha ocurrido')
    app.logger.critical('Situación crítica del servidor')
    return 'Se ha escrito en el log del servidor'
    
@app.route('/error', methods=['GET'])
def error():
    """ Devolver código de error """
    return "¡Todo mal!", 404


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
