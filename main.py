## MAIN 
from machine import ADC, Pin
import urequests
import time
import network
import json

# Traer fichero de configuración
with open('config.json', 'r') as f:
    config = json.load(f)

# ======================
# CONFIGURACIÓN WIFI
# ======================
WIFI_SSID = config["SSID"]
WIFI_PASS = config["PASSWORD"]

# ======================
# CONFIGURACIÓN INFLUXDB
# ======================
INFLUX_URL = config["INFLUX_URL"]
INFLUX_TOKEN = config["INFLUX_TOKEN"]
INFLUX_ORG = config["INFLUX_ORG"]
INFLUX_BUCKET = config["INFLUX_BUCKET"]
CLASSROOM = config["CLASSROOM"]
PIN_SENSOR = config["PIN_SENSOR"]

# ======================
# SENSOR ANALÓGICO
# ======================
adc = ADC(Pin(PIN_SENSOR))
adc.atten(ADC.ATTN_11DB)      # Rango completo ~0-3.3V
adc.width(ADC.WIDTH_12BIT)    # 0 - 4095

# ======================
# CONEXIÓN WIFI
# ======================
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)

    print("WiFi conectado:", wlan.ifconfig())

# ======================
# ENVIAR A INFLUXDB
# ======================
def enviar_influx(valor):
    pin_luz.value(1)
    headers = {
        "Authorization": "Token " + INFLUX_TOKEN,
        "Content-Type": "text/plain; charset=utf-8"
    }

    data = "noiselevel,classroom={} valor={}".format(CLASSROOM, valor)

    url = "{}?bucket={}&precision=s".format(
        INFLUX_URL, INFLUX_BUCKET
    )

    try:
        r = urequests.post(url, headers=headers, data=data)
        r.close()
        print("Dato enviado:", valor)
        pin_luz.value(0)
    except Exception as e:
        print("Error enviando a InfluxDB:", e)

# ======================
# PROGRAMA PRINCIPAL
# ======================
conectar_wifi()
pin_luz = Pin(2, Pin.OUT)

while True:
    valor_adc = adc.read()
    enviar_influx(valor_adc)
    time.sleep(5) 