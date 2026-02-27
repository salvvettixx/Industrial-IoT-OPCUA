from src.ingesta import Ingestor
from src.motor_rag import MotorRAG
import os

def main():
    print("--- Bienvenido al Sistema RAG Avanzado (Senior Edition) ---")
    
    # 1. Verificar si la DB ya existe
    if not os.path.exists("./chroma_db"):
        print("\n[*] Iniciando fase de INGESTA...")
        ingestor = Ingestor()
        ingestor.create_vector_store()
    else:
        print("\n[*] Base de datos vectorial detectada. Saltando ingesta.")

    # 2. Inicializar Motor
    print("\n[*] Inicializando MOTOR RAG con Re-ranking...")
    motor = MotorRAG()

    # 3. Bucle de consulta
    while True:
        pregunta = input("\nPregunta (o 'salir' para terminar): ")
        if pregunta.lower() in ["salir", "exit", "q"]:
            break
        
        try:
            respuesta = motor.responder(pregunta)
            print(f"\n> RESPUESTA:\n{respuesta['respuesta']}")
            print(f"\n> FUENTES CONSULTADAS: {set(respuesta['fuentes'])}")
        except Exception as e:
            print(f"Error al procesar la pregunta: {e}")

if __name__ == "__main__":
    main()
