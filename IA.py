import ollama

# Ya no usamos transformers ni torch, sino la librería de python para Ollama.
# Ollama nos permite ejecutar modelos grandes (LLMs) como Mistral de forma local y eficiente.

def generar_respuesta(pregunta):
    # Creamos la lista de mensajes que le enviaremos al modelo.
    # El rol "system" sirve para darle instrucciones generales de comportamiento.
    # El rol "user" es la pregunta que hace el usuario.
    mensajes = [
        {"role": "system", "content": "Eres un asistente útil y amable que responde en español de manera clara y concisa."},
        {"role": "user", "content": pregunta}
    ]
    
    try:
        # Llamamos al modelo 'mistral' mediante Ollama
        # Esta función se conecta a la API local de Ollama (por defecto en el puerto 11434)
        resultado = ollama.chat(
            model='mistral', 
            messages=mensajes
        )
        
        # El resultado es un diccionario. Extraemos el contenido del mensaje generado.
        respuesta = resultado['message']['content']
        
    except Exception as e:
        # Si hay un error (ej. Ollama no está ejecutándose, o Mistral no está descargado), lo capturamos.
        respuesta = f"Error al conectar con Ollama o el modelo Mistral: {str(e)}"
        
    return respuesta.strip()
