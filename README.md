# Monitoreo Acústico de Aulas con IoT (ESP32 + InfluxDB + Grafana)

Este proyecto implementa un sistema de monitoreo de niveles de ruido ambiental en tiempo real. Utiliza un microcontrolador **ESP32** con **MicroPython** para capturar señales analógicas, enviarlas a una base de datos de series temporales (**InfluxDB**) y visualizarlas en un dashboard dinámico de **Grafana**.

## 1. Arquitectura del Sistema
El flujo de datos sigue una arquitectura de IoT de extremo a extremo:
`Sensor LM393` → `ESP32 (MicroPython)` → `WiFi` → `InfluxDB Cloud/Local` → `Grafana Dashboard`

## 2. Componentes Técnicos
| Componente | Función |
| :--- | :--- |
| **ESP32** | Microcontrolador principal con conectividad WiFi. |
| **Sensor LM393** | Captura variaciones de presión sonora (Salida Analógica). |
| **InfluxDB** | Base de datos de series temporales (Time Series). |
| **Grafana** | Plataforma de visualización y alertas. |

## 3. Conexiones (Hardware)
Las conexiones realizadas en la placa son:
* **VCC** -> 3.3V (ESP32)
* **GND** -> GND (ESP32)
* **Out (Analógico)** -> GPIO 33 (ESP32)

## 4. Configuración del Software
El firmware está desarrollado en **MicroPython**, destacando el uso de un archivo `config.json` para la seguridad de las credenciales.

### Librerías Utilizadas:
* `machine.ADC` y `machine.Pin`: Control de hardware.
* `urequests`: Comunicación HTTP con InfluxDB API.
* `network`: Gestión de la pila WiFi.
* `json`: Manejo de configuración externa.

### Flujo de Programa:
1. **Inicialización:** Lectura de `config.json` y configuración del ADC (12 bits, atenuación 11dB para rango 0-3.3V).
2. **Conexión:** Establecimiento de red WiFi segura.
3. **Bucle Principal:** * Captura del valor analógico.
   * Feedback visual mediante LED interno (GPIO 2) durante la transmisión.
   * Envío mediante **HTTP POST** usando Line Protocol: `noiselevel,classroom={ID} valor={ADC}`.
   * Intervalo de muestreo: 5 segundos.

## 5. Visualización y Alertas (Grafana)
El dashboard permite un análisis profundo mediante consultas en lenguaje **Flux**:

* **Gauge Panel:** Nivel actual en tiempo real.
* **Stat Panel:** Máximo pico registrado durante el día.
* **Time Series:** Historial de las últimas 6 horas.
* **Minute Peaks:** Filtrado de picos máximos por cada minuto para reducir ruido visual.

### Sistema de Alertas:
* **Umbral Crítico:** Configurado en > 750 (valor ADC).
* **Lógica:** Si el promedio excede el umbral durante 30 segundos, se dispara la notificación.

## 6. Conclusión
Este proyecto demuestra una solución eficiente y escalable para el monitoreo ambiental. La separación de la configuración en JSON y el uso de bases de datos especializadas como InfluxDB permiten que el sistema sea fácilmente adaptable a múltiples aulas, mejorando la gestión del bienestar acústico en centros educativos.

## 7. Referencias
* [MicroPython Documentation](https://docs.micropython.org)
* [InfluxDB API Reference](https://docs.influxdata.com)
* [Grafana Flux Query Language](https://grafana.com/docs)
* [ESP32 Datasheet - Espressif Systems](https://www.espressif.com)