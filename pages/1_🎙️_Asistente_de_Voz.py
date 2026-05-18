import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Voz")
st.write("Registra tus comandos de voz de forma nativa desde el navegador.")
st.write("---")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Captura de Audio Colectiva")
    st.write("Haz clic en iniciar, habla y detén la grabación:")
    
    # Grabador real de tu requerimiento streamlit-mic-recorder
    audio = mic_recorder(
        start_prompt="🎙️ Iniciar Grabación",
        stop_prompt="🛑 Detener",
        just_once=False,
        key="mic_cocina"
    )

    if audio:
        st.audio(audio['bytes'], format='audio/wav')
        st.success("¡Audio capturado correctamente en la memoria!")
        st.json({
            "Tamaño del buffer": f"{len(audio['bytes'])} bytes",
            "Formato de salida": "WAV"
        })

with col2:
    st.subheader("📖 Intenciones y Casos de Uso")
    st.markdown("""
    Este módulo está diseñado para procesar flujos de interacción como:
    * *“¿Cuánto tiempo le queda al temporizador?”*
    * *“¿Cuál es la temperatura de los sensores?”*
    """)
