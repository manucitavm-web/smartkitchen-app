import streamlit as st
import paho.mqtt.client as mqtt
import time

# Configuración inicial de la página (Layout ancho para mejor visualización UX)
st.set_page_config(page_title="Monitoreo Wokwi", page_icon="🌡️", layout="wide")

st.markdown("# 🌡️ Monitoreo de Sensores (Wokwi)")
st.write("Visualiza las variables capturadas por tu circuito virtual en tiempo real.")
st.write("---")

# 📡 Configuración de red (Idéntica a tu código de Wokwi)
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "manuela_vallejo/smartkitchen"

# Inicializar los estados de la sesión en español para evitar vacíos visuales
if "temperatura" not in st.session_state:
    st.session_state["temperatura"] = "Esperando..."
if "humedad" not in st.session_state:
    st.session_state["humedad"] = "Esperando..."

# Función callback para procesar la llegada de datos desde el broker MQTT
def mensaje_recibido(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    try:
        # Separar la cadena "temperatura,humedad" que envía el ESP32
        datos = payload.split(",")
        st.session_state["temperatura"] = f"{datos[0]} °C"
        st.session_state["humedad"] = f"{datos[1]} %"
    except Exception:
        # En caso de un formato inesperado, muestra el mensaje plano para diagnóstico
        st.session_state["temperatura"] = payload

# 📊 Renderizado estético de las tarjetas métricas en dos columnas
c1, c2 = st.columns(2)
c1.metric(label="🌡️ Temperatura Horno", value=st.session_state["temperatura"])
c2.metric(label="💧 Humedad Ambiente", value=st.session_state["humedad"])

st.write("---")

# 🎨 Personalización estética del botón mediante inyección de CSS
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

# 🔄 Botón interactivo para escuchar el broker MQTT bajo demanda (Evita saturar la red)
if st.button("🔄 Actualizar Lecturas de Wokwi", type="primary", use_container_width=True):
    with st.spinner("Conectando con el circuito virtual de Wokwi..."):
        
        # Manejo de compatibilidad para versiones nuevas y antiguas de paho-mqtt
        try:
            api_version = mqtt.CallbackAPIVersion.VERSION1
            cliente = mqtt.Client(callback_api_version=api_version)
        except AttributeError:
            cliente = mqtt.Client()  # Respaldo para versiones previas
            
        cliente.on_message = mensaje_recibido
        
        try:
            # Establecer conexión y suscribirse al canal exclusivo
            cliente.connect(BROKER, PORT, 60)
            cliente.subscribe(TOPIC)
            
            # ⏱️ Bucle controlado: procesa eventos de red hasta atrapar la telemetría
            intentos = 0
            while intentos < 15:  # Límite máximo de 3 segundos (15 intentos * 0.2s)
                cliente.loop(timeout=0.2)
                
                # Si las variables cambiaron, rompemos el ciclo inmediatamente para ahorrar tiempo
                if st.session_state["temperatura"] != "Esperando...":
                    break
                    
                time.sleep(0.2)
                intentos += 1
                
            cliente.disconnect()
            
            # Feedback interactivo según el resultado de la sincronización
            if st.session_state["temperatura"] != "Esperando...":
                st.toast("¡Datos sincronizados desde Wokwi con éxito!", icon="📡")
            else:
                st.warning("No se recibió telemetría nueva. Verifica que la simulación en Wokwi esté en PLAY.")
                
            # Forzar el refresco de los componentes de Streamlit para renderizar los números
            st.rerun()
            
        except Exception as e:
            st.error(f"Error de red al conectar con el broker: {e}")
