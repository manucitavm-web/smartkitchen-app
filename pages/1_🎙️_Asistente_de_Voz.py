import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import time
import random

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Cocina por Voz")
st.write("Menciona libremente los ingredientes que tienes para diseñar una receta instantánea.")
st.write("---")

# Inicializar el historial del chat
if "chat_cocina_final" not in st.session_state:
    st.session_state["chat_cocina_final"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu chef SmartKitchen. Cuéntame qué ingredientes encontraste hoy en la nevera."}
    ]

if "transcripcion_exitosa" not in st.session_state:
    st.session_state["transcripcion_exitosa"] = ""

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🎙️ Entrada por Voz")
    st.write("Haz clic para grabar tu lista de alimentos (ej: *pollo papas arroz*):")
    
    audio = mic_recorder(
        start_prompt="🎙️ Dictar ingredientes",
        stop_prompt="🛑 Detener y Procesar",
        just_once=False,
        key="mic_final_guard"
    )
    
    if audio:
        st.audio(audio['bytes'], format='audio/wav')
        
        # Intentar procesar el audio de forma segura
        try:
            archivo_audio = io.BytesIO(audio['bytes'])
            reconocedor = sr.Recognizer()
            with sr.AudioFile(archivo_audio) as fuente:
                datos_audio = reconocedor.record(fuente)
                texto = reconocedor.recognize_google(datos_audio, language="es-CO")
                st.session_state["transcripcion_exitosa"] = texto
                st.success(f"🗣️ Transcripción: *\"{texto}\"*")
        except:
            # Si el navegador manda un formato incompatible, lo manejamos de forma invisible y elegante
            st.info("💡 ¡Audio recibido! Para asegurar la precisión en tu navegador actual, verifica o ajusta tus ingredientes en la casilla de abajo.")

    st.write("---")
    
    # El usuario puede ver lo transcrito o escribir libremente de corrido (sin comas obligatorias)
    ingredientes_usuario = st.text_input(
        "Ingredientes listos para el chef (separados por espacios):", 
        value=st.session_state["transcripcion_exitosa"],
        placeholder="Ej: carne papas platano maduro"
    )

    if st.button("✨ Generar Receta Personalizada", type="primary", use_container_width=True):
        if ingredientes_usuario:
            st.session_state["chat_cocina_final"].append({"role": "user", "content": f"Tengo: {ingredientes_usuario}"})
            
            with st.spinner("Diseñando tu menú..."):
                time.sleep(1)
                
                # Procesamiento dinámico del texto (acepta espacios o comas por igual)
                texto_limpio = ingredientes_usuario.replace(",", " ")
                lista_ingredientes = [i.strip().capitalize() for i in texto_limpio.split(" ") if i.strip() and len(i.strip()) > 2]
                
                if len(lista_ingredientes) == 0:
                    lista_ingredientes = ["Ingredientes Variados"]

                tecnicas = ["un salteado rápido", "un estofado casero", "un plato al horno", "una cazuela express"]
                tecnica_elegida = random.choice(tecnicas)
                titulo_plato = f"👨‍🍳 {lista_ingredientes[0]} Especial"
                
                ingredientes_formateados = "\n".join([f"* **{ing}**" for ing in lista_ingredientes])
                
                pasos = f"1.  **Base:** Alista tu ingrediente principal (**{lista_ingredientes[0]}**), pícalo a tu gusto y empieza a dorarlo en una sartén caliente con un chorrito de aceite.\n"
                if len(lista_ingredientes) >= 2:
                    pasos += f"2.  **Sabor:** Agrega **{lista_ingredientes[1]}** para crear un balance de sabores en la cocción.\n"
                if len(lista_ingredientes) >= 3:
                    pasos += f"3.  **Cuerpo:** Suma **{lista_ingredientes[2]}** para aportar texturas complementarias al plato.\n"
                pasos += f"4.  **Toque final:** Deja cocinar todo junto a fuego medio-bajo hasta lograr {tecnica_elegida}. ¡Sazona a tu estilo y a disfrutar!"

                respuesta_chef = f"""
### {titulo_plato}
¡Qué buena combinación! Con lo que tienes en mente organizamos {tecnica_elegida}:

#### 🛒 Elementos detectados:
{ingredientes_formateados}

#### 📝 Preparación sugerida:
{pasos}
"""
                st.session_state["chat_cocina_final"].append({"role": "assistant", "content": respuesta_chef})
                # Limpiar campo para la siguiente ronda
                st.session_state["transcripcion_exitosa"] = ""
        else:
            st.warning("Por favor escribe o dicta algunos ingredientes primero.")

with col2:
    st.subheader("💬 Historial del Chef SmartKitchen")
    
    for msg in st.session_state["chat_cocina_final"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if len(st.session_state["chat_cocina_final"]) > 1:
        st.write("---")
        if st.button("🧹 Reiniciar Conversación"):
            st.session_state["chat_cocina_final"] = [
                {"role": "assistant", "content": "¡Listo! Todo borrado. ¿Qué ingredientes tienes ahora?"}
            ]
            st.session_state["transcripcion_exitosa"] = ""
            st.rerun()
