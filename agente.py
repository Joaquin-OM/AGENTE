import string
import unicodedata
from leer import LeerDocumento




class Agente:


    def __init__(self, ruta_documento):
        self.lector = LeerDocumento(ruta_documento)
        # Leer el documento y separarlo por párrafos
        texto_completo = self.lector.leer_texto()
        self.parrafos = [p.strip() for p in texto_completo.split('\n\n') if p.strip()]

    def normalizar(self, texto):
        """Elimina acentos y convierte a minúsculas."""
        texto = texto.lower()
        texto = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
        return texto


    def limpiar_pregunta(self, pregunta):
        pregunta = self.normalizar(pregunta)

        # Eliminar signos de puntuación y caracteres especiales
        for signo in string.punctuation + "¿¡":
            pregunta = pregunta.replace(signo, "")

        # Separar la pregunta en palabras
        palabras = pregunta.split()
        return palabras


    def responder(self, pregunta):
        palabras_separadas = self.limpiar_pregunta(pregunta)
       
        # Palabras comunes a ignorar al buscar (stop words básicas)
        stop_words = {"que", "es", "la", "el", "en", "de", "y", "a", "un", "una", "con", "por", "los", "las", "se", "del", "al", "para"}
       
        # Extraer palabras útiles
        palabras_a_buscar = [palabra for palabra in palabras_separadas if palabra not in stop_words]

        # Si todas eran stop words y no hay palabras útiles
        if not palabras_a_buscar:
            return "No he podido entender tu pregunta. Por favor, intenta ser más específico."


        # Respuesta rápida para saludos
        if "hola" in palabras_separadas:
            return "¡Hola! Soy tu asistente. Puedo informarte sobre la digitalización y transformación digital. ¿Qué quieres saber?"

        # Buscar en los párrafos
        for palabra in palabras_a_buscar:
            for parrafo in self.parrafos:
                # Normalizar el párrafo para la búsqueda
                parrafo_normalizado = self.normalizar(parrafo)
                for signo in string.punctuation + "¿¡":
                    parrafo_normalizado = parrafo_normalizado.replace(signo, "")
               
                palabras_del_parrafo = parrafo_normalizado.split()
               
                if palabra in palabras_del_parrafo:
                    return parrafo

        return "Lo siento, no he encontrado información sobre eso en mi documento."
