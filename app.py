from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from src.motor_rag import MotorRAG
import os

app = Flask(__name__)
CORS(app)

# Inicializar el Motor RAG una sola vez al arrancar
print("[INFO] Cargando Motor RAG para la interfaz web...")
try:
    motor = MotorRAG()
except Exception as e:
    print(f"[ERROR] No se pudo inicializar el motor: {e}")
    motor = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    if not motor:
        return jsonify({"respuesta": "El motor RAG no está inicializado correctamente.", "fuentes": []}), 500
    
    data = request.json
    pregunta = data.get('pregunta', '')
    
    if not pregunta:
        return jsonify({"respuesta": "Por favor, introduce una pregunta.", "fuentes": []}), 400
    
    resultado = motor.responder(pregunta)
    return jsonify(resultado)

if __name__ == '__main__':
    # Asegurarse de que el puerto 5000 esté libre o usar otro
    app.run(host='0.0.0.0', port=5000, debug=False)
