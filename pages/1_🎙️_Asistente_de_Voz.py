import streamlit as st
from streamlit_mic_recorder import mic_recorder
import time
import random

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Cocina Inteligente")
st.write("Dicta o escribe libremente los ingredientes de tu nevera para diseñar una receta instantánea.")
st.write("---")

# Inicializar el historial del chat en la memoria de la aplicación
if "chat_廚房" not in st.session_state:
    st.session_state["chat_廚房"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente SmartKitchen. Dime qué ingredientes tienes en tu nevera hoy (ej: *'pollo, papas, cebolla'*) y te armaré una receta a la medida de inmediato."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🎙️ ¿Qué tienes a la mano?")
    
    # Grabador interactivo para la simulación de voz
    audio = mic_recorder(
        start_prompt="🎙️ Grabar ingredientes",
        stop_prompt="🛑 Detener grabación",
        just_once=False,
        key="mic_asistente"
    )
    
    if audio:
        st.audio(audio['bytes'], format='audio/wav')
        st.toast("¡Audio capturado en el sistema!", icon="🎤")

    # Entrada libre y real de texto para que escribas lo que quieras
    ingredientes = st.text_input(
        "Ingresa tus ingredientes separados por comas:", 
        placeholder="Ej: carne, tomate, arroz, plátano",
        key="input_ingredientes"
    )

    if st.button("✨ Generar Receta Personalizada", type="primary", use_container_width=True):
        if ingredientes:
            # Registrar el mensaje del usuario en el chat
            st.session_state["chat_廚房"].append({"role": "user", "content": f"Tengo: {ingredientes}"})
            
            with st.spinner("Nuestro chef digital está combinando tus ingredientes..."):
                time.sleep(1.5)  # Simula un tiempo de procesamiento fluido
                
                # Procesamos el texto del usuario de forma dinámica
                lista_ingredientes = [i.strip().capitalize() for i in ingredientes.split(",") if i.strip()]
                
                # Técnicas de cocina aleatorias para darle variedad al texto generado
                tecnicas = ["un salteado rápido", "un estofado rústico", "un tazón templado estilo bowl", "una cazuela casera"]
                tecnica_elegida = random.choice(tecnicas)
                
                # Estructura de la receta dinámica basada en la entrada real del usuario
                titulo_plato = f"👨‍🍳 {lista_ingredientes[0]} Especial SmartKitchen" if len(lista_ingredientes) > 0 else "👨‍🍳 Plato Sorpresa"
                
                ingredientes_formateados = "\n".join([f"* **{ing}** (lo que tienes en casa)." for ing in lista_ingredientes])
                
                pasos_dinamicos = ""
                if len(lista_ingredientes) >= 1:
                    pasos_dinamicos += f"1.  **Preparación base:** Toma el ingrediente principal (**{lista_ingredientes[0]}**), pícalo en trozos cómodos y dóralo en una sartén con un chorrito de aceite, sal y pimienta.\n"
                if len(lista_ingredientes) >= 2:
                    pasos_dinamicos += f"2.  **Integración:** Incorpora el segundo ingrediente (**{lista_ingredientes[1]}**) finamente picado para armar una base aromática llena de sabor.\n"
                if len(lista_ingredientes) >= 3:
                    pasos_dinamicos += f"3.  **Complemento técnico:** Suma **{lista_ingredientes[2]}** para aportar textura y cuerpo a la preparación media.\n"
                else:
                    pasos_dinamicos += "3.  **Sazón:** Añade las especias que más te gusten de tu despensa para realzar los aromas.\n"
                
                pasos_dinamicos += f"4.  **Montaje:** Junta todo a fuego medio bajo por 5 minutos adicionales hasta lograr {tecnica_elegida}. ¡Sirve caliente y disfruta!"

                # Respuesta armada dinámicamente con los datos reales del usuario
                respuesta_chef = f"""
### {titulo_plato}
¡Excelente combinación! Con lo que me listaste podemos preparar {tecnica_elegida}. Aquí tienes la propuesta estructurada:

#### 🛒 Ingredientes a Utilizar:
{ingredientes_formateados}
* *Básicos de cocina:* Aceite, sal y pimienta.

#### 📝 Modo de Preparación:
{pasos_dinamicos}

---
💡 **Consejo de Diseño UX:** Recuerda que si este plato genera vapores o humos intensos, puedes ir a la pestaña **Alertas y Tiempos** para encender el extractor remoto en Wokwi.
"""
                # Guardar respuesta en el historial
                st.session_state["chat_廚房"].append({"role": "assistant", "content": respuesta_chef})
        else:
            st.warning("Escribe al menos un ingrediente para poder ayudarte.")

with col2:
    st.subheader("💬 Menú y Sugerencias del Asistente")
    
    # Renderizar el historial completo
    for msg in st.session_state["chat_廚房"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Botón para limpiar pantalla
    if len(st.session_state["chat_廚房"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar historial de recetas"):
            st.session_state["chat_廚房"] = [
                {"role": "assistant", "content": "¡Listo! Todo despejado. ¿Qué otros ingredientes tienes para probar hoy?"}
            ]
            st.rerun()
