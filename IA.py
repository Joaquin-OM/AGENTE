from transformers import pipeline

# "text-generation" --> será un modelo de generar texto y GPT2 el modelo que se usará
chatbot = pipeline("text-generation", model="gpt2")

def generar_respuesta(pregunta):

    # Creamos el prompt (En GPT2 mejor en ingles si no tenemos una fuente interna como es en esta práctica)
    prompt = f"""
Write a random text about: {pregunta}
"""

    # Llamamos al modelo para generar texto
    resultado = chatbot(
        prompt,
        # Número máximo de palabras nuevas que puede generar
        max_new_tokens=50,
        # Permite que la IA genere respuestas variadas (no siempre lo mismo)
        do_sample=True,
        # Controla la improvisación de la IA de menos improvisación a más
        temperature=0.5,
        # Penaliza repetir palabras o frases de más repetición a menos.
        repetition_penalty=1.2
    )

    # El modelo devuelve una lista con resultados
    texto = resultado[0]["generated_text"]

    # Quitamos el prompt original para quedarnos solo con la respuesta
    respuesta = texto.replace(prompt, "")

    # Eliminamos espacios innecesarios al inicio y final
    return respuesta.strip()
