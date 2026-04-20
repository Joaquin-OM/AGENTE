import os
from flask import Flask, render_template, request, session, redirect, url_for
from agente import Agente

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesion' # Necesario para usar session

# Instanciar el agente una sola vez al cargar la aplicación Flask
ruta_documento = os.path.join(os.path.dirname(__file__), "documento.txt")
mi_agente = Agente(ruta_documento)

# --- FASE 2: Controlador Modular ---
def procesar_mensaje(mensaje_usuario):
    """
    Controlador para procesar el mensaje del usuario conectando a tu Agente.
    """
    respuesta = mi_agente.responder(mensaje_usuario)
    return respuesta

# --- FASE 1: Configuración de Flask y Rutas ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'historial' not in session:
        session['historial'] = []
    
    # Mensaje de bienvenida inicial
    mensaje_bienvenida = "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"

    if request.method == 'POST':
        pregunta_usuario = request.form.get('pregunta', '').strip()
        
        if pregunta_usuario:
            respuesta_chatbot = procesar_mensaje(pregunta_usuario)
            # Guardamos en el historial (añadimos al final)
            session['historial'].append({
                'usuario': pregunta_usuario,
                'bot': respuesta_chatbot
            })
            # Marcamos la sesión como modificada para que Flask la guarde
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
    # Ejecutamos la aplicación Flask
    app.run(debug=True, port=5000)
