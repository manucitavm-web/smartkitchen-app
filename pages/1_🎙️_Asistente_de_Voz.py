import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import time
import random

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Cocina por Voz Nativó")
st.write("Graba tu voz enumerando libremente los ingredientes que tienes y el sistema los procesará automáticamente.")
st.write("---")

# Inicializar el historial del chat en la memoria de la aplicación
if "chat_cocina_voz" not in st.session_state:
    st.session_state["chat_cocina_voz"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente SmartKitchen. Presiona el botón de la izquierda y dime qué tienes en la nevera hoy. ¡Te escucharé con atención!"}
    ]

if "texto_transcrito" not in st.session_state:
    st.session_state["texto_transcrito"] = ""

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🎙️ Grabadora de Ingredientes")
    st.write("Haz clic, menciona tus alimentos de corrido (ej: *pollo papas cebolla*) y detén la grabación:")
    
    # Componente de grabación nativo
    audio = mic_recorder(
        start_prompt="🎙️ Dictar mis ingredientes",
        stop_prompt="🛑 Detener y Procesar",
        just_once=False,
        key="mic_automatizado"
    )
    
    if audio:
        st.audio(audio['bytes'], format='audio/wav')
        
        # --- PROCESAMIENTO AUTOMÁTICO DE SPEECH-TO-TEXT ---
        with st.spinner("Sincronizando audio y transcribiendo..."):
            try:
                # Convertir los bytes del micrófono en un archivo virtual de audio
                archivo_audio = io.BytesIO(audio['bytes'])
                reconocedor = sr.Recognizer()
                
                with sr.AudioFile(archivo_audio) as fuente:
                    datos_audio = reconocedor.record(fuente)
                    # Intentar transcribir usando el motor gratuito de Google en español
                    texto = reconocedor.recognize_google(datos_audio, language="es-CO")
                    st.session_state["texto_transcrito"] = texto
                    st.success(f"🗣️ Te entendí: *\"{texto}\"*")
            except sr.UnknownValueError:
                st.error("No logré entender el audio con claridad. Intenta hablar un poco más fuerte o cerca al micrófono.")
            except sr.RequestError:
                st.warning("El servicio de transcripción rápida está saturado. No te preocupes, puedes usar la casilla de abajo.")
            except Exception as e:
                st.error(f"Nota del sistema: {e}")

    st.write("---")
    
    # Casilla auxiliar por si el usuario quiere corregir lo que dictó o escribir directamente
    ingredientes_input = st.text_input(
        "Ingredientes detectados (puedes editarlos libremente):", 
        value=st.session_state["texto_transcrito"],
        placeholder="Ej: carne papas plátano tomate"
    )

    if st.button("✨ Generar Receta con estos Ingredientes", type="primary", use_container_width=True):
        if ingredientes_input:
            # Registrar el mensaje del usuario en el chat
            st.session_state["chat_cocina_voz"].append({"role": "user", "content": f"Tengo: {ingredientes_input}"})
            
            with st.spinner("El chef está diseñando tu menú..."):
                time.sleep(1)
                
                # Limpiamos el texto libre del usuario (reemplaza espacios por comas si es necesario)
                texto_limpio = ingredientes_input.replace(",", " ")
                lista_ingredientes = [i.strip().capitalize() for i in texto_limpio.split(" ") if i.strip() and len(i.strip()) > 2]
                
                if len(lista_ingredientes) == 0:
                    lista_ingredientes = ["Ingredientes Variados"]

                tecnicas = ["un salteado rápido", "un estofado casero", "un plato al horno", "un tazón exprés"]
                tecnica_elegida = random.choice(tecnicas)
                titulo_plato = f"👨‍🍳 {lista_ingredientes[0]} Sorpresa"
                
                ingredientes_formateados = "\n".join([f"* **{ing}**" for ing in lista_ingredientes])
                
                # Lógica dinámica de preparación
                pasos = f"1.  **Base:** Toma tu primer ingrediente (**{lista_ingredientes[0]}**), córtalo finamente y empieza a cocinarlo en una sartén con aceite.\n"
                if len(lista_ingredientes) >= 2:
                    pasos += f"2.  **Sabor:** Agrega **{lista_ingredientes[1]}** a la mezcla para potenciar los aromas del sartén.\n"
                if len(lista_ingredientes) >= 3:
                    pasos += f"3.  **Complemento:** Incorpora **{lista_ingredientes[2]}** para darle volumen e integrar las texturas de la preparación.\n"
                pasos += f"4.  **Final:** Cocina todo junto a fuego medio por unos minutos hasta lograr {tecnica_elegida}. ¡Sazona al gusto y disfruta!"

                respuesta_chef = f"""
### {titulo_plato}
¡Qué buena combinación! Con lo que dictaste organizamos {tecnica_elegida}:

#### 🛒 Elementos utilizados:
{ingredientes_formateados}

#### 📝 Preparación paso a paso:
{pasos}
"""
                st.session_state["chat_cocina_voz"].append({"role": "assistant", "content": respuesta_chef})
                # Limpiar la transcripción actual para la próxima interacción
                st.session_state["texto_transcrito"] = ""
        else:
            st.warning("Por favor graba un audio o escribe algo en la casilla para poder procesarlo.")

with col2:
    st.subheader("💬 Historial del Chef SmartKitchen")
    
    # Renderizar los mensajes del chat interactivo
    for msg in st.session_state["chat_cocina_voz"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if len(st.session_state["chat_cocina_voz"]) > 1:
        st.write("---")
        if st.button("🧹 Reiniciar Conversación"):
            st.session_state["chat_cocina_voz"] = [
                {"role": "assistant", "content": "¡Listo! Todo borrado. ¿Qué ingredientes tienes ahora?"}
            ]
            st.session_state["texto_transcrito"] = ""
            st.rerun()
