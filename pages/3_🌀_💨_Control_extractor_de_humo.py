import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- CONFIGURACIÓN ESTÉTICA (SÓLO VISUAL) ---
st.set_page_config(page_title="Control de Extractor de Humo", page_icon="🌀")

st.markdown("""
    <style>
    /* Fondo de la página en un gris azulado muy sutil y limpio */
    .main { background-color: #F4F6F9; }
    
    /* Títulos y textos en azul oscuro elegante */
    h1, h2, h3, p, span, label { color: #1E3A8A !important; }

    /* Estilo para TODOS los botones de Streamlit (Encender y Apagar) */
    div.stButton > button {
        background-color: #3B82F6 !important; /* Azul vibrante */
        color: white !important;
        border-radius: 20px !important;
        border: 2px solid #60A5FA !important; /* Azul claro para el borde */
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Efecto al pasar el mouse por encima del botón */
    div.stButton > button:hover {
        background-color: #1D4ED8 !important; /* Azul más oscuro al presionar */
        border: 2px solid #2563EB !important;
        transform: scale(1.02);
    }

    /* Personalización del Slider en tonos azules por si acaso */
    .stSlider > div > div > div > div {
        background-color: #3B82F6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA ORIGINAL (MANTENIDA SIN ALTERACIONES) ---
values = 0.0
act1="OFF"

def on_publish(client,userdata,result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("GIT-HUBM") # ID Original
client1.on_message = on_message

# --- INTERFAZ ---
st.title("🌀💨 Control de extractor de humo")

# Descripción integrada (Opción 2)
st.write("Panel de control remoto para extractor de humo de tu cocina inteligente (Smart Kitchen). Esta pestaña de la aplicación te ofrece una solución interactiva de automatización donde, mediante dos botones: Encendido y Apagado, podrás intervenir en el estado del sistema de ventilación instantáneamente y sin configuraciones complejas.")
st.write("---")

# Botones organizados en columnas para mejor estética
col1, col2 = st.columns(2)

with col1:
    if st.button('Encender'):
        act1="Encender"
        client1= paho.Client("GIT-HUBM")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message = json.dumps({"Act1":act1})
        ret= client1.publish("manuela_vallejo/smartkitchen/comandos", "ENCENDER_EXTRACTOR") # Tópico Original
    else:
        st.write('')

with col2:
    if st.button('Apagar'):
        act1="Apagar"
        client1= paho.Client("GIT-HUBM")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message = json.dumps({"Act1":act1})
        ret= client1.publish("manuela_vallejo/smartkitchen/comandos", "APAGAR_EXTRACTOR") # Tópico Original
    else:
        st.write('')
