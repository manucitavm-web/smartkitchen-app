import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# ── CONFIGURACIÓN ─────────────────────────────
st.set_page_config(
    page_title="Monitoreo Wokwi",
    page_icon="🌡️",
    layout="wide"
)

# ── ESTILOS ───────────────────────────────────
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right, #dbeafe, #93c5fd);
}

[data-testid="stSidebar"] {
    background-color: #dbeafe;
}

h1, h2, h3, p, span, label {
    color: #1E3A8A !important;
    font-family: 'Trebuchet MS', sans-serif;
}

/* MÉTRICAS */
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.85);
    padding: 20px;
    border-radius: 25px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
}

/* BOTONES */
div.stButton > button {
    background-color: #3B82F6 !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
    width: 100%;
    font-weight: bold;
    height: 55px;
}

div.stButton > button:hover {
    background-color: #1D4ED8 !important;
}

/* ALERTAS */
.stAlert {
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# ── TITULO ────────────────────────────────────
st.title("🌡️💧 Monitor Inteligente")

st.subheader(
    "💙 Visualiza los sensores de SmartKitchen en tiempo real desde Wokwi"
)

# ── INFORMACIÓN ───────────────────────────────
st.info("""
👩‍🍳 Panel de Monitoreo Inteligente

Esta sección permite visualizar la temperatura y humedad
de la cocina inteligente simulada en Wokwi en tiempo real ✨
""")

st.write("")

# ── MQTT ──────────────────────────────────────
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "manuela_vallejo/smartkitchen"

# ── ESTADOS ───────────────────────────────────
if "temperatura" not in st.session_state:
    st.session_state["temperatura"] = "Esperando..."

if "humedad" not in st.session_state:
    st.session_state["humedad"] = "Esperando..."

# ── CALLBACK ──────────────────────────────────
def mensaje_recibido(client, userdata, msg):

    try:

        payload = msg.payload.decode("utf-8")

        datos = json.loads(payload)

        if "Temp" in datos and "Hum" in datos:

            st.session_state["temperatura"] = f"{datos['Temp']} °C"

            st.session_state["humedad"] = f"{datos['Hum']} %"

    except:
        pass

# ── MÉTRICAS ──────────────────────────────────
c1, c2 = st.columns(2)

with c1:

    st.metric(
        label="🌡️ Temperatura Horno",
        value=st.session_state["temperatura"]
    )

with c2:

    st.metric(
        label="💧 Humedad Ambiente",
        value=st.session_state["humedad"]
    )

st.write("")

# ── BOTÓN ─────────────────────────────────────
if st.button(
    "🔄 Actualizar Lecturas de Wokwi",
    use_container_width=True
):

    with st.spinner("📡 Conectando con Wokwi..."):

        st.session_state["temperatura"] = "Esperando..."
        st.session_state["humedad"] = "Esperando..."

        try:

            api_version = mqtt.CallbackAPIVersion.VERSION1

            cliente = mqtt.Client(
                callback_api_version=api_version
            )

        except AttributeError:

            cliente = mqtt.Client()

        cliente.on_message = mensaje_recibido

        try:

            cliente.connect(BROKER, PORT, 60)

            cliente.subscribe(TOPIC)

            intentos = 0

            while intentos < 30:

                cliente.loop(timeout=0.2)

                if st.session_state["temperatura"] != "Esperando...":
                    break

                time.sleep(0.2)

                intentos += 1

            cliente.disconnect()

            if st.session_state["temperatura"] != "Esperando...":

                st.success("📡 Datos sincronizados correctamente")

            else:

                st.warning(
                    "No se recibió información nueva desde Wokwi."
                )

            st.rerun()

        except Exception as e:

            st.error(f"Error de conexión: {e}")

# ── FOOTER ────────────────────────────────────
st.write("---")

st.caption("💙 SmartKitchen © 2026")
