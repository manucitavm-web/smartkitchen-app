import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- CONFIGURACIÓN ESTÉTICA (SÓLO VISUAL) ---
st.set_page_config(page_title="MQTT Control Pink", page_icon="🌸")

st.markdown("""
    <style>
    /* Fondo de la página */
    .main { background-color: #fffafa; }
    
    /* Títulos y textos en tonos fucsia */
    h1, h2, h3, p, span, label { color: #ff1493 !important; }

    /* Estilo para TODOS los botones de Streamlit (ON, OFF, Enviar) */
    div.stButton > button {
        background-color: #ff69b4 !important;
        color: white !important;
        border-radius: 20px !important;
        border: 2px solid #ffb6c1 !important;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #ff1493 !important;
        border: 2px solid #db7093 !important;
        transform: scale(1.02);
    }

    /* Personalización del Slider */
    .stSlider > div > div > div > div {
        background-color: #ff69b4 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Muestra la versión de Python
st.write("Versión de Python:", platform.python_version())

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
st.title("MQTT Control")

# Botones organizados en columnas para mejor estética
col1, col2 = st.columns(2)

with col1:
    if st.button('ON'):
        act1="ON"
        client1= paho.Client("GIT-HUBM")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message = json.dumps({"Act1":act1})
        ret= client1.publish("manuela_vallejo/smartkitchen/comandos", message) # Tópico Original
    else:
        st.write('')

with col2:
    if st.button('OFF'):
        act1="OFF"
        client1= paho.Client("GIT-HUBM")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message = json.dumps({"Act1":act1})
        ret= client1.publish("manuela_vallejo/smartkitchen/comandos", message) # Tópico Original
    else:
        st.write('')

st.markdown("---") # Línea separadora estética

values = st.slider('Selecciona el rango de valores', 0.0, 100.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client1= paho.Client("GIT-HUBM")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message = json.dumps({"Analog": float(values)})
    ret= client1.publish("cmqtt_manu", message) # Tópico Original
else:
    st.write('')
