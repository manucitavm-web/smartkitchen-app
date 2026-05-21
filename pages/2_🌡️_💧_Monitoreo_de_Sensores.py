import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# Configuración inicial de la página (Layout ancho para mejor visualización UX)
st.set_page_config(page_title="Monitoreo Wokwi", page_icon="🌡️", layout="wide")

# --- CONFIGURACIÓN ESTÉTICA UNIFICADA (AZUL) ---
st.markdown("""
    <style>
    /* Fondo de la página en un gris azulado muy sutil y limpio */
    .main { background-color: #F4F6F9; }
    
    /* Títulos y textos en azul oscuro elegante */
    h1, h2, h3, p, span, label, .stMetric { color: #1E3A8A !important; }

    /* Estilo para TODOS los botones de Streamlit (Incluyendo el primario de actualizar) */
    div.stButton > button {
        background-color: #3B82F6 !important; /* Azul vibrante unificado */
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
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🌡️💧 Monitoreo de Sensores")

# Descripción integrada alineada con el estilo de la pestaña anterior
st.write("Panel de visualización de datos para la cocina inteligente (Smart Kitchen). Esta pestaña de la aplicación ofrece una solución interactiva de monitoreo donde cualquier usuario puede revisar el estado térmico del horno y la humedad del ambiente en tiempo real, facilitando el seguimiento preventivo de las variables climáticas del entorno.")
st.write("---")

# 📡 Datos de red (Mismo broker de tu trabajo anterior + tu canal único)
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "manuela_vallejo/smartkitchen"

# Inicializar los estados de la sesión para evitar vacíos visuales
if "temperatura" not in st.session_state:
    st.session_state["temperatura"] = "Esperando..."
if "humedad" not in st.session_state:
    st.session_state["humedad"] = "Esperando..."

# Función callback configurada para leer el formato JSON de tu ESP32
def mensaje_recibido(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        datos = json.loads(payload)
        
        # Mapea las llaves exactas del JSON que envía tu circuito
        if "Temp" in datos and "Hum" in datos:
            st.session_state["temperatura"] = f"{datos['Temp']} °C"
            st.session_state["humedad"] = f"{datos['Hum']} %"
    except Exception:
        pass  # Evita que la interfaz se rompa si llega un dato corrupto

# 📊 Renderizado de las tarjetas métricas en dos columnas
c1, c2 = st.columns(2)
c1.metric(label="🌡️ Temperatura Horno", value=st.session_state["temperatura"])
c2.metric(label="💧 Humedad Ambiente", value=st.session_state["humedad"])

st.write("---")

# 🔄 Botón interactivo bajo demanda con ventana de tiempo ampliada (Evita el aviso amarillo)
if st.button("🔄 Actualizar Lecturas de Wokwi", type="primary", use_container_width=True):
    with st.spinner("Conectando con el circuito virtual de Wokwi..."):
        
        # Limpiamos antes de escuchar para garantizar que el dato sea fresco
        st.session_state["temperatura"] = "Esperando..."
        st.session_state["humedad"] = "Esperando..."
        
        # Manejo de compatibilidad para versiones de paho-mqtt
        try:
            api_version = mqtt.CallbackAPIVersion.VERSION1
            cliente = mqtt.Client(callback_api_version=api_version)
        except AttributeError:
            cliente = mqtt.Client()
            
        cliente.on_message = mensaje_recibido
        
        try:
            cliente.connect(BROKER, PORT, 60)
            cliente.subscribe(TOPIC)
            
            # 🔥 Bucle de paciencia ampliado: 30 intentos de 0.2s = 6 segundos máximos de espera activa
            intentos = 0
            while intentos < 30:
                cliente.loop(timeout=0.2)
                
                # Si los datos cambiaron y ya no son "Esperando...", rompemos el ciclo de inmediato
                if st.session_state["temperatura"] != "Esperando...":
                    break
                    
                time.sleep(0.2)
                intentos += 1
                
            cliente.disconnect()
            
            # Feedback visual según el resultado
            if st.session_state["temperatura"] != "Esperando...":
                st.toast("¡Datos sincronizados desde Wokwi con éxito!", icon="📡")
            else:
                st.warning("No se recibió telemetría nueva. Verifica que Wokwi esté en PLAY transmitiendo.")
                
            # Forzar refresco para pintar las métricas en pantalla
            st.rerun()
            
        except Exception as e:
            st.error(f"Error de red al conectar con el broker: {e}")
