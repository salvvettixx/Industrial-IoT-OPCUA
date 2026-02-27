# 🏭 Industrial IoT & Digital Twin - OPC-UA Professional Suite

![Industry 4.0](https://img.shields.io/badge/Industry-4.0-blue?style=for-the-badge)
![OPC-UA](https://img.shields.io/badge/OPC--UA-IEC_62541-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Real-Time](https://img.shields.io/badge/Latency-Low-green?style=for-the-badge)

Solución integral de grado industrial para la implementación de comunicaciones M2M (Machine-to-Machine) basadas en el estándar **OPC-UA (IEC 62541)**. Este ecosistema permite la creación de Gemelos Digitales (Digital Twins) para activos críticos, garantizando interoperabilidad, seguridad robusta y monitoreo en tiempo real.

## 🌟 Características Técnicas

- **Servidor de Campo OPC-UA:** Arquitectura robusta con Address Space jerárquico modelado bajo estándares industriales.
- **Protocolo de Alta Eficiencia:** Implementación de suscripciones (`DataChange`) para optimizar el ancho de banda y reducir la latencia de red.
- **Seguridad Industrial de Extremo a Extremo:** Cifrado asimétrico X.509, políticas de seguridad `Basic256Sha256` y gestión de sesiones seguras.
- **Supervisión Web Inteligente:** Dashboard de control integrado mediante WebSockets para visualización instantánea sin necesidad de software SCADA externo.
- **Resiliencia Operativa:** Cliente con lógica de reconexión automática `Keep-Alive` y gestión de timeouts para entornos críticos.

## 🏗️ Arquitectura de la Solución

1. **Capa Sensor/Accionador:** Generación de telemetría dinámica y exposición de métodos de control.
2. **Capa de Comunicación:** Túnel TCP binario basado en el stack OPC-UA para máxima fiabilidad.
3. **Capa de Supervisión:** Transformación de protocolos industriales a WebSockets para visualización remota en dashboards interactivos.

## 🚀 Guía de Inicio Rápido

### Instalación de Dependencias
Utiliza el gestor de paquetes de Python (asegúrate de tener `py` configurado):
```powershell
py -m pip install asyncua flask-socketio cryptography
```

### Ejecución del Ecosistema
El proyecto incluye un simulador unificado que lanza el servidor industrial y el panel de control:
```powershell
py opcua_simulator.py
```
Acceso al Dashboard: [http://localhost:5001](http://localhost:5001)

## 📁 Estructura del Ecosistema

```
Industrial-IoT-OPCUA/
├── opcua_simulator.py    # Orquestador del Gemelo Digital + Web Bridge
├── server_opcua.py       # Nodo de campo (Servidor OPC-UA)
├── client_scada.py       # Estación de monitoreo (Cliente SCADA)
├── templates/            # Interfaz de Usuario (Industrial Design)
└── docs/                 # Documentación Técnica (GitHub Pages)
```

---
Desarrollado para la convergencia de tecnologías IT/OT y la excelencia en la Automatización Industrial. 
