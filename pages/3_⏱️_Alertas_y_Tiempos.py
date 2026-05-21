import streamlit as st
import paho.mqtt.client as mqtt

# Configuración estética de la página
st.set_page_config(page_title="Control Alertas", page_icon="⏱️", layout="wide")

st.markdown("# ⏱️ Temporizadores y Alertas Activas")
st.write("Envía instrucciones directas para activar componentes en tu simulación de Wokwi.")
st.write("---")

# 📡 Alineación de red con tu ecosistema seguro
BROKER = "broker.mqttdashboard.com"  # Mismo servidor confiable que usamos antes
PORT = 1883
TOPIC_CMD = "manuela_vallejo/smartkitchen/comandos"  # Canal seguro y personalizado

st.subheader("⚙️ Control de Actuadores Remotos")
extractor = st.toggle("🌀 Encender Extractor de Humo")

if st.button("Transmitir Orden a Wokwi", use_container_width=True):
    comando = "ENCENDER_EXTRACTOR" if extractor else "APAGAR_EXTRACTOR"
    
    try:
        # Configurar la versión correcta de la API de MQTT para evitar caídas en la nube
        try:
            api_version = mqtt.CallbackAPIVersion.VERSION1
            cliente = mqtt.Client(callback_api_version=api_version)
        except AttributeError:
            cliente = mqtt.Client()  # Respaldo para versiones antiguas de la librería
            
        cliente.connect(BROKER, PORT, 60)
        cliente.publish(TOPIC_CMD, comando)
        cliente.disconnect()
        
        st.success(f"📡 Comando enviado a la nube MQTT con éxito: `{comando}`")
        st.toast(f"Orden '{comando}' transmitida", icon="⚡")
        
    except Exception as e:
        st.error(f"No se pudo enviar la señal al broker: {e}")
