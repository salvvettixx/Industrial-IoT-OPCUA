import asyncio
import json
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from asyncua import Server, ua
from threading import Thread

# --- CONFIGURACIÓN DE LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OPCUA_SIMULATOR")

# --- APP FLASK + SOCKET.IO ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Estado global para la sincronización entre OPC-UA y la Web
telemetry_data = {
    "temperature": 25.0,
    "motor_status": False,
    "last_update": "",
    "alerts": []
}

# --- LÓGICA DEL SERVIDOR OPC-UA ---
async def start_opcua_server():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4848/freeopcua/server/")
    server.set_server_name("Simulador_Industrial_OPCUA")
    
    uri = "http://simulador.industrial.io"
    idx = await server.register_namespace(uri)

    # Construcción del Address Space
    objects = server.nodes.objects
    machine = await objects.add_object(idx, "Maquinaria_Principal")
    temp_var = await machine.add_variable(idx, "Temperatura_Motor", 25.0)
    status_var = await machine.add_variable(idx, "Estado_Motor", False)
    
    await temp_var.set_writable()
    await status_var.set_writable()

    logger.info("Servidor OPC-UA iniciado en el puerto 4840")
    
    async with server:
        count = 0
        while True:
            await asyncio.sleep(2)
            # Simular cambios físicos en la máquina
            count += 0.5
            new_temp =round(25.0 + (count % 15), 2)
            motor_st = True if new_temp < 35 else False
            
            # Actualizar OPC-UA
            await temp_var.write_value(new_temp)
            await status_var.write_value(motor_st)
            
            # Sincronizar con el dashboard web vía SocketIO
            telemetry_data.update({
                "temperature": new_temp,
                "motor_status": motor_st,
                "last_update": datetime.now().strftime("%H:%M:%S")
            })
            
            socketio.emit('opcua_data', telemetry_data)

# --- RUTAS FLASK ---
@app.route('/')
def index():
    return render_template('opcua_dashboard.html')

def run_flask():
    socketio.run(app, host='0.0.0.0', port=5001, debug=False)

if __name__ == "__main__":
    # Ejecutamos el servidor OPC-UA en el bucle principal de asyncio
    # y Flask en un hilo separado para la simulación
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    asyncio.run(start_opcua_server())
