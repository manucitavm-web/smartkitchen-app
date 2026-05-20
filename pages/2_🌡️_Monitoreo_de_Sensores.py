import streamlit as st
import paho.mqtt.client as mqtt
import time

st.set_page_config(page_title="Monitoreo Wokwi", page_icon="🌡️", layout="wide")

st.markdown("# 🌡️ Monitoreo de Sensores (Wokwi)")
st.write("Visualiza las variables capturedas por tu circuito virtual en tiempo real.")
st.write("---")

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "manuela_vallejo/smartkitchen"

# Inicializar los estados de la sesión en español para evitar vacíos
if "temperatura" not in st.session_state:
    st.session_state["temperatura"] = "Esperando..."
if "humedad" not in st.session_state:
    st.session_state["humedad"] = "Esperando..."

# Función callback para procesar la llegada de datos de Wokwi
def mensaje_recibido(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    try:
        datos = payload.split(",")
        st.session_state["temperatura"] = f"{datos[0]} °C"
        st.session_state["humedad"] = f"{datos[1]} %"  # Unificado a 'humedad' en español
    except:
        st.session_state["temperatura"] = payload

# Renderizado estético de las tarjetas de telemetría (UX Limpio)
c1, c2 = st.columns(2)
c1.metric(label="🌡️ Temperatura Horno", value=st.session_state["temperatura"])
c2.metric(label="💧 Humedad Ambiente", value=st.session_state["humedad"])

st.write("---")

# 🎨 Personalización de color para el botón de actualización (CSS Inyectado)
st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #5C6BC0; /* <--- Cambia este código HEX por el color que quieras (Ej: #5C6BC0 es un azul/lila) */
        color: white;
        border-color: #5C6BC0;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #3F51B5; /* Color un poco más oscuro para el efecto focus/hover */
        color: white;
        border-color: #3F51B5;
    }
    </style>
""", unsafe_allow_html=True)

# Botón interactivo para escuchar el broker MQTT bajo demanda
if st.button("🔄 Actualizar Lecturas de Wokwi", type="primary", use_container_width=True):
    with st.spinner("Escuchando el canal MQTT..."):
        cliente = mqtt.Client()
        cliente.on_message = mensaje_recibido
        try:
            cliente.connect(BROKER, PORT, 60)
            cliente.subscribe(TOPIC)
            cliente.loop_start()
            time.sleep(2)  # Ventana segura de 2 segundos para atrapar la telemetría
            cliente.loop_stop()
            cliente.disconnect()
            st.toast("Datos sincronizados de la nube.", icon="📡")
            st.rerun()  # Forzar actualización para pintar los datos nuevos al instante
        except Exception as e:
            st.error(f"Error de red: {e}")
