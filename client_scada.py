import asyncio
import logging
from asyncua import Client, ua

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SCADA_Client")

class SubscriptionHandler:
    """Implementa la gestión de eventos DataChange (Suscripciones)"""
    def datachange_notification(self, node, val, data):
        logger.info(f"ALERTA SCADA - Cambio de Dato: Nodo {node} valor {val}")

async def main():
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    
    while True: # Bucle de Reconexión Automática
        client = Client(url=url)
        try:
            logger.info(f"Intentando conectar con Gateway Industrial: {url}")
            async with client:
                logger.info("Conexión establecida con éxito.")
                
                # 1. Descubrimiento Dinámico de Nodos
                root = client.nodes.root
                objects = client.nodes.objects
                namespace_idx = await client.get_namespace_index("http://empresa.com/iot/linea1")
                
                # Obtener referencia a la variable de temperatura
                temp_node = await objects.get_child([f"{namespace_idx}:Linea_Produccion_1", f"{namespace_idx}:Machine_Alpha", f"{namespace_idx}:Temperature"])
                
                # 2. Configurar Suscripción (Optimización de Tráfico)
                handler = SubscriptionHandler()
                sub = await client.create_subscription(500, handler)
                handle = await sub.subscribe_data_change(temp_node)
                
                logger.info("Suscripción activa. Monitoreando cambios en tiempo real...")

                # 3. Mantener sesión viva y gestionar Timeout
                while True:
                    await asyncio.sleep(5)
                    val = await temp_node.read_value()
                    logger.info(f"Lectura cíclica de control: {val}")

        except Exception as e:
            logger.error(f"Fallo en la comunicación: {e}. Reintentando en 5 segundos...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
