import asyncio
import logging
from asyncua import Server, ua
from asyncua.common.methods import uamethod

# Configuración de Logging Industrial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OPCUA_Server")

@uamethod
def reset_machine(parent):
    logger.info("Comando de RESET recibido del cliente SCADA.")
    return [True]

async def main():
    # 1. Inicializar Servidor
    server = Server()
    await server.init()
    
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("IndustrialGateway_Alpha")

    # 2. Configuración de Seguridad (Certificados X.509)
    # Nota: En producción, estos archivos deben estar firmados por una CA.
    # await server.load_certificate("server_cert.der")
    # await server.load_private_key("server_key.pem")

    # 3. Definir Namespace
    uri = "http://empresa.com/iot/linea1"
    idx = await server.register_namespace(uri)

    # 4. Estructura del Address Space (Modelo de Información)
    objects = server.nodes.objects
    linea1 = await objects.add_folder(idx, "Linea_Produccion_1")
    machine = await linea1.add_object(idx, "Machine_Alpha")
    
    # Variables con permisos y límites
    temp = await machine.add_variable(idx, "Temperature", 25.0)
    await temp.set_writable() # Permitir escritura desde SCADA
    
    status = await machine.add_variable(idx, "MotorStatus", False)
    await status.set_writable()

    # Añadir Método de Control
    await machine.add_method(idx, "ResetMachine", reset_machine, [], [ua.VariantType.Boolean])

    # 5. Inicio del Servidor
    logger.info(f"Servidor OPC-UA iniciado en {server.endpoint}")
    async with server:
        count = 0
        while True:
            await asyncio.sleep(1)
            # Simulación de telemetría dinámica
            new_temp = 25.0 + (count % 10) * 0.5
            await temp.write_value(new_temp)
            count += 1

if __name__ == "__main__":
    asyncio.run(main())
