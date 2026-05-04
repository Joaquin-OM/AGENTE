import os
from flask import Flask, render_template, request, session, redirect, url_for

# --- Carga opcional de variables de entorno ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Aviso: 'python-dotenv' no instalado. Se ignorara el archivo .env.")

# --- Agente interno ---
from agente import Agente

# --- IA generativa opcional ---
try:
    from IA import generar_respuesta
    IA_DISPONIBLE = True
except Exception as e:
    print("Aviso: IA generativa no disponible (" + str(e) + ").")
    print("       Para activarla: pip install transformers torch")
    IA_DISPONIBLE = False
    def generar_respuesta(pregunta):
        return ("Lo siento, no encontre informacion sobre eso en mi documento "
                "y la IA generativa no esta disponible.")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_por_defecto_no_segura')

ruta_documento = os.path.join(os.path.dirname(__file__), "documento.txt")
mi_agente = Agente(ruta_documento)


def procesar_mensaje(mensaje_usuario):
    respuesta_agente = mi_agente.responder(mensaje_usuario)
    if "Lo siento, no he encontrado" in respuesta_agente:
        try:
            return generar_respuesta(mensaje_usuario)
        except Exception as e:
            return "Hubo un error al generar la respuesta con IA: " + str(e)
    return respuesta_agente


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'historial' not in session:
        session['historial'] = []

    mensaje_bienvenida = "Hola! Soy tu asistente virtual. En que puedo ayudarte?"

    if request.method == 'POST':
        pregunta_usuario = request.form.get('pregunta', '').strip()
        if pregunta_usuario:
            respuesta_chatbot = procesar_mensaje(pregunta_usuario)
            session['historial'].append({
                'usuario': pregunta_usuario,
                'bot': respuesta_chatbot
            })
            session.modified = True

    return render_template(
        'index.html',
        mensaje_bienvenida=mensaje_bienvenida,
        historial=session['historial']
    )


@app.route('/limpiar')
def limpiar():
    session.pop('historial', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    if debug_mode:
        print("Iniciando en DESARROLLO en puerto " + str(port))
        print("Abre http://127.0.0.1:" + str(port))
        app.run(debug=True, port=port)
    else:
        print("Iniciando en PRODUCCION en puerto " + str(port))
        try:
            from waitress import serve
            serve(app, host='0.0.0.0', port=port)
        except ImportError:
            print("Aviso: 'waitress' no instalado, usando servidor Flask.")
            app.run(debug=False, host='0.0.0.0', port=port)
