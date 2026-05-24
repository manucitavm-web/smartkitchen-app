import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ── CONFIGURACIÓN VISUAL ─────────────────────────────────
st.set_page_config(
    page_title="Control de Extractor de Humo",
    page_icon="🌀",
    layout="wide"
)

# ── ESTILOS ──────────────────────────────────────────────
st.markdown("""
<style>

/* FONDO GENERAL */
.stApp {
    background: linear-gradient(to bottom right, #dbeafe, #93c5fd);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #dbeafe;
}

/* TITULOS */
h1, h2, h3, p, span, label {
    color: #1E3A8A !important;
    font-family: 'Trebuchet MS', sans-serif;
}

/* BOTONES */
div.stButton > button {
    background-color: #3B82F6 !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
    width: 100%;
    font-weight: bold;
    transition: 0.3s;
    height: 60px;
    font-size: 18px;
}

div.stButton > button:hover {
    background-color: #1D4ED8 !important;
    transform: scale(1.02);
}

/* ALERTAS */
.stAlert {
    border-radius: 20px;
}

/* SLIDER */
.stSlider > div > div > div > div {
    background-color: #3B82F6 !important;
}

</style>
""", unsafe_allow_html=True)

# ── LÓGICA ORIGINAL ──────────────────────────────────────
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883

client1 = paho.Client("GIT-HUBM")
client1.on_message = on_message

# ── TITULO ───────────────────────────────────────────────
st.title("🌀💨 Control de Extractor de Humo")

st.subheader(
    "💙 Controla el sistema de ventilación inteligente de SmartKitchen"
)

# ── INFORMACIÓN ──────────────────────────────────────────
st.info("""
👩‍🍳 Panel de Automatización Inteligente

Esta sección permite controlar el extractor de humo de la cocina inteligente
simulada en Wokwi mediante comandos remotos en tiempo real ✨
""")

st.write("")

# ── BOTONES ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:

    if st.button(
        '🟢 Encender Extractor',
        use_container_width=True
    ):

        act1 = "Encender"

        client1 = paho.Client("GIT-HUBM")

        client1.on_publish = on_publish

        client1.connect(broker, port)

        message = json.dumps({"Act1": act1})

        ret = client1.publish(
            "manuela_vallejo/smartkitchen/comandos",
            "ENCENDER_EXTRACTOR"
        )

        st.success("💨 Extractor encendido correctamente")

    else:

        st.write('')

with col2:

    if st.button(
        '🔴 Apagar Extractor',
        use_container_width=True
    ):

        act1 = "Apagar"

        client1 = paho.Client("GIT-HUBM")

        client1.on_publish = on_publish

        client1.connect(broker, port)

        message = json.dumps({"Act1": act1})

        ret = client1.publish(
            "manuela_vallejo/smartkitchen/comandos",
            "APAGAR_EXTRACTOR"
        )

        st.warning("💨 Extractor apagado correctamente")

    else:

        st.write('')

# ── FOOTER ───────────────────────────────────────────────
st.write("---")

st.caption("💙 SmartKitchen © 2026")
