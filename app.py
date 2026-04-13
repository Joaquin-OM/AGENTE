import os
from flask import Flask, render_template, request
from agente import Agente

app = Flask(__name__)

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
    respuesta_chatbot = None
    pregunta_usuario = None
    
    # Mensaje de bienvenida inicial enviado desde Flask a HTML (Demostración Jinja2)
    mensaje_bienvenida = "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"

    if request.method == 'POST':
        # Capturamos la pregunta del usuario desde el formulario
        pregunta_usuario = request.form.get('pregunta', '')
        
        # Procesamos el mensaje a través de nuestro controlador
        if pregunta_usuario.strip():
            respuesta_chatbot = procesar_mensaje(pregunta_usuario)
        else:
            respuesta_chatbot = "Por favor, escribe una pregunta."

    # Renderizamos la plantilla pasando las variables al frontend
    return render_template(
        'index.html', 
        mensaje_bienvenida=mensaje_bienvenida,
        pregunta_usuario=pregunta_usuario,
        respuesta_chatbot=respuesta_chatbot
    )

if __name__ == '__main__':
    # Ejecutamos la aplicación Flask
    app.run(debug=True, port=5000)
