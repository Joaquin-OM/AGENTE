import os
from flask import Flask, render_template, request, session, redirect, url_for
from agente import Agente
from ia import generar_respuesta

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesion' # Necesario para usar session

# Instanciar el agente una sola vez al cargar la aplicación Flask
ruta_documento = os.path.join(os.path.dirname(__file__), "documento.txt")
mi_agente = Agente(ruta_documento)

# --- FASE 2: Controlador Modular ---
def procesar_mensaje(mensaje_usuario):
    """
    Controlador para procesar el mensaje del usuario conectando a tu Agente.
    Si el documento interno no encuentra respuesta, usamos IA generativa (GPT2).
    """
    # Intentamos primero con nuestro agente interno
    respuesta_agente = mi_agente.responder(mensaje_usuario)
    
    # Si la respuesta es la de "no encontrado", usamos GPT-2 de transformers
    if "Lo siento, no he encontrado información" in respuesta_agente:
        try:
            return generar_respuesta(mensaje_usuario)
        except Exception as e:
            return f"Hubo un error al generar la respuesta con IA: {e}"
            
    return respuesta_agente

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
