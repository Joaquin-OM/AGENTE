from transformers import pipeline

# Usamos un modelo especializado en español para evitar respuestas sin sentido
# 'datificate/gpt2-small-spanish' es ligero y entiende perfectamente nuestro idioma
chatbot = pipeline("text-generation", model="datificate/gpt2-small-spanish", device=-1)

def generar_respuesta(pregunta):
    # Prompt en español para un modelo en español
    prompt = f"Pregunta: {pregunta}\nRespuesta:"

    resultado = chatbot(
        prompt,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.3, # Bajamos la temperatura para que sea menos errático
        repetition_penalty=1.2,
        pad_token_id=50256
    )

    texto = resultado[0]["generated_text"]

    # Limpiamos para obtener solo la respuesta generada
    if "Respuesta:" in texto:
        respuesta = texto.split("Respuesta:")[-1]
    else:
        respuesta = texto.replace(prompt, "")

    return respuesta.strip()


