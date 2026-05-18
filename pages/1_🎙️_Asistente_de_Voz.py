import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Cocina con IA Real")
st.write("Escribe o dicta libremente los ingredientes que tienes en tu nevera y la IA te creará una receta única.")
st.write("---")

# 🔐 CONFIGURACIÓN DE LA IA (Pega aquí tu clave de Google AI Studio)
# Nota: Para producción es mejor usar st.secrets, pero para tu entrega puedes ponerla directo aquí:
API_KEY = "AIzaSyBGng7EBh0dKFD53KXz7cOapi5e4Pjlp9Q" 

if API_KEY != "TU_API_KEY_AQUÍ":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ Recuerda poner tu API Key de Google AI Studio en el código para que la IA responda.")

# Inicializar el historial del chat en la memoria de la página
if "chat_real" not in st.session_state:
    st.session_state["chat_real"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu chef de IA. Dime qué ingredientes tienes (ej: *'tengo pollo, papas y limón'*) y te diré qué cocinar."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🎙️ ¿Qué tienes en tu nevera?")
    
    # Grabador nativo para interactuar por voz
    audio = mic_recorder(
        start_prompt="🎙️ Grabar mis ingredientes",
        stop_prompt="🛑 Detener grabación",
        just_once=False,
        key="mic_real"
    )
    
    if audio:
        st.audio(audio['bytes'], format='audio/wav')
        st.info("🎙️ ¡Audio registrado! (Nota: Escribe tus ingredientes abajo para que la IA los procese textualmente de forma exacta en esta versión web).")

    # Cuadro de entrada libre para el usuario (Chat interactivo real)
    ingredientes_usuario = st.text_input("Escribe aquí lo que tienes (¡Lo que quieras de verdad!):", placeholder="Ej: yuca, queso, carne molida y cebolla")

    if st.button("✨ Generar Receta Personalizada", type="primary", use_container_width=True):
        if ingredientes_usuario:
            # Guardamos lo que dijo el usuario en el chat
            st.session_state["chat_real"].append({"role": "user", "content": ingredientes_usuario})
            
            if API_KEY != "TU_API_KEY_AQUÍ":
                with st.spinner("El Chef de IA está creando tu receta..."):
                    try:
                        # Creamos un prompt de diseño UX para que la IA responda estructurado
                        prompt_chef = f"Actúa como un chef profesional de asistencia en casa. El usuario te dice que tiene estos ingredientes de forma libre: '{ingredientes_usuario}'. Diseña una receta creativa, rápida y deliciosa usando únicamente esos ingredientes y básicos de despensa (sal, aceite). Dale un título llamativo y estructura los pasos de forma clara."
                        
                        respuesta = model.generate_content(prompt_chef)
                        st.session_state["chat_real"].append({"role": "assistant", "content": respuesta.text})
                    except Exception as e:
                        st.error(f"Error al conectar con Gemini: {e}")
            else:
                st.error("No puedo generar la receta porque no has puesto tu API Key en la línea 13.")

with col2:
    st.subheader("💬 Menú y Respuestas del Chef IA")
    
    # Renderizado del chat interactivo
    for msg in st.session_state["chat_real"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if len(st.session_state["chat_real"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar Nevera y Reiniciar Chat"):
            st.session_state["chat_real"] = [
                {"role": "assistant", "content": "¡Listo! Nevera vacía. ¿Qué nuevos ingredientes tienes ahora?"}
            ]
            st.rerun()
