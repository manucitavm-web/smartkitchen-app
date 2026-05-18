import streamlit as st
import paho.mqtt.client as mqtt
import time

st.set_page_config(page_title="Monitoreo Wokwi", page_icon="🌡️", layout="wide")

st.markdown("# 🌡️ Monitoreo de Sensores (Wokwi)")
st.write("Visualiza las variables capturadas por tu circuito virtual en tiempo real.")
st.write("---")

# Servidor intermedio en internet para conectar con Wokwi
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "smartkitchen/telemetria"

if "temperatura" not in st.session_state:
    st.session_state["temperatura"] = "Esperando..."
if "humedad" not in st.session_state:
    st.session_state["humedad"] = "Esperando..."

# Función que se ejecuta cuando llega un dato desde Wokwi
def mensaje_recibido(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    try:
        # Si Wokwi manda "24,60", lo separamos
        datos = payload.split(",")
        st.session_state["temperatura"] = f"{datos[0]} °C"
        st.session_state["humedad"] = f"{datos[1]} %"
    except:
        st.session_state["temperatura"] = payload

c1, c2 = st.columns(2)
c1.metric(label="🌡️ Temperatura Horno", value=st.session_state["temperatura"])
c2.metric(label="💧 Humedad Ambiente", value=st.session_state["humedad"])

st.write("---")

if st.button("🔄 Actualizar Lecturas de Wokwi", type="primary", use_container_width=True):
    with st.spinner("Escuchando el canal MQTT..."):
        cliente = mqtt.Client()
        cliente.on_message = mensaje_recibido
        try:
            cliente.connect(BROKER, PORT, 60)
            cliente.subscribe(TOPIC)
            cliente.loop_start()
            time.sleep(2)  # Ventana de tiempo para capturar el dato
            cliente.loop_stop()
            cliente.disconnect()
            st.toast("Datos sincronizados de la nube.", icon="📡")
        except Exception as e:
            st.error(f"Error de red: {e}")
