from transformers import pipeline

# Usamos distilgpt2: es la versión "rápida" de gpt2 (mitad de tamaño, doble de velocidad)
# device=-1 asegura que use la CPU de forma eficiente (o 0 para GPU si está disponible)
chatbot = pipeline("text-generation", model="distilgpt2", device=-1)

def generar_respuesta(pregunta):
    # Un prompt estructurado ayuda a que la IA genere una respuesta coherente
    prompt = f"User asks about: {pregunta}\nShort answer:"

    # Llamamos al modelo con parámetros optimizados para velocidad
    resultado = chatbot(
        prompt,
        max_new_tokens=40, # Suficiente para una respuesta rápida
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.2,
        pad_token_id=50256 # Evita advertencias de configuración
    )

    # El modelo devuelve una lista con resultados
    texto = resultado[0]["generated_text"]

    # Extraemos solo lo generado después de nuestro prompt
    if "Short answer:" in texto:
        respuesta = texto.split("Short answer:")[-1]
    else:
        respuesta = texto.replace(prompt, "")

    return respuesta.strip()

