import streamlit as st
from streamlit_mic_recorder import mic_recorder
import time

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Cocina Conversacional")
st.write("Habla libremente con la IA. Dicta los ingredientes que tengas a la mano para recibir ideas personalizadas.")
st.write("---")

# Inicializar el historial de conversación en la memoria de la app si no existe
if "historial_chat" not in st.session_state:
    st.session_state["historial_chat"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente SmartKitchen. Dime qué ingredientes tienes en tu nevera hoy y te diseñaré una receta a la medida."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🎙️ Entrada de Voz")
    st.write("Presiona el botón, menciona tus ingredientes en voz alta y detén la grabación:")
    
    # Grabador de audio nativo de tus requerimientos
    audio_registro = mic_recorder(
        start_prompt="🎙️ Hablar con la IA",
        stop_prompt="🛑 Enviar Mensaje",
        just_once=False,
        key="chat_mic"
    )

    if audio_registro:
        st.audio(audio_registro['bytes'], format='audio/wav')
        
        with st.spinner("Transcribiendo y pensando..."):
            time.sleep(2) # Simulación del procesamiento de lenguaje natural
            
            # --- SIMULACIÓN DE DETECCIÓN LINGÜÍSTICA DINÁMICA ---
            # Aquí simulamos que la IA extrae el texto del audio y responde de manera fluida
            # En un entorno de producción, aquí conectarías la API de Gemini o OpenAI
            consulta_usuario = "Tengo papas, carne de res, cebolla y un tomate."
            respuesta_ia = (
                "¡Excelente combinación! Con esos ingredientes podemos preparar un **Lomo Saltado Exprés** o un **Estofado Rústico**. "
                "Aquí tienes la propuesta:\n\n"
                "**Paso 1:** Corta la carne en tiras y séllala a fuego alto en una sartén con aceite.\n"
                "**Paso 2:** Retira la carne y en la misma sartén sofríe la cebolla y el tomate en gajos.\n"
                "**Paso 3:** Mezcla todo, añade las papas (puedes hacerlas cocidas o fritas) y sazona con sal y pimienta. "
                "¡Quedará delicioso!"
            )
            # ────────────────────────────────────────────────────
        
        # Guardar la interacción en el historial para que se renderice en el chat
        st.session_state["historial_chat"].append({"role": "user", "content": f"🎤 *[Audio enviado]* -> \"{consulta_usuario}\""})
        st.session_state["historial_chat"].append({"role": "assistant", "content": respuesta_ia})

with col2:
    st.subheader("💬 Historial de la Conversación")
    
    # Renderizar el chat de manera estética usando el formato nativo de Streamlit
    for mensaje in st.session_state["historial_chat"]:
        with st.chat_message(mensaje["role"]):
            st.write(mensaje["content"])

    # Botón auxiliar para reiniciar la nevera/conversación
    if len(st.session_state["historial_chat"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar conversación y empezar de nuevo"):
            st.session_state["historial_chat"] = [
                {"role": "assistant", "content": "¡Hola de nuevo! ¿Qué otros ingredientes encontraste en la cocina?"}
            ]
            st.rerun()
