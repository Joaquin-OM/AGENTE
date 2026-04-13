class LeerDocumento:


    def __init__(self, ruta):
        self.ruta = ruta


    def leer_texto(self):
        with open(self.ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        return contenido