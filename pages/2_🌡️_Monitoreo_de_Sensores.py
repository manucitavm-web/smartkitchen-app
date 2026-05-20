import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# Configuración inicial de la página
st.set_page_config(page_title="Monitoreo Wokwi", page_icon="🌡️", layout="wide")

st.markdown("# 🌡️ Monitoreo de Sensores (Wokwi)")
st.write("Visualiza las variables capturadas por tu circuito virtual en tiempo real.")
st.write("---")

# 📡 Cambiamos solo el Broker, dejamos TU topic idéntico
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "manuela_vallejo/smartkitchen"

# Inicializar los estados de la sesión
if "temperatura" not in st.session_state:
    st.session_state["temperatura"] = "Esperando..."
if "humedad" not in st.session_state:
    st.session_state["humedad"] = "Esperando..."

# Función callback configurada para leer el JSON de tu ESP32
def mensaje_recibido(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        datos = json.loads(payload)
        
        # Mapea las llaves del JSON que envía el circuito viejo
        if "Temp" in datos and "Hum" in datos:
            st.session_state["temperatura"] = f"{datos['Temp']} °C"
            st.session_state["humedad"] = f"{datos['Hum']} %"
    except Exception:
        pass

# Renderizado de las tarjetas métricas
c1, c2 = st.columns(2)
c1.metric(label="🌡️ Temperatura Horno", value=st.session_state["temperatura"])
c2.metric(label="💧 Humedad Ambiente", value=st.session_state["humedad"])

st.write("---")

# Personalización estética del botón lila
st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #5C6BC0;
        color: white;
        border-color: #5C6BC0;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #3F51B5;
        color: white;
        border-color: #3F51B5;
    }
    </style>
""", unsafe_allow_html=True)

# Botón con la lógica de bucle controlado
if st.button("🔄 Actualizar Lecturas de Wokwi", type="primary", use_container_width=True):
    with st.spinner("Conectando con el circuito virtual de Wokwi..."):
        
        try:
            api_version = mqtt.CallbackAPIVersion.VERSION1
            cliente = mqtt.Client(callback_api_version=api_version)
        except AttributeError:
            cliente = mqtt.Client()
            
        cliente.on_message = mensaje_recibido
        
        try:
            cliente.connect(BROKER, PORT, 60)
            cliente.subscribe(TOPIC)
            
            # Escucha activa controlada (máximo 3 segundos)
            intentos = 0
            while intentos < 15:
                cliente.loop(timeout=0.2)
                if st.session_state["temperatura"] != "Esperando...":
                    break
                time.sleep(0.2)
                intentos += 1
                
            cliente.disconnect()
            
            if st.session_state["temperatura"] != "Esperando...":
                st.toast("¡Datos sincronizados desde Wokwi con éxito!", icon="📡")
            else:
                st.warning("No se recibió telemetría nueva. Verifica que Wokwi esté en PLAY.")
                
            st.rerun()
            
        except Exception as e:
            st.error(f"Error de red al conectar con el broker: {e}")
