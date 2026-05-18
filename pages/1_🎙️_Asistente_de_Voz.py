import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import time

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Cocina por Voz Inteligente")
st.write("Graba tu voz diciendo los ingredientes que tienes y la IA los transcribirá para crear tu receta.")
st.write("---")

# 🔐 CLAVE API DE GOOGLE AI STUDIO (Pega tu clave aquí adentro)
API_KEY = "AIzaSyBGng7EBh0dKFD53KXz7cOapi5e4Pjlp9Q"

if API_KEY != "TU_API_KEY_AQUÍ":
    genai.configure(api_key=API_KEY)
    # Usamos el modelo más actualizado y estable
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ Recuerda pegar tu API Key en la línea 13 del código para activar la Inteligencia Artificial.")

# Inicializar el historial del chat
if "chat_conversacional_real" not in st.session_state:
    st.session_state["chat_conversacional_real"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu chef SmartKitchen. Presiona el botón de abajo, menciona de corrido los ingredientes de tu nevera y yo me encargo de escucharte y diseñar tu menú."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🎙️ Grabadora de Ingredientes")
    st.write("Haz clic, habla libremente y detén la grabación:")
    
    # Capturamos el audio nativo desde el navegador
    audio_datos = mic_recorder(
        start_prompt="🎙️ Empezar a hablar",
        stop_prompt="🛑 Detener y Enviar",
        just_once=True,
        key="mic_multimodal_real"
    )
    
    if audio_datos:
        # Mostramos el reproductor para que el usuario verifique su grabación
        st.audio(audio_datos['bytes'], format='audio/wav')
        
        if API_KEY != "TU_API_KEY_AQUÍ":
            with st.spinner("Gemini está escuchando tu audio y transcribiendo..."):
                try:
                    # Pasamos los bytes del audio directamente a la API de Google en el formato nativo
                    audio_mime = audio_datos.get('sample_mime_type', 'audio/wav')
                    input_audio = {
                        "mime_type": audio_mime,
                        "data": audio_datos['bytes']
                    }
                    
                    # Le pedimos a la IA que haga dos tareas en una: transcribir e idear la receta
                    instruccion_prompt = (
                        "Primero, transcribe exactamente los ingredientes que escuchas en este audio en una línea que diga 'Ingredientes detectados: ...'. "
                        "Luego, actuando como un chef profesional, diseña una receta creativa y estructurada utilizando únicamente esos ingredientes "
                        "y básicos de despensa (sal, aceite). Dale un título llamativo y separa los pasos de forma clara."
                    )
                    
                    # Llamada real al modelo multimodal
                    respuesta_ia = model.generate_content([instruccion_prompt, input_audio])
                    
                    # Guardamos la interacción real en el chat
                    st.session_state["chat_conversacional_real"].append({"role": "user", "content": "🎤 *[Mensaje de voz enviado]*"})
                    st.session_state["chat_conversacional_real"].append({"role": "assistant", "content": respuesta_ia.text})
                    
                except Exception as e:
                    st.error(f"Error al procesar el audio con la IA: {e}")
                    st.info("Nota de desarrollo: Verifica que el formato del micrófono esté habilitado en tu navegador.")
        else:
            st.error("No se puede procesar el audio porque falta la clave API en la línea 13.")

with col2:
    st.subheader("💬 Respuesta del Chef IA")
    
    # Renderizar la conversación completa en la pantalla
    for msg in st.session_state["chat_conversacional_real"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if len(st.session_state["chat_conversacional_real"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar historial y reiniciar chef"):
            st.session_state["chat_conversacional_real"] = [
                {"role": "assistant", "content": "¡Todo despejado! ¿Qué nuevos ingredientes vas a dictar?"}
            ]
            st.rerun()
