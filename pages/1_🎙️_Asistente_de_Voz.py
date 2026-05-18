import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import time
import random

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Cocina por Voz Dinámico")
st.write("Graba tus ingredientes. El sistema los transcribirá en tiempo real y creará una receta única con lo que dijiste.")
st.write("---")

# Inicializar el historial del chat en la memoria de la aplicación
if "chat_dinamico_real" not in st.session_state:
    st.session_state["chat_dinamico_real"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu chef SmartKitchen. Presiona el botón, dime qué ingredientes tienes (sin importar cuáles sean) y yo los transcribiré para armar tu plato."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🎙️ Captura de Voz Directa")
    st.write("Haz clic en hablar, menciona tus alimentos de corrido y detén la grabación:")
    
    # Configuramos el grabador nativo
    audio = mic_recorder(
        start_prompt="🎙️ Empezar a dictar",
        stop_prompt="🛑 Detener y Transcribir",
        just_once=True,
        key="mic_transcriptor_dinamico"
    )
    
    texto_transcrito = ""

    # Si la persona graba un audio, se activa el proceso de conversión real
    if audio:
        st.audio(audio['bytes'], format='audio/wav')
        
        with st.spinner("Transformando tu voz en texto..."):
            try:
                # Leemos los bytes que grabaste directamente desde la memoria
                archivo_audio = io.BytesIO(audio['bytes'])
                reconocedor = sr.Recognizer()
                
                with sr.AudioFile(archivo_audio) as fuente:
                    # Ajuste de ruido para que te escuche bien en cualquier entorno
                    reconocedor.adjust_for_ambient_noise(fuente, duration=0.5)
                    datos_audio = reconocedor.record(fuente)
                    
                    # Llamada al motor de reconocimiento libre en español latino
                    texto_transcrito = reconocedor.recognize_google(datos_audio, language="es-CO")
                    st.success(f"🗣️ Transcripción exitosa: *\"{texto_transcrito}\"*")
            
            except sr.UnknownValueError:
                st.error("🎙️ El audio se recibió, pero no logré identificar las palabras. Intenta hablar más claro o pausado.")
            except sr.RequestError:
                st.warning("📡 Servicio de transcripción temporalmente saturado. Puedes escribir en la casilla de abajo.")
            except Exception as e:
                st.error(f"Aviso del sistema: {e}")

    st.write("---")
    
    # El cuadro de texto ahora se llena AUTOMÁTICAMENTE con lo que transcribió el micrófono
    ingredientes_finales = st.text_input(
        "Ingredientes listos para el Chef:", 
        value=texto_transcrito,
        placeholder="Tus palabras aparecerán aquí al hablar"
    )

    if st.button("✨ Generar Receta con lo que Dije", type="primary", use_container_width=True):
        if ingredientes_finales:
            # Guardamos lo que el usuario dijo en el historial del chat
            st.session_state["chat_dinamico_real"].append({"role": "user", "content": f"Ingredientes dictados: {ingredientes_finales}"})
            
            with st.spinner("El chef está cocinando tu idea..."):
                time.sleep(1.2)
                
                # Procesamos las palabras reales que dijiste (separa por espacios)
                palabras = [p.strip().capitalize() for p in ingredientes_finales.replace(",", " ").split(" ") if p.strip()]
                
                # Si por alguna razón la lista queda vacía, ponemos un genérico seguro
                if len(palabras) == 0:
                    palabras = ["Mis ingredientes personalizados"]
                
                # Selección aleatoria de técnicas para que la receta varíe de forma divertida
                tecnicas = ["un salteado al wok", "un guiso casero reconfortante", "una preparación express a la sartén", "un tazón gourmet"]
                tecnica_elegida = random.choice(tecnicas)
                
                titulo_plato = f"👨‍🍳 {palabras[0]} al Estilo SmartKitchen"
                ingredientes_lista = "\n".join([f"* **{item}** (Detectado desde tu audio)" for item in palabras])
                
                # Armamos las instrucciones dinámicamente usando TUS palabras reales
                pasos = f"1.  **Alistar la base:** Toma tu primer ingrediente dictado (**{palabras[0]}**), córtalo en porciones medianas y sella en una sartén con aceite caliente.\n"
                if len(palabras) >= 2:
                    pasos += f"2.  **Saborizar:** Añade **{palabras[1]}** picado finamente para armar el fondo de sabor y dejar que se mezclen los jugos.\n"
                if len(lista_ingredientes := palabras) >= 3:
                    pasos += f"3.  **Amalgama:** Incorpora **{palabras[2]}** para darle la textura perfecta y el balance de nutrientes al plato.\n"
                pasos += f"4.  **Terminado:** Baja el fuego y deja que todo se cocine por 5 minutos más hasta lograr {tecnica_elegida}. ¡Sirve inmediatamente!"

                respuesta_chef = f"""
### {titulo_plato}
¡Brillante! Con los ingredientes que acabas de dictar en tiempo real, diseñamos {tecnica_elegida}:

#### 🛒 Ingredientes Procesados:
{ingredientes_lista}

#### 📝 Preparación a la Medida:
{pasos}
"""
                st.session_state["chat_dinamico_real"].append({"role": "assistant", "content": respuesta_chef})
                st.rerun()
        else:
            st.warning("Primero debes grabar un audio o escribir los ingredientes.")

with col2:
    st.subheader("💬 Historial del Chef SmartKitchen")
    
    # Renderizar el chat interactivo
    for msg in st.session_state["chat_dinamico_real"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if len(st.session_state["chat_dinamico_real"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar historial de recetas"):
            st.session_state["chat_dinamico_real"] = [
                {"role": "assistant", "content": "¡Listo! Todo limpio. ¿Qué nuevos ingredientes vas a dictar?"}
            ]
            st.rerun()
