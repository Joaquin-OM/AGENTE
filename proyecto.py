import os
from agente import Agente


def main():


    ruta = os.path.join(os.path.dirname(__file__), "documento.txt")


    agente = Agente(ruta)


    print("Chatbot simple - Fase 1")
    print("Escribe una pregunta (o 'salir' para terminar)")


    while True:


        pregunta = input("\nPregunta: ")


        if pregunta.lower() == "salir":
            print("Adiós")
            break


        respuesta = agente.responder(pregunta)


        print(respuesta)


if __name__ == "__main__":
    main()
