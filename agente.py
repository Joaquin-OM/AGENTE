import string
from leer import LeerDocumento




class Agente:


    def __init__(self, ruta_documento):
        self.lector = LeerDocumento(ruta_documento)
        # Leer el documento y separarlo por párrafos
        texto_completo = self.lector.leer_texto()
        self.parrafos = [p.strip() for p in texto_completo.split('\n\n') if p.strip()]


    def limpiar_pregunta(self, pregunta):
        pregunta = pregunta.lower()


        # Eliminar signos de puntuación
        for signo in string.punctuation + "¿¡":
            pregunta = pregunta.replace(signo, "")


        # Separar la pregunta en formato de lista de listas (ej. [['que'], ['es'], ...])
        palabras = [[palabra] for palabra in pregunta.split()]


        return palabras


    def responder(self, pregunta):


        palabras_separadas = self.limpiar_pregunta(pregunta)
       
        # Palabras comunes a ignorar al buscar (stop words básicas)
        stop_words = {"que", "es", "la", "el", "en", "de", "y", "a", "un", "una", "con", "por", "los", "las", "se", "del", "al", "para"}
       
        # Extraer palabras útiles
        palabras_a_buscar = [item[0] for item in palabras_separadas if item[0] not in stop_words]


        # Si todas eran stop words y no hay palabras útiles
        if not palabras_a_buscar:
            return "Agente: Demaciadas respuestas para esta pregunta, haz una pregunta mas especifica"


        # Buscar en los párrafos
        for palabra in palabras_a_buscar:
            for parrafo in self.parrafos:
                # Normalizar el párrafo para la búsqueda
                parrafo_normalizado = parrafo.lower()
                for signo in string.punctuation + "¿¡":
                    parrafo_normalizado = parrafo_normalizado.replace(signo, "")
               
                palabras_del_parrafo = parrafo_normalizado.split()
               
                if palabra in palabras_del_parrafo:
                    return f"Agente:\n{parrafo}"


        return "Agente: La palabra o pregunta no se encuentra en el documento."
