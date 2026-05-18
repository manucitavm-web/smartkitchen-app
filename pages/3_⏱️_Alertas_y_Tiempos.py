import streamlit as st
import paho.mqtt.client as mqtt

st.set_page_config(page_title="Control Alertas", page_icon="⏱️", layout="wide")

st.markdown("# ⏱️ Temporizadores y Alertas Activas")
st.write("Envía instrucciones directas para activar componentes en tu simulación de Wokwi.")
st.write("---")

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_CMD = "smartkitchen/comandos"

st.subheader("⚙️ Control de Actuadores Remotos")
extractor = st.toggle("🌀 Encender Extractor de Humo")

if st.button("Transmitir Orden a Wokwi", use_container_width=True):
    comando = "ENCENDER_EXTRACTOR" if extractor else "APAGAR_EXTRACTOR"
    
    try:
        cliente = mqtt.Client()
        cliente.connect(BROKER, PORT, 60)
        cliente.publish(TOPIC_CMD, comando)
        cliente.disconnect()
        st.success(f"📡 Comando enviado a la nube MQTT: `{comando}`")
    except Exception as e:
        st.error(f"No se pudo enviar la señal: {e}")
